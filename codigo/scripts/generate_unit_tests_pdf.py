import os
import sys
from fpdf import FPDF

# Asegurar existencia de la carpeta doc
os.makedirs(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "doc"), exist_ok=True)

class UnitTestsPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 8)
        self.set_text_color(160, 160, 160)
        self.cell(0, 10, 'REPORTE TÉCNICO DE PRUEBAS UNITARIAS OFFLINE - MARCELO GILARDONI', 0, 1, 'R')
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(160, 160, 160)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def create_pdf():
    pdf = UnitTestsPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Titulo Principal
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(30, 41, 59) # Slate 800
    pdf.cell(0, 12, "REPORTE DETALLADO DE PRUEBAS UNITARIAS (QA)", 0, 1, "C")
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(79, 70, 229) # Indigo 600
    pdf.cell(0, 6, "ASEGURAMIENTO DE CALIDAD DETERMINISTA Y OFFLINE (PYTEST)", 0, 1, "C")
    pdf.ln(8)
    
    # Autor
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(100, 6, "Estudiante: Marcelo Gilardoni", 0, 0, "L")
    pdf.cell(0, 6, "Usuario de GitHub: gilardoni72", 0, 1, "R")
    pdf.ln(4)

    # Introducción
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    intro_text = (
        "Este manual tecnico describe individualmente el funcionamiento, entradas, salidas y "
        "criterios de validacion de las 6 pruebas unitarias deterministas implementadas en pytest "
        "(test_trading_api.py). Estas pruebas garantizan el correcto funcionamiento de tu API de Trading "
        "de forma 100% offline antes del despliegue productivo."
    )
    pdf.multi_cell(0, 5, intro_text)
    pdf.ln(5)

    # Tabla de Contenidos / Conceptos de QA
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "1. Filosofia de Pruebas Unitarias Deterministas (Sin LLM)", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    qa_phil = (
        "En la ingenieria de software moderna, las pruebas unitarias deben ser rapidas, deterministas y "
        "completamente independientes de servicios externos de red. Es por ello que nuestra suite "
        "esta diseñada bajo el patron de 'Tool Correctness'.\n\n"
        "Comprueba de forma logica el correcto enrutamiento de FastAPI, la tipacion con Pydantic, "
        "el bloqueo perimetral de seguridad y el comportamiento de resiliencia ACID en disco (mock_db.json) "
        "sin realizar una sola llamada pagada o lenta a Gemini en internet. Esto permite correr "
        "las pruebas en menos de 2 segundos de forma local."
    )
    pdf.multi_cell(0, 5, qa_phil)
    pdf.ln(5)

    # Desglose de los 6 tests
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "2. Analisis Detallado de las 6 Pruebas Unitarias", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)

    tests_details = [
        {
            "id": "1. test_health_endpoint (Prueba de Salud del Sistema)",
            "desc": "Qué hace: Envía una solicitud GET / al servidor FastAPI.\n"
                    "Qué valida: Comprueba que el servidor responda de inmediato con un código HTTP 200 OK y el JSON {'status': 'online'}.\n"
                    "Por qué importa: Confirma que la infraestructura web básica esté levantada y responda adecuadamente."
        },
        {
            "id": "2. test_explain_trading_endpoint_unauthorized_missing_header (Seguridad Faltante)",
            "desc": "Qué hace: Envía una simulación POST al endpoint de trading sin la cabecera X-API-Key.\n"
                    "Qué valida: Que el servidor bloquee la llamada y retorne de inmediato un código HTTP 401 Unauthorized.\n"
                    "Por qué importa: Garantiza que el cortafuegos de tu API esté activo por defecto ante accesos anónimos."
        },
        {
            "id": "3. test_explain_trading_endpoint_unauthorized_wrong_key (Seguridad Clave Incorrecta)",
            "desc": "Qué hace: Envía una simulación POST colocando una clave incorrecta en la cabecera X-API-Key.\n"
                    "Qué valida: Que el servidor identifique que la clave no coincide y retorne de inmediato un código HTTP 401 Unauthorized.\n"
                    "Por qué importa: Asegura que el validador autentique estrictamente los tokens (no solo que existan, sino que coincidan)."
        },
        {
            "id": "4. test_explain_trading_endpoint_authorized_success (Flujo Exitoso Completo)",
            "desc": "Qué hace: Envía una simulación de inversión válida con la clave de acceso correcta.\n"
                    "Qué valida: Que el servidor retorne HTTP 200 OK, realice los cálculos matemáticos de ROI y comisiones de forma exacta en Python, y enmascare los datos personales (Maria Gomez -> M**** G****).\n"
                    "Por qué importa: Es el Happy Path del sistema; valida que tus algoritmos de negocio y enmascaramiento funcionen de forma integrada."
        },
        {
            "id": "5. test_explain_trading_endpoint_validation_empty_message (Validación de Datos)",
            "desc": "Qué hace: Envía una petición con un mensaje de consulta vacío o lleno de puros espacios.\n"
                    "Qué valida: Que el controlador FastAPI intercepte la entrada inválida y retorne un código HTTP 400 Bad Request.\n"
                    "Por qué importa: Previene que la API envíe prompts vacíos a internet, evitando costos inútiles de red en Google."
        },
        {
            "id": "6. test_explain_alias_endpoint_success (Prueba de Retrocompatibilidad)",
            "desc": "Qué hace: Envía una consulta válida utilizando la ruta de compatibilidad de los laboratorios anteriores (/weather/explain).\n"
                    "Qué valida: Que el alias funcione de manera idéntica al endpoint principal, retornando un HTTP 200 OK con el reporte financiero.\n"
                    "Por qué importa: Garantiza la retrocompatibilidad estricta con las llamadas automáticas del profesor sin romper sus integraciones."
        }
    ]

    for test in tests_details:
        pdf.set_font("Helvetica", "B", 10.5)
        pdf.set_text_color(51, 65, 85)
        pdf.cell(0, 5, test["id"], 0, 1, "L")
        pdf.set_font("Helvetica", "", 9.5)
        pdf.set_text_color(75, 85, 99)
        pdf.multi_cell(0, 4.5, test["desc"])
        pdf.ln(3.5)
        
    pdf.ln(5)
    pdf.set_font("Helvetica", "I", 9.5)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(0, 10, "Fin del Reporte de Pruebas Unitarias - Marcelo Gilardoni | Solutions Architect & SRE.", 0, 1, "C")
    
    # Escribir PDF final
    target_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "doc", "pruebas_unitarias.pdf")
    pdf.output(target_path)
    print(f"Reporte de pruebas unitarias PDF generado exitosamente en: {target_path}")

if __name__ == "__main__":
    create_pdf()
