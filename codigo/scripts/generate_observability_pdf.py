import os
import sys
from fpdf import FPDF

# Asegurar existencia de la carpeta doc
os.makedirs(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "doc"), exist_ok=True)

class ObsPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 8)
        self.set_text_color(160, 160, 160)
        self.cell(0, 10, 'REPORTE TÉCNICO DE OBSERVABILIDAD - TRABAJO FINAL', 0, 1, 'R')
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(160, 160, 160)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def create_pdf():
    pdf = ObsPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Titulo Principal
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(30, 41, 59) # Slate 800
    pdf.cell(0, 12, "OBSERVABILIDAD CON OPENTELEMETRY", 0, 1, "C")
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(79, 70, 229) # Indigo 600
    pdf.cell(0, 6, "SISTEMA DE DIAGNÓSTICO EMPRESARIAL PARA DETECCIÓN DE ERRORES Y LATENCIAS", 0, 1, "C")
    pdf.ln(8)
    
    # Seccion 1: Por que OpenTelemetry?
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "1. ¿Por que implementar OpenTelemetry (OTel)?", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    p1_text = (
        "En un sistema distribuido que integra multiples sistemas externos (como la API de precios de CoinGecko "
        "y el motor de IA de Google Gemini 3.5), la observabilidad es vital. El estandar OpenTelemetry nos permite "
        "rastrear con precision de milisegundos que paso con una consulta, en que momento ocurrio y, en caso de fallas, "
        "determinar la causa raiz de forma automatica y cientifica, evitando conjeturas."
    )
    pdf.multi_cell(0, 5, p1_text)
    pdf.ln(4)
    
    # Seccion 2: Los Tres Pilares de la Observabilidad Implementados
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "2. Los Pilares de la Observabilidad Implementados", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(0, 5, "- Pilar 1: Monitoreo por Spans (Trazabilidad)", 0, 1, "L")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    pdf.multi_cell(0, 5, "Creamos spans aislados para auditar de forma independiente cada capa del sistema: 'get_asset_price' para el conector, 'simulate_transaction' para el adaptador y 'run_query' para el motor de Gemini. Esto aisla y visualiza los cuellos de botella de red de inmediato.")
    pdf.ln(2)
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(0, 5, "- Pilar 2: Correlacion de Logs (Trace ID & Span ID)", 0, 1, "L")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    pdf.multi_cell(0, 5, "Inyectamos de forma dinamica el TraceId y SpanId unico de OpenTelemetry dentro del formateador de logs de FastAPI. De este modo, si se procesan 10,000 peticiones en paralelo, podemos rastrear y filtrar todas las lineas de log de un usuario especifico con un solo clic.")
    pdf.ln(2)
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(0, 5, "- Pilar 3: Registro y Deteccion de Fallas (Error Handling)", 0, 1, "L")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    pdf.multi_cell(0, 5, "Si un sistema externo falla (como el rate-limit 429 de Gemini o errores 404 de CoinGecko), el Span correspondiente se marca automaticamente con estatus 'ERROR' y adjunta metadatos del error. El middleware previene la caida del sistema y activa el fallback de manera segura.")
    pdf.ln(4)

    # Seccion 3: Ejemplo de Registro de Trazas
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "3. Ejemplo de Trazas impresas en Consola", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    
    pdf.set_font("Courier", "", 8.5)
    pdf.set_text_color(51, 65, 85)
    code_text = (
        "[OTel Span] 'get_asset_price' | Parent: 0x93ef... | Status: StatusCode.OK | Duration: 15.42ms\n"
        "[OTel Span] 'simulate_transaction' | Parent: 0xbfd7... | Status: StatusCode.OK | Duration: 23.10ms\n"
        "[OTel Span] 'run_query' | Parent: 0x00f0... | Status: StatusCode.OK | Duration: 1120.40ms\n"
    )
    pdf.multi_cell(0, 4.5, code_text)
    pdf.ln(4)
    
    # Seccion 4: Comandos para la demostracion
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "4. Como Demostrar la Observabilidad en Vivo", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    p4_text = (
        "- Demostracion 1 (Desglose de Spans): Al realizar una consulta, la consola de FastAPI imprimira "
        "automaticamente las duraciones parciales de cada capa en formato OTel Span, visualizando la rapidez "
        "de tus de algoritmos locales.\n\n"
        "- Demostracion 2 (Correlacion): Muestra las lineas de log del servidor. Resalta que cada registro "
        "posee la cabecera correlacionada [TraceId: ... | SpanId: ...] inyectada por tu middleware de OTel.\n\n"
        "- Demostracion 3 (Errores): Ejecuta una llamada con un activo inexistente (como 'XYZ') y observa "
        "como el Span se marca con estado 'ERROR' capturando la excepcion de forma autonoma sin que caiga la API.\n\n"
        "- Demostracion 4 (Fallo de BD): Bloquea 'mock_db.json' como 'Solo Lectura'. Observa cómo OTel registra la "
        "excepción de disco 'PermissionError' y el adaptador aborta la llamada a Gemini, previniendo inconsistencias."
    )
    pdf.multi_cell(0, 5, p4_text)
    pdf.ln(5)
    
    # Cierre
    pdf.set_font("Helvetica", "I", 9.5)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(0, 10, "Documento de observabilidad corporativa - BSG Institute, Estrategias de Integracion.", 0, 1, "C")
    
    # Escribir PDF final
    target_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "doc", "observabilidad_proyecto.pdf")
    pdf.output(target_path)
    print(f"Reporte de observabilidad PDF generado exitosamente en: {target_path}")

if __name__ == "__main__":
    create_pdf()
