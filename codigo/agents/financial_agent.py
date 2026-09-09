import os
import logging
import google.generativeai as genai
from services.trading_service import TradingService, TransactionResult
from observability import tracer, trace
from langfuse import Langfuse

logger = logging.getLogger(__name__)

class FinancialAgentManager:
    def __init__(self, api_key: str, model_name: str, demo_mode: bool = False):
        self.demo_mode = demo_mode
        self.api_key = api_key
        self.model_name = model_name
        self.trading_service = TradingService(demo_mode=demo_mode)
        
        # Configurar API de Gemini
        if not self.demo_mode:
            genai.configure(api_key=self.api_key)
            
        # Inicializar Langfuse de forma opcional si estan las credenciales configuradas
        self.langfuse = None
        if os.environ.get("LANGFUSE_PUBLIC_KEY") and os.environ.get("LANGFUSE_SECRET_KEY"):
            try:
                self.langfuse = Langfuse()
                logger.info("Langfuse inicializado exitosamente.")
            except Exception as e:
                logger.warning(f"No se pudo inicializar Langfuse: {str(e)}")

    def _generate_mock_explanation(self, user_query: str, tx: TransactionResult) -> str:
        """
        Simula una respuesta natural, amigable y analitica para el Modo Demo
        """
        explanation = (
            f"**[MOCK MODE - ANALISIS DEL ASESOR DE TRADING]**\n\n"
            f"¡Hola! He procesado tu solicitud de simulación para **{tx.asset}**. Aquí tienes el análisis técnico detallado:\n\n"
            f"1. **Monto a Invertir:** ${tx.monto_invertido:,.2f} USD\n"
            f"2. **Comisión de Trading (0.5%):** ${tx.comision_pagada:,.2f} USD (Monto neto invertido: ${tx.monto_invertido - tx.comision_pagada:,.2f} USD)\n"
            f"3. **Precio de Compra Actual:** ${tx.precio_compra:,.2f} USD\n"
            f"4. **Cantidad Adquirida:** {tx.cantidad_adquirida:.6f} {tx.asset}\n\n"
            f"**Proyección si alcanza tu Precio Objetivo de ${tx.precio_objetivo:,.2f} USD:**\n"
            f"- **Valor Final de la Cartera:** ${tx.valor_proyectado:,.2f} USD\n"
            f"- **Retorno Neto (Ganancia Estimada):** **${tx.retorno_usd:,.2f} USD**\n"
            f"- **Retorno de Inversión (ROI):** **{tx.roi_porcentaje:.2f}%**\n\n"
            f"*Nota de Privacidad:* Se ha detectado e enmascarado la identidad sensible. Operación asignada al usuario anónimo: `{tx.user_id}`.\n\n"
            f"Recomendación del Asesor: Un ROI proyectado del {tx.roi_porcentaje:.2f}% es una oportunidad muy sólida. "
            f"No obstante, ten en cuenta la alta volatilidad del mercado de criptoactivos. Te sugerimos diversificar tu capital "
            f"y colocar órdenes de Stop-Loss para salvaguardar tu inversión."
        )
        return explanation

    async def run_query(self, user_name: str, user_query: str, stream: bool = False) -> str:
        """
        Procesa la consulta utilizando el conector y adaptador de trading,
        enmascara datos de usuario (PII) y solicita a Gemini que genere la explicacion.
        Soporta ejecucion con y sin streaming.
        """
        with tracer.start_as_current_span("run_query") as span:
            span.set_attribute("gemini.model", self.model_name)
            span.set_attribute("gemini.streaming", stream)
            
            # Extraer parámetros de trading de manera segura y enmascarar PII
            params = self.trading_service.extract_safe_parameters(user_query)
            masked_user = self.trading_service.mask_user_data(user_name)

            # 1. Ejecutar el adaptador de trading (conector a CoinGecko asíncrono asocia precios reales)
            tx: TransactionResult = await self.trading_service.simulate_transaction(
                user_name=user_name,
                asset_symbol=params["asset"],
                monto_usd=params["monto"],
                precio_objetivo=params["target"]
            )

            if self.demo_mode or not self.api_key or "placeholder" in self.api_key:
                span.set_attribute("gemini.demo_fallback", True)
                return self._generate_mock_explanation(user_query, tx)

            # --- CONEXIÓN REAL CON GOOGLE GEMINI 3.5 ---
            try:
                # Configurar prompt con instrucciones de sistema rigurosas
                system_prompt = (
                    "Eres un asesor financiero experto en criptoactivos y trading algorítmico.\n"
                    "Tu objetivo es explicar los cálculos de ROI, comisiones de trading y proyecciones de una simulación de forma muy analítica y amigable en español.\n\n"
                    "REGLAS DE SEGURIDAD Y PRIVACIDAD:\n"
                    "1. NUNCA expongas datos de identificación personal (PII) del usuario. Dirígete a él utilizando únicamente su identificador enmascarado proporcionado.\n"
                    "2. Presenta los cálculos de comisiones (0.5%), cantidad adquirida, valor proyectado, ganancias y ROI porcentual de forma clara.\n"
                    "3. Concluye con recomendaciones profesionales de control de riesgo (ej: stop-loss, diversificación).\n"
                )

                prompt_user = (
                    f"Consulta del usuario: {user_query}\n\n"
                    f"Datos procesados del Adaptador Financiero:\n"
                    f"- Identificador de Usuario Enmascarado: {tx.user_id}\n"
                    f"- Activo: {tx.asset}\n"
                    f"- Monto Invertido original: ${tx.monto_invertido:,.2f} USD\n"
                    f"- Comisión Cobrada (0.5%): ${tx.comision_pagada:,.2f} USD\n"
                    f"- Precio de Compra Actual: ${tx.precio_compra:,.2f} USD\n"
                    f"- Cantidad Adquirida: {tx.cantidad_adquirida:.6f} {tx.asset}\n"
                    f"- Precio Objetivo de Venta: ${tx.precio_objetivo:,.2f} USD\n"
                    f"- Valor Proyectado Final: ${tx.valor_proyectado:,.2f} USD\n"
                    f"- Ganancia Neta Estimada: ${tx.retorno_usd:,.2f} USD\n"
                    f"- Retorno de Inversión (ROI): {tx.roi_porcentaje:.2f}%\n"
                )

                # Inicializar modelo de Gemini
                model = genai.GenerativeModel(
                    model_name=self.model_name,
                    system_instruction=system_prompt
                )

                # Inicializar traza en Langfuse si esta habilitado de forma segura
                trace_lf = None
                generation_lf = None
                if self.langfuse:
                    try:
                        trace_lf = self.langfuse.trace(
                            name="Simulacion de Trading",
                            user_id=tx.user_id,
                            input=user_query,
                            metadata={
                                "asset": tx.asset,
                                "monto_usd": tx.monto_invertido,
                                "roi_porcentaje": tx.roi_porcentaje
                            }
                        )
                        generation_lf = trace_lf.generation(
                            name="Explicacion Gemini 3.5",
                            model=self.model_name,
                            model_parameters={"temperature": 0.3},
                            input=prompt_user
                        )
                    except Exception as lf_err:
                        logger.warning(f"Error registrando inicio de traza en Langfuse: {str(lf_err)}")

                # Controlar modo streaming o no streaming
                if stream:
                    # Con streaming (streamGenerateContent / generate_content_stream)
                    response = model.generate_content(prompt_user, stream=True)
                    full_text = ""
                    for chunk in response:
                        full_text += chunk.text
                    if generation_lf:
                        try:
                            generation_lf.end(output=full_text)
                        except Exception:
                            pass
                    return full_text
                else:
                    # Sin streaming (generateContent / generate_content)
                    response = model.generate_content(prompt_user)
                    res_text = response.text
                    if generation_lf:
                        try:
                            generation_lf.end(output=res_text)
                        except Exception:
                            pass
                    return res_text

            except Exception as e:
                if 'generation_lf' in locals() and generation_lf:
                    try:
                        generation_lf.end(output=f"Error: {str(e)}", status_message="FAILED")
                    except Exception:
                        pass
                logger.error(f"Error llamando a Gemini Real: {str(e)}. Fallback a mock.")
                span.set_status(trace.StatusCode.ERROR, description=str(e))
                span.record_exception(e)
                span.set_attribute("gemini.demo_fallback", True)
                return self._generate_mock_explanation(user_query, tx)
