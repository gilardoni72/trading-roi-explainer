import os
import sys
from fpdf import FPDF

# Asegurar que el directorio de doc exista
os.makedirs(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "doc"), exist_ok=True)

class ProjectPDF(FPDF):
    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 10)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, 'BSG INSTITUTE - ESTRATEGIAS DE INTEGRACIÓN | PROYECTO FINAL', 0, 1, 'R')
        self.ln(2)

    def footer(self):
        # Posicionar a 1.5 cm del final
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(150, 150, 150)
        # Numero de pagina
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def build_pdf():
    pdf = ProjectPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Titulo Principal
    pdf.set_font("Arial", "B", 18)
    pdf.set_text_color(30, 41, 59) # Slate 800
    pdf.cell(0, 12, "TRADING ROI EXPLAINER & SIMULATOR API", 0, 1, "C")
    
    pdf.set_font("Arial", "B", 11)
    pdf.set_text_color(79, 70, 229) # Indigo 600
    pdf.cell(0, 6, "PLAN DE INTEGRACIÓN ARQUITECTÓNICA Y SOLUCIÓN FINAL", 0, 1, "C")
    pdf.ln(8)
    
    # Seccion 1: Resumen Ejecutivo
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "1. Resumen del Caso de Uso", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(75, 85, 99) # Gray 600
    text_resumen = (
        "Este proyecto final de integracion implementa una API de Trading de criptoactivos (BTC, ETH, SOL) "
        "con simulacion de retornos de inversion (ROI) y comisiones de mercado en tiempo real. "
        "El servicio une una capa REST asincrona de alto desempeno con un Agente de Inteligencia Artificial (LLM) "
        "reforzado contra la alucinacion de datos a traves del patron Connector-Adapter con herramientas reales."
    )
    pdf.multi_cell(0, 5, text_resumen)
    pdf.ln(4)
    
    # Seccion 2: Arquitectura del Sistema
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "2. Arquitectura de Integracion por Capas", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    
    pdf.set_font("Arial", "B", 10)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(0, 5, "- CAPA 1: Interfaz de Consumo (FastAPI REST)", 0, 1, "L")
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(75, 85, 99)
    pdf.multi_cell(0, 5, "Expone el endpoint protegido '/api/v1/trading/explain'. Recibe solicitudes tipadas por Pydantic y un middleware mide de manera exacta los tiempos de ejecucion (duracion_ms) de cada request.")
    pdf.ln(2)
    
    pdf.set_font("Arial", "B", 10)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(0, 5, "- CAPA 2: Conector (Market Price Connector)", 0, 1, "L")
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(75, 85, 99)
    pdf.multi_cell(0, 5, "Modulo asincrono de integracion externa. En modo real, consume la API publica de precios de CoinGecko de forma asincrona con httpx. En modo offline (Demo Mode), genera precios realistas de manera determinista utilizando mocks locales.")
    pdf.ln(2)
    
    pdf.set_font("Arial", "B", 10)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(0, 5, "- CAPA 3: Adaptador (Trading Adapter)", 0, 1, "L")
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(75, 85, 99)
    pdf.multi_cell(0, 5, "Aplica logica de negocio sobre los datos crudos del conector. Deduce de forma estricta las comisiones transaccionales fijas (0.5%) del broker, calcula la cantidad neta del activo comprado, el retorno proyectado en USD y el ROI porcentual.")
    pdf.ln(2)
    
    pdf.set_font("Arial", "B", 10)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(0, 5, "- CAPA 4: Agente LLM (LangChain)", 0, 1, "L")
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(75, 85, 99)
    pdf.multi_cell(0, 5, "Orquesta el flujo cognitivo. El LLM (gpt-4o-mini o simulador de demo) recibe unicamente parametros ya limpios y desprovistos de PII. Tiene herramientas mapeadas para resolver dudas y generar el reporte analitico final en formato amigable.")
    pdf.ln(4)

    # Seccion 3: Seguridad y Enmascaramiento
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "3. Seguridad, Proteccion de Datos y Enmascaramiento", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(75, 85, 99)
    text_seguridad = (
        "1. Endpoint Cerrado con Clave (Autenticacion):\n"
        "Se implemento una validacion estricta mediante FastAPI Dependencies. Todas las llamadas al endpoint "
        "exigen la cabecera 'X-API-Key'. Si el token es ausente o invalido, el sistema retorna inmediatamente "
        "un error HTTP 401 Unauthorized, impidiendo llamadas no autorizadas.\n\n"
        "2. Proteccion de Datos Personales (Enmascaramiento):\n"
        "Para cumplir con estandares de privacidad financiera (PII), el Adaptador ejecuta de manera automatica "
        "un enmascaramiento de nombres e identificadores de usuario (ejemplo: 'Maria Gomez' se convierte en "
        "'M**** G****') antes de registrar la operacion en base de datos o enviarla al LLM. Ademas, el sistema "
        "extrae de forma estricta unicamente los parametros numericos claves (activo, monto, precio meta), de "
        "modo que ningun texto libre o datos personales sensibles del usuario sean transferidos al LLM externo."
    )
    pdf.multi_cell(0, 5, text_seguridad)
    pdf.ln(6)
    
    # Seccion 4: Checklist y Resultados de Medicion (p50, p95)
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "4. Resultados del Control y Checklist", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(75, 85, 99)
    text_resultados = (
        "- Endpoint Protegido: /api/v1/trading/explain (Cabecera X-API-Key obligatoria).\n"
        "- Pruebas de Vias: Sin cabecera devuelve 401. Con cabecera correcta devuelve 200.\n"
        "- Logica de Enmascaramiento: Activa para nombres y extraccion parametrica.\n"
        "- Suite de Tests: 6 pruebas unitarias exitosas cubriendo salud, autenticacion, validaciones y alias.\n"
        "- Script de Medicion: Desarrollado en python, ejecutando 10 peticiones secuenciales consecutivas.\n"
    )
    pdf.multi_cell(0, 5, text_resultados)
    pdf.ln(6)
    
    # Firma y Cierre
    pdf.set_font("Arial", "I", 10)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 10, "Documento generado para evaluacion de la clase - BSG Institute, Curso de Estrategias de Integracion.", 0, 1, "C")
    
    # Escribir el archivo final
    target_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "doc", "proyecto_integracion_trading_roi.pdf")
    pdf.output(target_path)
    print(f"Documentacion PDF generada con exito en: {target_path}")

if __name__ == "__main__":
    build_pdf()
