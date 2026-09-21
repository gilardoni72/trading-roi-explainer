import os
import sys
from fpdf import FPDF

# Asegurar existencia de la carpeta doc
os.makedirs(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "doc"), exist_ok=True)

class LangfuseGuidePDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 8)
        self.set_text_color(160, 160, 160)
        self.cell(0, 10, 'GUÍA DE OBSERVABILIDAD EN LA NUBE (PASO 7 - OPCIÓN C) - MARCELO GILARDONI', 0, 1, 'R')
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(160, 160, 160)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def create_pdf():
    pdf = LangfuseGuidePDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Titulo Principal
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(30, 41, 59) # Slate 800
    pdf.cell(0, 12, "PASO 7: OBSERVABILIDAD DE LLM OPS EN LA NUBE", 0, 1, "C")
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(79, 70, 229) # Indigo 600
    pdf.cell(0, 6, "INTEGRACIÓN PASO A PASO CON LANGFUSE CLOUD (MARCELO GILARDONI)", 0, 1, "C")
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
        "Este manual describe los 4 pasos exactos de ejecucion e indicaciones tecnicas para realizar la "
        "prueba de Observabilidad Cognitiva en la nube con Langfuse Cloud durante tu sustentacion. "
        "Permite auditar costos en USD, tokens, prompts e identidades enmascaradas frente al docente."
    )
    pdf.multi_cell(0, 5, intro_text)
    pdf.ln(5)

    # Requisito de Claves
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "Requisito Previo obligatorio: Enlace de Credenciales", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    req_text = (
        "Para que tu servidor FastAPI local se comunique de forma segura con la nube de Langfuse:\n"
        "1. Inicia sesion en us.cloud.langfuse.com y ve a Settings -> API Credentials.\n"
        "2. Crea nuevas llaves y guardalas de forma local en tu archivo 'codigo/.env' (ignorado por Git):\n"
        "   LANGFUSE_PUBLIC_KEY=\"pk-lf-...\"\n"
        "   LANGFUSE_SECRET_KEY=\"sk-lf-...\"\n"
        "   LANGFUSE_HOST=\"https://us.cloud.langfuse.com\""
    )
    pdf.multi_cell(0, 5, req_text)
    pdf.ln(5)

    # LOS 4 PASOS EN VIVO
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "Secuencia de Ejecucion en Vivo (4 Pasos)", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)

    steps = [
        ("Paso 1: Crear el Dataset de 20 casos de prueba en la Nube",
         "Ejecuta en PowerShell el script poblador de datasets:\n"
         "Comando: python codigo/scripts/create_langfuse_dataset.py\n"
         "- Que señalar: En el navegador, actualiza y muestra en la pestaña 'Datasets' el dataset "
         "'trading_agent_evaluation' con tus 20 casos de prueba creados de forma instantanea."),
         
        ("Paso 2: Ejecutar la Corrida de Evaluacion en Vivo (con Gemini 3.5)",
         "Ejecuta en PowerShell la evaluacion cognitiva automatica de los 20 casos:\n"
         "Comando: python codigo/scripts/run_langfuse_evaluation.py\n"
         "- Que señalar: Tu agente procesara cada caso de forma real, enmascarara las identidades a "
         "M**** G**** y enviara las metricas de trazas, costos y respuestas a Langfuse Cloud."),
         
        ("Paso 3: Mostrar las Trazas Individuales (Tracing)",
         "Ve a la pestaña 'Tracing' en tu navegador de Langfuse y selecciona una consulta exitosa:\n"
         "- Enmascaramiento: Señala que el User ID registrado es 'M**** G****', protegiendo la privacidad (PII).\n"
         "- Costos y Tokens: Señala en la tarjeta 'Model costs' el costo calculado en USD y los tokens consumidos."),
         
        ("Paso 4: El Dashboard Ejecutivo Consolidado (Métricas de Gerencia)",
         "Haz clic en la pestaña 'Dashboards' o 'Home' en Langfuse Cloud:\n"
         "- Enseña los graficos interactivos auto-generados que consolidan tu uso de Gemini 3.5:\n"
         "   * Model Cost (Costos totales acumulados en dolares).\n"
         "   * Total Traces (Volumen total de transacciones simuladas).\n"
         "   * Model Usage (Distribucion de tokens y llamadas por modelo).\n"
         "   * Latency averages (Historia de velocidad y rendimiento de tu API).")
    ]

    for title, desc in steps:
        pdf.set_font("Helvetica", "B", 10.5)
        pdf.set_text_color(51, 65, 85)
        pdf.cell(0, 5, title, 0, 1, "L")
        pdf.set_font("Helvetica", "", 9.5)
        pdf.set_text_color(100, 116, 139)
        pdf.multi_cell(0, 4.5, desc)
        pdf.ln(3)

    # Cierre
    pdf.set_font("Helvetica", "I", 9.5)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(0, 10, "Guía de Observabilidad en la Nube - Marcelo Gilardoni | Solutions Architect & SRE.", 0, 1, "C")
    
    # Escribir PDF final
    target_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "doc", "paso_7_langfuse_paso_a_paso.pdf")
    pdf.output(target_path)
    print(f"Guía de Langfuse en PDF generada exitosamente en: {target_path}")

if __name__ == "__main__":
    create_pdf()
