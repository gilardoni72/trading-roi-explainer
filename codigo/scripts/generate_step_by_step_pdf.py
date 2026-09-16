import os
import sys
from fpdf import FPDF

# Asegurar existencia de la carpeta doc
os.makedirs(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "doc"), exist_ok=True)

class PasoAPasoPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 8)
        self.set_text_color(160, 160, 160)
        self.cell(0, 10, 'GUÍA DE EXPOSICIÓN EN VIVO PASO A PASO - MARCELO GILARDONI', 0, 1, 'R')
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(160, 160, 160)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def create_pdf():
    pdf = PasoAPasoPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # ==========================================
    # PÁGINA 1: PORTADA Y PASOS 0, 1 & 2
    # ==========================================
    pdf.add_page()
    
    # Titulo Principal
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(30, 41, 59) # Slate 800
    pdf.cell(0, 12, "GUIA PASO A PASO DE SUSTENTACION EN VIVO", 0, 1, "C")
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(79, 70, 229) # Indigo 600
    pdf.cell(0, 6, "TRADING ROI EXPLAINER & SIMULATOR API (MARCELO GILARDONI)", 0, 1, "C")
    pdf.ln(8)
    
    # Autor
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(100, 6, "Estudiante: Marcelo Gilardoni", 0, 0, "L")
    pdf.cell(0, 6, "Repositorio: gilardoni72/trading-roi-explainer", 0, 1, "R")
    pdf.ln(4)

    # Introducción
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    intro_text = (
        "Este documento contiene la secuencia exacta de comandos, flujos e indicaciones paso a paso "
        "para realizar tu sustentacion en vivo de forma impecable. Sigue cada paso secuencialmente "
        "copiando y pegando los comandos en tu terminal de PowerShell."
    )
    pdf.multi_cell(0, 5, intro_text)
    pdf.ln(4)

    # Paso 0: Preparación
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "Paso 0: Preparacion Inicial de la Consola", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    p0_text = (
        "Abre PowerShell en tu computadora y ejecuta los siguientes comandos de preparacion:\n"
        "1. Posicionarte en la carpeta del proyecto:\n"
        "   cd C:\\OpenCode\\1-integracion-tbf\n"
        "2. Asegurar que la Base de Datos este en modo lectura/escritura (Desbloquear):\n"
        "   Set-ItemProperty -Path \"C:\\OpenCode\\1-integracion-tbf\\codigo\\database\\mock_db.json\" -Name IsReadOnly -Value $false"
    )
    pdf.multi_cell(0, 5, p0_text)
    pdf.ln(4)

    # Paso 1: Levantar FastAPI
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "Paso 1: Levantar el Servidor FastAPI (Backend)", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    p1_text = (
        "Enciende tu servidor de backend para habilitar los endpoints y OpenTelemetry:\n"
        "Comando literal:\n"
        "& \"C:\\OpenCode\\sesion_3\\.venv\\Scripts\\uvicorn.exe\" main:app --reload --host 127.0.0.1 --port 8000 --app-dir \"C:\\OpenCode\\1-integracion-tbf\\codigo\"\n"
        "- Verifica que indique: 'Application startup complete'. Deja esta consola abierta durante toda la demo."
    )
    pdf.multi_cell(0, 5, p1_text)
    
    # ==========================================
    # PÁGINA 2: PASOS 2, 3 & 4
    # ==========================================
    pdf.add_page()

    # Paso 2: Swagger
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "Paso 2: Prueba Interactiva y de Seguridad (Swagger UI)", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    p2_text = (
        "Abre en tu navegador la URL: http://127.0.0.1:8000/docs e ingresa al POST /api/v1/trading/explain.\n"
        "2.1 Demostracion de Bloqueo: Deja la cabecera 'X-API-Key' vacia y presiona Execute. Mostrara error HTTP 401.\n"
        "2.2 Demostracion de Éxito: Ingresa la clave 'trading-secret-key-123' en 'X-API-Key' y presiona Execute.\n"
        "   - Resalta el Enmascaramiento PII: Se dirige al usuario de forma segura como 'M****** G********'.\n"
        "   - Resalta los Calculos: Comisiones (0.5% = $7.50 USD), capital neto de compra y ROI neto del 19.40% calculados de forma exacta en el backend."
    )
    pdf.multi_cell(0, 5, p2_text)
    pdf.ln(4)

    # Paso 3: Observabilidad OTel
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "Paso 3: Observabilidad Tecnica en Consola (OpenTelemetry)", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    p3_text = (
        "Regresa a tu primera consola de PowerShell (Uvicorn). Señala las trazas impresas de forma automatica:\n"
        "- Trazabilidad de Spans: Enseña las lineas '[OTel Span] 'get_asset_price'' e ''simulate_transaction'' "
        "con sus microsegundos parciales de red. Explica que esto te permite diagnosticar cuellos de botella de inmediato.\n"
        "- Correlacion de Logs: Señala el ID unico '[TraceId: ... | SpanId: ...]' inyectado de forma automatica "
        "en cada linea de log tradicional del servidor FastAPI."
    )
    pdf.multi_cell(0, 5, p3_text)
    pdf.ln(4)

    # Paso 4: Falla ACID
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "Paso 4: Prueba de Resiliencia Fisica y Transaccionalidad ACID (Opcion A)", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    p4_text = (
        "1. Bloquear Base de Datos en Windows: Ve al archivo 'mock_db.json' en Windows. Clic derecho -> Propiedades "
        "-> Marca la casilla 'Solo lectura' (Read-only) -> Aceptar.\n"
        "2. Ejecutar consulta: Presiona 'Execute' de nuevo en Swagger.\n"
        "3. Qué señalar: El servidor FastAPI retornara de inmediato un HTTP 503 Service Unavailable detallando "
        "el Permission Error. Explica que el adaptador intercepto el fallo de disco y aborto el proceso antes de "
        "llamar a Gemini, previniendo inconsistencias financieras y ahorrando costes de red en la nube.\n"
        "4. Restauracion: Desmarca la casilla de Solo lectura para continuar."
    )
    pdf.multi_cell(0, 5, p4_text)

    # ==========================================
    # PÁGINA 3: PASOS 5, 6, 7 & 8
    # ==========================================
    pdf.add_page()

    # Paso 5: QA Pytest
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "Paso 5: Aseguramiento de Calidad Offline (Opcion B - Pytest)", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    p5_text = (
        "Abre una segunda consola de PowerShell y ejecuta las 6 pruebas offline asincronas de QA:\n"
        "Comando literal:\n"
        "& \"C:\\OpenCode\\sesion_3\\.venv\\Scripts\\python.exe\" -m pytest \"C:\\OpenCode\\1-integracion-tbf\\codigo\\tests\\test_trading_api.py\" -v\n"
        "- Muestra al docente que todas las aserciones de ruteo, claves y enmascaramiento pasan con exito (6 passed) "
        "en menos de 2 segundos sin costos de API."
    )
    pdf.multi_cell(0, 5, p5_text)
    pdf.ln(4)

    # Paso 6: Benchmark
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "Paso 6: Medidor de Percentiles p50 y p95 (Opcion B - Benchmark)", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    p6_text = (
        "En tu segunda terminal de PowerShell, ejecuta el benchmark secuencial de carga:\n"
        "Comando literal:\n"
        "& \"C:\\OpenCode\\sesion_3\\.venv\\Scripts\\python.exe\" \"C:\\OpenCode\\1-integracion-tbf\\codigo\\scripts\\benchmark_latencia.py\"\n"
        "- Muestra la tabla de percentiles final: p50 (Mediana) de ~20.97 ms y p95 (Peor caso del 5%) de ~28.86 ms, "
        "demostrando un rendimiento asincrono optimo del servidor local."
    )
    pdf.multi_cell(0, 5, p6_text)
    pdf.ln(4)

    # Paso 7: Langfuse
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "Paso 7: Observabilidad de LLM Ops en la Nube (Opcion C - Langfuse)", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    p7_text = (
        "Abre en tu navegador la web https://us.cloud.langfuse.com. Corre estos comandos secuenciales para poblar tu panel:\n"
        "A. Crear Dataset en la nube con los 20 casos de prueba:\n"
        "   & \"C:\\OpenCode\\sesion_3\\.venv\\Scripts\\python.exe\" \"C:\\OpenCode\\1-integracion-tbf\\codigo\\scripts\\create_langfuse_dataset.py\"\n"
        "B. Correr la evaluacion en vivo con Gemini 3.5:\n"
        "   & \"C:\\OpenCode\\sesion_3\\.venv\\Scripts\\python.exe\" \"C:\\OpenCode\\1-integracion-tbf\\codigo\\scripts\\run_langfuse_evaluation.py\"\n"
        "- Dale F5 al navegador y enseña las trazas, costos en USD, tokens e identidades enmascaradas en la pestaña Datasets."
    )
    pdf.multi_cell(0, 5, p7_text)
    pdf.ln(4)

    # Paso 8: DeepEval
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "Paso 8: Evaluacion Cognitiva Avanzada (DeepEval)", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    p8_text = (
        "En tu segunda terminal de PowerShell, ejecuta la prueba cognitiva asertiva con tu Juez Gemini:\n"
        "Comando literal (incluyendo el flag -s para ver el reporte de deepeval en consola):\n"
        "& \"C:\\OpenCode\\sesion_3\\.venv\\Scripts\\python.exe\" -m pytest \"C:\\OpenCode\\1-integracion-tbf\\codigo\\tests\\test_deepeval_agent.py\" -v -s\n"
        "- Señala en pantalla la scorecard cognitiva interactiva y el razonamiento del Juez Gemini evaluando la relevancia."
    )
    pdf.multi_cell(0, 5, p8_text)
    pdf.ln(5)
    
    # Cierre
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(0, 10, "Manual de Sustentacion Paso a Paso - Marcelo Gilardoni | Solutions Architect & SRE.", 0, 1, "C")
    
    # Escribir PDF final
    target_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "doc", "paso_a_paso.pdf")
    pdf.output(target_path)
    print(f"Reporte paso a paso PDF generado exitosamente en: {target_path}")

if __name__ == "__main__":
    create_pdf()
