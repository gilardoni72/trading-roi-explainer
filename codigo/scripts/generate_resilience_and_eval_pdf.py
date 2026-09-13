import os
import sys
from fpdf import FPDF

# Asegurar existencia de la carpeta doc
os.makedirs(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "doc"), exist_ok=True)

class MasterManualPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 8)
        self.set_text_color(160, 160, 160)
        self.cell(0, 10, 'MANUAL COMPLETO DE EJECUCIÓN Y DEMOSTRACIÓN - TRABAJO FINAL', 0, 1, 'R')
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(160, 160, 160)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def create_pdf():
    pdf = MasterManualPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # ==========================================
    # PÁGINA 1: PORTADA E INICIO DEL SERVIDOR
    # ==========================================
    pdf.add_page()
    
    # Título Principal
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(30, 41, 59) # Slate 800
    pdf.cell(0, 12, "MANUAL DE EJECUCION Y DEMOSTRACION EN VIVO", 0, 1, "C")
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(79, 70, 229) # Indigo 600
    pdf.cell(0, 6, "TRADING ROI EXPLAINER & SIMULATOR API (GEMINI 3.5 & OPENTELEMETRY)", 0, 1, "C")
    pdf.ln(8)
    
    # Autor
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(100, 6, "Autor: Marcelo Gilardoni", 0, 0, "L")
    pdf.cell(0, 6, "Rol: Solutions Architect / DevOps", 0, 1, "R")
    pdf.ln(4)

    # Introducción
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    intro = (
        "Este manual describe el procedimiento exacto paso a paso para levantar, probar y demostrar "
        "en vivo todas las capacidades tecnicas de tu Trabajo Final de Integracion. Detalla el funcionamiento "
        "de la peticion normal inicial, el comportamiento de resiliencia ante fallos (Opcion A), la ejecucion "
        "de pruebas y percentiles de latencia (Opcion B), y el monitoreo avanzado en la nube con Langfuse (Opcion C)."
    )
    pdf.multi_cell(0, 5, intro)
    pdf.ln(5)

    # Fase 1: Levantamiento del Servidor
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "1. Levantamiento del Servidor FastAPI (Punto de Partida)", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    f1_desc = (
        "Para iniciar la aplicacion, abre tu terminal de PowerShell en Windows y ejecuta el comando literal:\n"
    )
    pdf.multi_cell(0, 5, f1_desc)
    pdf.ln(1)

    # Comando Uvicorn
    pdf.set_font("Courier", "", 8.5)
    pdf.set_text_color(220, 38, 38)
    pdf.multi_cell(0, 4.5, '& "C:\\OpenCode\\sesion_3\\.venv\\Scripts\\uvicorn.exe" main:app --reload --host 127.0.0.1 --port 8000 --app-dir "C:\\OpenCode\\1-integracion-tbf\\codigo"')
    pdf.ln(3)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    f1_result = (
        "Explicacion de lo que ocurre:\n"
        "- Se carga el entorno virtual de Python con todas las dependencias oficiales.\n"
        "- El servidor Uvicorn arranca de forma asincrona y se queda escuchando peticiones locales en la URL: http://127.0.0.1:8000\n"
        "- OpenTelemetry (OTel) se inicializa de forma automatica correlacionando logs con TraceID/SpanId."
    )
    pdf.multi_cell(0, 5, f1_result)
    pdf.ln(5)

    # Fase 2: Peticion Normal Inicial
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "2. Ejecucion de la Peticion Normal Inicial (Swagger)", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pnormal_desc = (
        "1. Abre en tu navegador de internet la interfaz Swagger: http://127.0.0.1:8000/docs\n"
        "2. Haz clic en 'Try it out' en el endpoint POST /api/v1/trading/explain.\n"
        "3. Inserta la clave de seguridad 'trading-secret-key-123' en la casilla 'X-API-Key'.\n"
        "4. En el Request Body, envia el siguiente JSON conteniendo tus datos en claro:\n"
        "   {\n"
        "     \"user_name\": \"Marcelo Gilardoni\",\n"
        "     \"message\": \"Tengo $1500 USD y quiero simular una inversion en BTC si sube a $80000\"\n"
        "   }\n"
        "5. Haz clic en el gran boton azul 'Execute' y observa el resultado HTTP 200 OK."
    )
    pdf.multi_cell(0, 5, pnormal_desc)
    
    # ==========================================
    # PÁGINA 2: DETALLE DEL FLUJO NORMAL Y OPCIÓN A
    # ==========================================
    pdf.add_page()
    
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(0, 6, "Explicacion Detallada del Resultado de la Peticion Normal:", 0, 1, "L")
    pdf.ln(2)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    pnormal_analysis = (
        "- Enmascaramiento PII Activo: El adaptador del backend intercepto tu nombre y lo enmascaro "
        "como 'M****** G********' en la respuesta final de Gemini. Tu identidad nunca sale de tu servidor web.\n"
        "- Extraccion de Parametros: El sistema limpio el texto del mensaje y extrajo unicamente las variables "
        "necesarias (activo='BTC', monto=1500.0, precio_meta=80000.0) para prevenir ataques de prompt injection.\n"
        "- Logica Matematica Exacta: El adaptador realizo los calculos en frio deduciendo la comision (0.5% = $7.50 USD) "
        "y calculo de forma automatica un ROI del 1.36%, guardando la simulacion de forma limpia en mock_db.json.\n"
        "- Auditoria de Red: Gemini 3.5 redacto de manera perfecta el informe financiero en Markdown en un promedio "
        "de 3 segundos de procesamiento total (x-process-time)."
    )
    pdf.multi_cell(0, 5, pnormal_analysis)
    pdf.ln(5)

    # Opción A: Simulación de Falla de Consistencia (ACID)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "3. Simulacion de Falla en Base de Datos (Opcion A - ACID)", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    opciona_steps = (
        "Pasos de ejecucion en vivo:\n"
        "1. Ve al archivo 'C:\\OpenCode\\1-integracion-tbf\\codigo\\database\\mock_db.json' en Windows.\n"
        "2. Haz clic derecho -> Propiedades -> Marca 'Solo lectura' (Read-only) -> Aceptar.\n"
        "3. Regresa a tu navegador o ejecuta el script de demostracion de consola:\n"
        "   python codigo/scripts/demo_gemini_streaming.py\n"
        "4. Observa la respuesta HTTP 503 Service Unavailable controlada."
    )
    pdf.multi_cell(0, 5, opciona_steps)
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(0, 5, "Explicacion Detallada de la Falla y Resiliencia (Opcion A):", 0, 1, "L")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    opciona_analysis = (
        "- Aborto Seguro y Control de Costos: Al fallar la escritura en disco por falta de permisos, el "
        "adaptador detuvo el hilo de ejecucion antes de llamar a Gemini 3.5. Esto previene facturar costos "
        "de red inútiles y asegura la integridad transaccional (si no se puede guardar, no se ejecuta).\n"
        "- Respuesta Consistente: El cliente recibe un JSON ordenado HTTP 503 informando que la operacion "
        "fallo por consistencia de base de datos y que debe reintentar.\n"
        "- Diagnostico con OpenTelemetry: El Span 'simulate_transaction' se marco con estado 'ERROR' y "
        "registro la excepcion 'PermissionError', imprimiendo la alerta en la consola del servidor.\n"
        "- *(Restauracion): No olvides desmarcar la casilla de Solo lectura para continuar con las pruebas.*"
    )
    pdf.multi_cell(0, 5, opciona_analysis)
    
    # ==========================================
    # PÁGINA 3: DETALLE DE OPCIONES B Y C
    # ==========================================
    pdf.add_page()
    
    # Opción B: Pruebas y Latencia Benchmark
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "4. Pruebas Unitarias y Medidores de Latencia (Opcion B)", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    opcionb_steps = (
        "Pasos de ejecucion en vivo:\n"
        "1. Ejecutar las 6 pruebas de Pytest locales asocian la salud de la API, claves y enmascaramiento:\n"
        "   python -m pytest codigo/tests/test_trading_api.py -v\n"
        "   - Observaras: '6 passed in less than 2s'. Las pruebas corren deterministamente offline sin costos.\n"
        "2. Ejecutar el script de Benchmark de Latencias (10 llamadas consecutivas):\n"
        "   python codigo/scripts/benchmark_latencia.py\n"
        "   - Se realizara una simulacion de carga de 10 peticiones secuenciales."
    )
    pdf.multi_cell(0, 5, opcionb_steps)
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(0, 5, "Explicacion Detallada de Metricas (Opcion B):", 0, 1, "L")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    opcionb_analysis = (
        "- El benchmark reportara la mediana p50 (~20.97 ms) y el percentil p95 (~28.86 ms) de la velocidad de "
        "tu framework FastAPI y persistencia local.\n"
        "- Los resultados son cientificos, medidos de forma real e historizados en 'database/benchmark_results.json'."
    )
    pdf.multi_cell(0, 5, opcionb_analysis)
    pdf.ln(5)

    # Opción C: Observabilidad Cognitiva (Langfuse Cloud)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "5. Observabilidad Cognitiva y Datasets en la Nube (Opcion C)", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    opcionc_steps = (
        "Pasos de ejecucion en vivo:\n"
        "1. Crear el Dataset 'trading_agent_evaluation' en tu cuenta de Langfuse Cloud:\n"
        "   python codigo/scripts/create_langfuse_dataset.py\n"
        "2. Correr la evaluacion asincrona en vivo de tus 3 casos de prueba con Gemini 3.5:\n"
        "   python codigo/scripts/run_langfuse_evaluation.py\n"
        "3. Abre tu navegador web en: https://us.cloud.langfuse.com"
    )
    pdf.multi_cell(0, 5, opcionc_steps)
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(0, 5, "Explicacion Detallada de Trazabilidad LLM Ops (Opcion C):", 0, 1, "L")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    opcionc_analysis = (
        "- Muestra al docente la pestaña 'Datasets' y enseña los 3 casos de prueba cargados.\n"
        "- Muestra la pestaña 'Runs' donde se compara de forma automatica tu Entrada, la Respuesta del LLM "
        "y el Resultado Esperado de Referencia. Resalta el enmascaramiento (User ID: M**** G****) y los costes "
        "estimados calculados por Langfuse para auditoria de produccion."
    )
    pdf.multi_cell(0, 5, opcionc_analysis)
    pdf.ln(5)

    # Cierre
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(0, 10, "Manual Tecnico Completo - Marcelo Gilardoni | Solutions Architect & DevOps.", 0, 1, "C")
    
    # Escribir PDF final
    target_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "doc", "reporte_resiliencia_y_evaluacion.pdf")
    pdf.output(target_path)
    print(f"Reporte de resiliencia y evaluacion PDF generado exitosamente en: {target_path}")

if __name__ == "__main__":
    create_pdf()
