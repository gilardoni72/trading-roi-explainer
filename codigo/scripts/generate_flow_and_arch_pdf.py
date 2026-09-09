import os
import sys
from fpdf import FPDF

# Asegurar existencia de la carpeta doc
os.makedirs(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "doc"), exist_ok=True)

class FlowPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 8)
        self.set_text_color(160, 160, 160)
        self.cell(0, 10, 'REPORTE TÉCNICO COMPLEMENTARIO - TRABAJO FINAL', 0, 1, 'R')
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(160, 160, 160)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def create_pdf():
    pdf = FlowPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # --- PÁGINA 1: FLUJO DE DATOS EN DETALLE ---
    pdf.add_page()
    
    # Titulo Principal
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(30, 41, 59) # Slate 800
    pdf.cell(0, 12, "FLUJO DE DATOS EN DETALLE", 0, 1, "C")
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(79, 70, 229) # Indigo 600
    pdf.cell(0, 6, "CICLO DE VIDA COMPLETO DE UNA CONSULTA (EJEMPLO EN VIVO)", 0, 1, "C")
    pdf.ln(8)
    
    # Descripcion
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    intro = (
        "Para garantizar la seguridad, el enmascaramiento de informacion sensible y la precision financiera, "
        "cada llamada realizada a la API sigue un ciclo de vida riguroso dividido en 7 fases consecutivas."
    )
    pdf.multi_cell(0, 5, intro)
    pdf.ln(5)
    
    # Pasos del Flujo
    steps = [
        ("Fase 1: Entrada de la Solicitud (Cliente)", 
         "El usuario envia una peticion HTTP POST al endpoint o ejecuta el comando CLI con el mensaje: "
         "'Tengo $1500 USD que me sobraron de mi sueldo y quiero invertir en BTC si llega a $80000', "
         "declarando su nombre real 'Maria Gomez' (PII sensible) y adjuntando la cabecera 'X-API-Key'."),
        
        ("Fase 2: Filtro de Seguridad Perimetral", 
         "FastAPI captura la peticion y activa la validacion de la cabecera 'X-API-Key'. Si es ausente o incorrecta, "
         "retorna inmediatamente un codigo HTTP 401 Unauthorized, cortando la llamada antes de consumir recursos. "
         "A la par, se inicia el temporizador de alta precision para medir la latencia del procesamiento."),
        
        ("Fase 3: Adaptacion de Datos y Enmascaramiento PII", 
         "El Adaptador Financiero procesa la entrada de manera automatica: "
         "1. Anonimiza el nombre real del usuario enmascarandolo de forma estricta: 'Maria Gomez' -> 'M**** G****'. "
         "2. Extrae exclusivamente los parametros de trading: activo='BTC', monto=1500.0, precio_meta=80000.0, "
         "eliminando textos libres y referencias personales para prevenir ataques de prompt injection."),
        
        ("Fase 4: Conexion Asincrona Externa (Market Price Connector)", 
         "El conector asincrono llama a la API de CoinGecko o al simulador determinista local offline (Modo Demo) "
         "para obtener el precio de cotizacion actual de Bitcoin en tiempo real (ejemplo: $77,417.00 USD)."),
        
        ("Fase 5: Calculos Financieros Cuantitativos", 
         "El adaptador ejecuta la logica matematica: deduce la comision fija de trading (0.5% = $7.50 USD), "
         "calcula la tenencia neta adquirida (0.019279 BTC), proyecta el retorno al precio objetivo ($1,542.30 USD) "
         "y computa el Retorno de Inversion (ROI Neto) resultante (2.82%). Guarda esta bitacora en mock_db.json."),
        
        ("Fase 6: Explicacion Inteligente con Gemini 3.5", 
         "Los calculos y el identificador enmascarado son empaquetados en un prompt estructurado y enviados a Gemini 3.5. "
         "El modelo (con o sin streaming) redacta un informe analitico y amigable en espanol con pautas de gestion de riesgo."),
        
        ("Fase 7: Retorno de la Respuesta y Registro de Latencias", 
         "FastAPI detiene el temporizador, calcula la latencia (ms) de la ejecucion, la inyecta en la cabecera "
         "HTTP 'X-Process-Time' y entrega el reporte final sanitizado y seguro al cliente.")
    ]
    
    for title, text in steps:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(51, 65, 85)
        pdf.cell(0, 5, title, 0, 1, "L")
        pdf.set_font("Helvetica", "", 9.5)
        pdf.set_text_color(100, 116, 139)
        pdf.multi_cell(0, 4.5, text)
        pdf.ln(3)

    # --- PÁGINA 2: IMAGEN DE LA ARQUITECTURA ---
    pdf.add_page()
    
    # Titulo Pagina 2
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 12, "DIAGRAMA DE ARQUITECTURA DE INTEGRACION", 0, 1, "C")
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(79, 70, 229)
    pdf.cell(0, 6, "CAPAS, FLUJOS DE CONTROL Y COMPONENTES TECNOLOGICOS", 0, 1, "C")
    pdf.ln(10)
    
    # Ruta de la imagen de la arquitectura
    img_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "doc", "arquitectura_integracion.png")
    
    if os.path.exists(img_path):
        # Insertar imagen centrada: A4 es 210 de ancho, margen de 10 a cada lado -> ancho disponible 190.
        # Aspect ratio de la imagen original es 1200/800 = 1.5. Ancho de 190 -> Alto de 190/1.5 = 126.6.
        pdf.image(img_path, x=10, y=pdf.get_y(), w=190, h=126.6)
        pdf.ln(135) # Espaciado despues de la imagen
    else:
        pdf.set_font("Helvetica", "I", 10)
        pdf.set_text_color(220, 38, 38)
        pdf.cell(0, 10, "Error: No se pudo localizar la imagen de arquitectura_integracion.png para embeber.", 0, 1, "C")
        pdf.ln(5)

    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(100, 116, 139)
    pdf.multi_cell(0, 4.5, (
        "El diagrama superior ilustra la orquestacion desacoplada del sistema. Cada llamada transita obligatoriamente "
        "desde el Cliente REST o CLI a traves de los filtros perimetrales y adaptadores antes de consumir la API "
        "de precios externos y la logica de lenguaje natural de Google Gemini 3.5."
    ))
    
    # Escribir PDF final
    target_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "doc", "flujo_datos_y_arquitectura.pdf")
    pdf.output(target_path)
    print(f"Reporte de flujo y arquitectura en PDF generado exitosamente en: {target_path}")

if __name__ == "__main__":
    create_pdf()
