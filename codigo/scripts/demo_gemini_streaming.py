import argparse
import asyncio
import json
import sys
import os
import google.generativeai as genai

# Forzar codificacion UTF-8 para evitar errores de consola en Windows con Emojis
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Asegurar PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings
from agents.financial_agent import FinancialAgentManager

async def main():
    # Configurar el lector de argumentos de consola (argparse)
    parser = argparse.ArgumentParser(description="Demo de consulta de trading utilizando Gemini 3.5")
    parser.add_argument(
        "--stream", 
        action="store_true", 
        help="Habilita la ejecucion en modo streaming real token por token"
    )
    args = parser.parse_args()

    # Inicializar el agente con tu API Key y Gemini 3.5
    api_key = settings.GEMINI_API_KEY
    model_name = settings.GEMINI_MODEL
    
    genai.configure(api_key=api_key)
    manager = FinancialAgentManager(
        api_key=api_key,
        model_name=model_name,
        demo_mode=False
    )
    
    user_name = "Maria Gomez"
    user_query = "Tengo $1500 USD y quiero simular una inversion en BTC si sube a $80000"

    print("=" * 70)
    print("💎 GEMINI 3.5 TRADING EXPLAINER - TRABAJO FINAL DE INTEGRACIÓN")
    print(f"MODO SELECCIONADO: {'CON STREAMING' if args.stream else 'SIN STREAMING'}")
    print("=" * 70)
    print(f"Usuario PII Original: {user_name}")
    print(f"Consulta: '{user_query}'")
    print("-" * 70)

    try:
        # Procesar transaccion simulada con el adaptador financiero
        print("[Adaptador Financiero] Procesando calculos, comisiones del 0.5% y enmascaramiento...")
        tx = await manager.trading_service.simulate_transaction(
            user_name=user_name,
            asset_symbol="BTC",
            monto_usd=1500.0,
            precio_objetivo=80000.0
        )
        print(f"[Adaptador Financiero] Usuario enmascarado: {tx.user_id}")
        print(f"[Adaptador Financiero] Comision deducida: ${tx.comision_pagada} USD")
        print(f"[Adaptador Financiero] ROI Calculado: {tx.roi_porcentaje}%\n")

        # Prompt del sistema e instrucciones de enmascaramiento
        system_prompt = (
            "Eres un asesor financiero experto en criptoactivos y trading algoritmico.\n"
            "Tu objetivo es explicar los calculos de ROI, comisiones de trading y proyecciones de una simulacion de forma muy analitica y amigable en espanol.\n\n"
            "REGLAS DE SEGURIDAD Y PRIVACIDAD:\n"
            "1. NUNCA expongas datos de identificacion personal (PII) del usuario. Dirigete a el utilizando unicamente su identificador enmascarado proporcionado.\n"
            "2. Presenta los calculos de comisiones (0.5%), cantidad adquirida, valor proyectado, ganancias y ROI porcentual de forma clara.\n"
            "3. Concluye con recomendaciones profesionales de control de riesgo (ej: stop-loss, diversificacion).\n"
        )

        prompt_user = (
            f"Consulta del usuario: {user_query}\n\n"
            f"Datos procesados del Adaptador Financiero:\n"
            f"- Identificador de Usuario Enmascarado: {tx.user_id}\n"
            f"- Activo: {tx.asset}\n"
            f"- Monto Invertido original: ${tx.monto_invertido:,.2f} USD\n"
            f"- Comision Cobrada (0.5%): ${tx.comision_pagada:,.2f} USD\n"
            f"- Precio de Compra Actual: ${tx.precio_compra:,.2f} USD\n"
            f"- Cantidad Adquirida: {tx.cantidad_adquirida:.6f} {tx.asset}\n"
            f"- Precio Objetivo de Venta: ${tx.precio_objetivo:,.2f} USD\n"
            f"- Valor Proyectado Final: ${tx.valor_proyectado:,.2f} USD\n"
            f"- Ganancia Neta Estimada: ${tx.retorno_usd:,.2f} USD\n"
            f"- Retorno de Inversion (ROI): {tx.roi_porcentaje:.2f}%\n"
        )

        # --- COMPROBACIÓN DE ENMASCARAMIENTO ---
        print("\n" + "#" * 70)
        print("🔍 PROMPT DE SISTEMA Y DATOS SANITIZADOS ENVIADOS A GEMINI 3.5:")
        print("#" * 70)
        print(f"--- SYSTEM INSTRUCTION (Rol cognitivo y privacidad) ---\n{system_prompt}")
        print(f"--- USER PROMPT CONTEXT (Solo variables de entrada limpias) ---\n{prompt_user}")
        print("#" * 70 + "\n")

        print("[LLM Explainer] Enviando datos sanitizados a Gemini 3.5 en Google...")

        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_prompt
        )

        start_time = asyncio.get_event_loop().time()

        if args.stream:
            # --- MODO CON STREAMING ---
            print("\n[INICIO DEL STREAM REAL] ")
            response_stream = model.generate_content(prompt_user, stream=True)
            for chunk in response_stream:
                print(chunk.text, end="", flush=True)
            duration = asyncio.get_event_loop().time() - start_time
            print(f"\n\n[FIN DEL STREAM] - Duracion total: {duration:.2f} s")
        else:
            # --- MODO SIN STREAMING ---
            print("\nEsperando respuesta completa...")
            response = model.generate_content(prompt_user)
            duration = asyncio.get_event_loop().time() - start_time
            print(f"\nRespuesta Recibida Completa ({duration:.2f} s):\n")
            print(response.text)

    except IOError as ioe:
        # CONTROLADOR DE CONSISTENCIA DE BASE DE DATOS
        print("\n" + "!" * 70)
        print("❌ ERROR CRÍTICO DE CONSISTENCIA DE BASE DE DATOS (PROCESO ABORTADO)")
        print("!" * 70)
        print(f"Detalle del fallo: {str(ioe)}")
        print("\n[POLÍTICA DE TRANSACCIONALIDAD FINANCIERA (ACID)]")
        print("- Se ha abortado la llamada a Gemini 3.5 para evitar costes y desajustes.")
        print("- El registro no pudo ser salvaguardado en el libro contable local.")
        print("- Mensaje entregado al cliente: 'Operación fallida por consistencia. Reintente.'")
        print("!" * 70 + "\n")

    except Exception as e:
        print("\n" + "!" * 70)
        print("AVISO: Limite de Cuota superado (429 Rate Limit) o Error de API de Gemini.")
        print("La version gratuita de Gemini permite un maximo de 5 peticiones por minuto.")
        print("Activando el simulador financiero inteligente local (Modo Demo Offline) para la demostracion...")
        print("!" * 70 + "\n")
        
        fallback_text = manager._generate_mock_explanation(user_query, tx)
        print(fallback_text)
        
    print("=" * 70)

    # --- REPORTE DE MÉTRICAS DE RENDIMIENTO ---
    try:
        results_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "benchmark_results.json")
        if os.path.exists(results_path):
            with open(results_path, "r") as f:
                res = json.load(f)
            print("\n" + "=" * 70)
            print("📊 REPORTE DE METRICAS DE LATENCIA (BENCHMARK DE RENDIMIENTO)")
            print("=" * 70)
            print(f"Metricas calculadas sobre 10 peticiones secuenciales:")
            print(f"- Latencia Minima:   {res.get('fastest_ms')} ms")
            print(f"- Latencia Maxima:   {res.get('slowest_ms')} ms")
            print(f"- Latencia Promedio: {res.get('avg_ms')} ms")
            print(f"- PERCENTIL p50 (Mediana):  {res.get('p50_ms')} ms")
            print(f"- PERCENTIL p95 (Peor 5%):  {res.get('p95_ms')} ms")
            print("=" * 70)
    except Exception:
        pass

    # Forzar flush de OpenTelemetry para asegurar la impresion de Spans en consola
    try:
        from opentelemetry import trace
        trace.get_tracer_provider().force_flush()
    except Exception:
        pass

if __name__ == "__main__":
    asyncio.run(main())
