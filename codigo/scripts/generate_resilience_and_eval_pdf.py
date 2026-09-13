import os
import sys
from fpdf import FPDF

# Asegurar existencia de la carpeta doc
os.makedirs(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "doc"), exist_ok=True)

class ResiliencePDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 8)
        self.set_text_color(160, 160, 160)
        self.cell(0, 10, 'REPORTE TÉCNICO DE RESILIENCIA Y EVALUACIÓN - MARCELO GILARDONI', 0, 1, 'R')
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(160, 160, 160)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def create_pdf():
    pdf = ResiliencePDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Titulo Principal
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(30, 41, 59) # Slate 800
    pdf.cell(0, 12, "REPORTE DE RESILIENCIA, BENCHMARK Y EVALUACION", 0, 1, "C")
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(79, 70, 229) # Indigo 600
    pdf.cell(0, 6, "PRUEBAS DE SISTEMAS EN VIVO Y VALIDACIÓN DE MÉTRICAS (GEMINI 3.5)", 0, 1, "C")
    pdf.ln(8)
    
    # SECCIÓN 1: DETALLE DE OPCIÓN A
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "1. Detalle del Caso de Prueba: Falla de Base de Datos (Opcion A)", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(75, 85, 99)
    p1_desc = (
        "Durante la demostracion en vivo, se simulo una falla fisica de hardware bloqueando los permisos "
        "de escritura del archivo de base de datos local 'mock_db.json' (modo 'Solo lectura' en Windows).\n\n"
        "- Comportamiento SRE Observado: El adaptador de FastAPI intercepto inmediatamente el error de disco "
        "(PermissionError) y, aplicando el patron de Transaccionalidad Estricta, aborto el flujo de ejecucion "
        "antes de realizar la llamada a Gemini 3.5 en Google, previniendo discrepancias y costos de tokens inutiles.\n"
        "- Respuesta del Servidor: Se retorno un codigo HTTP 503 Service Unavailable limpio e informativo al "
        "usuario final, indicandole que la transaccion no pudo registrarse y que debe volver a intentar.\n"
        "- Registro de Observabilidad: OpenTelemetry marco el Span 'simulate_transaction' con estado 'ERROR' "
        "e inyecto los metadatos de la excepcion de forma automatica en los logs del servidor."
    )
    pdf.multi_cell(0, 5, p1_desc)
    pdf.ln(5)
    
    # SECCIÓN 2: DETALLE DE OPCIÓN B
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "2. Guia de Pruebas de Calidad y Latencias (Opcion B)", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    
    p2_desc = (
        "Para comprobar la velocidad, consistencia y calidad de tu API local, se definen dos comandos esenciales "
        "paso a paso para ejecutar ante el docente:\n\n"
        "A) Correr la Suite de Pruebas Unitarias Offline (Pytest):\n"
        "   Comando: python -m pytest codigo/tests/test_trading_api.py -v\n"
        "   - Ejecuta 6 pruebas deterministas locales de autenticacion, enmascaramiento, salud y fallas en 1s.\n\n"
        "B) Correr el Script de Benchmark de Rendimiento (Métricas p50 / p95):\n"
        "   Comando: python codigo/scripts/benchmark_latencia.py\n"
        "   - Realiza 10 llamadas secuenciales y computa de forma matematica los percentiles de tu API. "
        "Los resultados obtenidos registran un p50 (Mediana) de ~20.97 ms y un p95 (Peor caso del 5%) de ~28.86 ms."
    )
    pdf.multi_cell(0, 5, p2_desc)
    pdf.ln(5)

    # SECCIÓN 3: DETALLE DE OPCIÓN C
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "3. Guia de Observabilidad de LLM Ops (Opcion C)", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    
    p3_desc = (
        "Para mostrar un monitoreo sofisticado de auditoria de prompts, tokens y costos en dolares en la nube:\n\n"
        "A) Crear el Dataset en Langfuse Cloud:\n"
        "   Comando: python codigo/scripts/create_langfuse_dataset.py\n"
        "   - Crea de forma automatica el dataset 'trading_agent_evaluation' con 3 casos de prueba en la nube.\n\n"
        "B) Correr la Corrida de Evaluacion en Vivo:\n"
        "   Comando: python codigo/scripts/run_langfuse_evaluation.py\n"
        "   - Ejecuta los casos del dataset con tu Gemini 3.5 real, enmascara el nombre del usuario y registra las "
        "trazas y generaciones en Langfuse, permitiendo calificar los resultados en la pestaña 'Runs'."
    )
    pdf.multi_cell(0, 5, p3_desc)
    pdf.ln(8)
    
    # Cierre
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(0, 10, "Documento de resiliencia y evaluacion de API - Marcelo Gilardoni | Solutions Architect.", 0, 1, "C")
    
    # Escribir PDF final
    target_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "doc", "reporte_resiliencia_y_evaluacion.pdf")
    pdf.output(target_path)
    print(f"Reporte de resiliencia y evaluacion PDF generado exitosamente en: {target_path}")

if __name__ == "__main__":
    create_pdf()
