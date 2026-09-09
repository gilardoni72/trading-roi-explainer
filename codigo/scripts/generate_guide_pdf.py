import os
import sys
from fpdf import FPDF

# Asegurar existencia de la carpeta doc
os.makedirs(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "doc"), exist_ok=True)

class GuidePDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 8)
        self.set_text_color(160, 160, 160)
        self.cell(0, 10, 'GUÍA DE DEMOSTRACIÓN EN VIVO - TRABAJO FINAL DE INTEGRACIÓN', 0, 1, 'R')
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(160, 160, 160)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def create_guide_pdf():
    pdf = GuidePDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Titulo Principal
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(30, 41, 59) # Slate 800
    pdf.cell(0, 12, "GUIA DE DEMOSTRACION EN VIVO", 0, 1, "C")
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(79, 70, 229) # Indigo 600
    pdf.cell(0, 6, "TRADING ROI EXPLAINER & TRANSACTION SIMULATOR API (GEMINI 3.5)", 0, 1, "C")
    pdf.ln(8)

    # Introduccion
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    intro_text = (
        "Esta guia contiene la secuencia detallada de comandos paso a paso para realizar una demostracion "
        "en vivo impecable y espectacular de tu trabajo final de integracion (Marcelo Gilardoni)."
    )
    pdf.multi_cell(0, 5, intro_text)
    pdf.ln(5)

    # PASO 0
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "Paso 0: Preparacion Inicial de la Consola", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    p0_desc = (
        "Abre una terminal de PowerShell en tu computadora y ejecuta los siguientes comandos:\n"
        "1. Posicionarte en la carpeta de tu trabajo final:\n"
        "   cd C:\\OpenCode\\1-integracion-tbf\n"
        "2. Activar el entorno virtual de Python:\n"
        "   .\\.venv\\Scripts\\Activate.ps1"
    )
    pdf.multi_cell(0, 5, p0_desc)
    pdf.ln(5)

    # PASO 1
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "Paso 1: Demostracion de Gemini 3.5 en Consola (Streaming vs No Streaming)", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    p1_desc = (
        "Compara la respuesta síncrona contra la visualización en vivo de tokens.\n"
        "1. Ejecutar CON STREAMING:\n"
        "   python codigo/scripts/demo_gemini_streaming.py --stream\n"
        "   - Resalta la velocidad percibida instantánea (<1s).\n"
        "   - Resalta la caja de comprobación de enmascaramiento: 'Maria Gomez' -> 'M**** G****'.\n"
        "2. Ejecutar SIN STREAMING:\n"
        "   python codigo/scripts/demo_gemini_streaming.py\n"
        "   - Muestra la espera síncrona estática (20s) para justificar el uso de streaming en producción."
    )
    pdf.multi_cell(0, 5, p1_desc)
    pdf.ln(5)

    # PASO 2
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "Paso 2: Levantar el Servidor Web e Interfaz Swagger (FastAPI)", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    p2_desc = (
        "Muestra el endpoint cerrado con llave ante accesos no autorizados:\n"
        "1. Inicia el servidor FastAPI:\n"
        "   python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000 --app-dir \"codigo\"\n"
        "2. Abre la documentacion interactiva en el navegador:\n"
        "   http://127.0.0.1:8000/docs\n"
        "3. Demuestra la proteccion X-API-Key: Sin cabecera el servidor bloquea con error HTTP 401. "
        "Al ingresar la clave 'trading-secret-key-123' en la autorizacion superior, retorna 200 OK."
    )
    pdf.multi_cell(0, 5, p2_desc)
    pdf.ln(5)

    # PASO 3
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "Paso 3: Demostracion de Observabilidad con OpenTelemetry (OTel)", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    p3_desc = (
        "Demuestra el sistema de diagnostico de trazas y logs en tiempo real:\n"
        "1. Desglose de Spans: Muestra los logs '[OTel Span]' con las latencias por capa (conector, adaptador, Gemini).\n"
        "2. Correlacion de Logs: Resalta que cada registro de log posee el [TraceId: ... | SpanId: ...].\n"
        "3. Diagnostico de Errores: Ejecuta un curl enviando un activo no valido como 'XYZ' y observa el Span de ERROR.\n"
        "4. Simulación de Falla en Base de Datos: Cambia 'mock_db.json' a 'Solo Lectura' en Windows. "
        "Verás cómo el sistema aborta de inmediato la llamada a Gemini para resguardar la consistencia "
        "financiera y le indica al cliente que vuelva a intentar (Retornando error 503)."
    )
    pdf.multi_cell(0, 5, p3_desc)
    pdf.ln(5)

    # PASO 4
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "Paso 4: Observabilidad en la Nube con Langfuse (LLM Ops)", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    p4_desc = (
        "1. Abre en tu navegador la consola web de Langfuse Cloud:\n"
        "   https://us.cloud.langfuse.com\n"
        "2. Señala el costo en USD, el conteo exacto de tokens de Gemini 3.5, "
        "el enmascaramiento de datos personales de 'Maria Gomez' a 'M**** G****' en las trazas, "
        "los prompts y generaciones de la simulacion."
    )
    pdf.multi_cell(0, 5, p4_desc)
    pdf.ln(5)

    # PASO 5
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "Paso 5: Evaluacion de Calidad con Datasets en Langfuse", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    p5_desc = (
        "1. Crear el Dataset 'trading_agent_evaluation' en la nube:\n"
        "   python codigo/scripts/create_langfuse_dataset.py\n"
        "2. Correr la evaluacion en vivo de los 3 casos de prueba con Gemini:\n"
        "   python codigo/scripts/run_langfuse_evaluation.py\n"
        "3. En la consola de Langfuse, muestra la pestaña 'Runs' con la comparativa lado a lado."
    )
    pdf.multi_cell(0, 5, p5_desc)
    pdf.ln(5)

    # PASO 6
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "Paso 6: Pruebas y Medicion de Latencias ( p50 y p95 )", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    p6_desc = (
        "1. Ejecutar las pruebas unitarias y de enmascaramiento de datos:\n"
        "   python -m pytest codigo/tests/test_trading_api.py -v\n"
        "2. Ejecutar el benchmark para medir p50 y p95 latencia (10 llamadas consecutivas):\n"
        "   python codigo/scripts/benchmark_latencia.py\n"
        "   Se generara la tabla de percentiles en pantalla y se guardara en benchmark_results.json."
    )
    pdf.multi_cell(0, 5, p6_desc)
    pdf.ln(5)

    # Guardar PDF final
    target_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "doc", "guia_demostracion.pdf")
    pdf.output(target_path)
    print(f"Guía de demostración PDF generada exitosamente en: {target_path}")

if __name__ == "__main__":
    create_guide_pdf()
