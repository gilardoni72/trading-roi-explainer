import os
import json
import logging
import httpx
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from config import settings
from observability import tracer

logger = logging.getLogger(__name__)

# --- Esquemas de Datos (Contracts) ---
class AssetPrice(BaseModel):
    symbol: str
    name: str
    price_usd: float
    is_demo: bool

class TransactionResult(BaseModel):
    user_id: str = Field(description="ID de usuario enmascarado/anonimizado")
    asset: str
    monto_invertido: float
    precio_compra: float
    cantidad_adquirida: float
    comision_pagada: float
    precio_objetivo: float
    valor_proyectado: float
    retorno_usd: float
    roi_porcentaje: float
    is_demo: bool

class TradingService:
    def __init__(self, demo_mode: bool = True):
        self.demo_mode = demo_mode
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "mock_db.json")
        self.mock_prices = {
            "BTC": {"name": "Bitcoin", "price_usd": 65000.0},
            "ETH": {"name": "Ethereum", "price_usd": 3500000.0}, # Or ~3500.0
            "SOL": {"name": "Solana", "price_usd": 150.0}
        }
        # Asegurar existencia de base de datos mock
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        if not os.path.exists(self.db_path):
            with open(self.db_path, "w") as f:
                json.dump([], f)

    def mask_user_data(self, raw_name: str) -> str:
        """
        Enmascara el nombre del usuario para proteger la Privacidad PII.
        Ejemplo: 'Maria Gomez' -> 'M**** G****'
        """
        if not raw_name:
            return "U****"
        parts = raw_name.strip().split()
        masked_parts = []
        for part in parts:
            if len(part) > 1:
                masked_parts.append(part[0] + "*" * (len(part) - 1))
            else:
                masked_parts.append(part)
        return " ".join(masked_parts)

    def extract_safe_parameters(self, text: str) -> Dict[str, Any]:
        """
        Extrae estrictamente los parametros transaccionales de la consulta
        para evitar que viaje texto libre con informacion sensible.
        """
        text_lower = text.lower()
        
        # Activo
        asset = "BTC"
        if "eth" in text_lower or "ethereum" in text_lower:
            asset = "ETH"
        elif "sol" in text_lower or "solana" in text_lower:
            asset = "SOL"
            
        # Buscar montos (ej: $1500, 1500, etc.)
        # Hacemos una extraccion simple para simular un parser estricto
        monto = 1000.0
        import re
        monto_match = re.search(r'(?:usd|\$)\s*(\d+(?:\.\d+)?)', text_lower)
        if not monto_match:
            monto_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:usd|\$|dolares|dólares)', text_lower)
        if not monto_match:
            # Buscar cualquier numero de 3 o mas digitos
            monto_match = re.search(r'\b(\d{3,})\b', text_lower)
            
        if monto_match:
            try:
                monto = float(monto_match.group(1))
            except ValueError:
                pass
                
        # Buscar precio objetivo
        precio_objetivo = 0.0
        target_match = re.search(r'(?:objetivo|target|llegue a|suba a|vender a)\s*(?:usd|\$)?\s*(\d+(?:\.\d+)?)', text_lower)
        if target_match:
            try:
                precio_objetivo = float(target_match.group(1))
            except ValueError:
                pass
                
        return {
            "asset": asset,
            "monto": monto,
            "target": precio_objetivo
        }

    async def get_asset_price(self, symbol: str) -> AssetPrice:
        """
        CONNECTOR: Obtiene el precio del activo desde el exterior.
        En modo demo usa simulador, en modo real consulta un endpoint externo.
        """
        with tracer.start_as_current_span("get_asset_price") as span:
            sym = symbol.upper().strip()
            span.set_attribute("trading.asset", sym)
            span.set_attribute("trading.demo_mode", self.demo_mode)
            if self.demo_mode:
                price_info = self.mock_prices.get(sym, {"name": sym, "price_usd": 100.0})
                # Pequena variacion para simular movimiento real
                import random
                variation = random.uniform(-0.01, 0.01)
                final_price = price_info["price_usd"] * (1 + variation)
                return AssetPrice(
                    symbol=sym,
                    name=price_info["name"],
                    price_usd=round(final_price, 2),
                    is_demo=True
                )
            else:
                # Consumo de API real de CoinGecko
                try:
                    # Mapeo de simbolos a ids de coingecko
                    coingecko_ids = {
                        "BTC": "bitcoin",
                        "ETH": "ethereum",
                        "SOL": "solana"
                    }
                    cg_id = coingecko_ids.get(sym, "bitcoin")
                    url = f"https://api.coingecko.com/api/v3/simple/price?ids={cg_id}&vs_currencies=usd"
                    async with httpx.AsyncClient() as client:
                        response = await client.get(url, timeout=10.0)
                        response.raise_for_status()
                        data = response.json()
                        price = data[cg_id]["usd"]
                        span.set_attribute("trading.price_usd", float(price))
                        return AssetPrice(
                            symbol=sym,
                            name=sym,
                            price_usd=float(price),
                            is_demo=False
                        )
                except Exception as e:
                    logger.error(f"Error llamando a CoinGecko: {str(e)}. Fallback a demo.")
                    span.set_status(trace.StatusCode.ERROR, description=str(e))
                    span.record_exception(e)
                    # Fallback seguro
                    price_info = self.mock_prices.get(sym, {"name": sym, "price_usd": 100.0})
                    return AssetPrice(
                        symbol=sym,
                        name=price_info["name"],
                        price_usd=price_info["price_usd"],
                        is_demo=True
                    )

    async def simulate_transaction(self, user_name: str, asset_symbol: str, monto_usd: float, precio_objetivo: float) -> TransactionResult:
        """
        ADAPTER: Toma el precio en crudo del conector y calcula las comisiones,
        cantidad comprada, valor proyectado, ganancias y ROI. Guarda la transaccion.
        """
        with tracer.start_as_current_span("simulate_transaction") as span:
            span.set_attribute("trading.asset_symbol", asset_symbol)
            span.set_attribute("trading.monto_usd", monto_usd)
            span.set_attribute("trading.target_price", precio_objetivo)
            
            # 1. Obtener precio actual
            price_data = await self.get_asset_price(asset_symbol)
            precio_actual = price_data.price_usd
            
            # 2. Comision del Broker (0.5% fija)
            comision_rate = 0.005
            comision_pagada = monto_usd * comision_rate
            monto_neto = monto_usd - comision_pagada
            
            # 3. Cantidad comprada
            cantidad_adquirida = monto_neto / precio_actual
            
            # 4. Si no se especifico precio objetivo, asumir un incremento del 20%
            if precio_objetivo <= 0:
                precio_objetivo = precio_actual * 1.20
                
            # 5. Valor proyectado en precio objetivo
            valor_proyectado = cantidad_adquirida * precio_objetivo
            
            # 6. Retorno (neto de inversion original)
            retorno_usd = valor_proyectado - monto_usd
            
            # 7. ROI Porcentaje
            roi_porcentaje = (retorno_usd / monto_usd) * 100
            
            # Enmascarar usuario para privacidad
            masked_user = self.mask_user_data(user_name)
            
            span.set_attribute("trading.user_id_masked", masked_user)
            span.set_attribute("trading.roi_percentage", roi_porcentaje)
            
            result = TransactionResult(
                user_id=masked_user,
                asset=asset_symbol.upper(),
                monto_invertido=monto_usd,
                precio_compra=precio_actual,
                cantidad_adquirida=round(cantidad_adquirida, 6),
                comision_pagada=round(comision_pagada, 2),
                precio_objetivo=round(precio_objetivo, 2),
                valor_proyectado=round(valor_proyectado, 2),
                retorno_usd=round(retorno_usd, 2),
                roi_porcentaje=round(roi_porcentaje, 2),
                is_demo=self.demo_mode or price_data.is_demo
            )
            
            # Registrar transaccion en db local
            try:
                with open(self.db_path, "r") as f:
                    txs = json.load(f)
                txs.append(result.model_dump())
                with open(self.db_path, "w") as f:
                    json.dump(txs, f, indent=4)
            except Exception as e:
                logger.error(f"No se pudo guardar la transaccion: {str(e)}")
                span.record_exception(e)
                span.set_status(trace.StatusCode.ERROR, description=str(e))
                raise IOError(f"Error de consistencia de datos: No se pudo registrar la simulacion en base de datos. Motivo: {str(e)}")
                
            return result
