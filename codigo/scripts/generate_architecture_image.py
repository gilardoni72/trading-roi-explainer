import os
from PIL import Image, ImageDraw, ImageFont

def draw_rounded_rectangle(draw, x1, y1, x2, y2, radius, fill, outline=None, width=1):
    draw.rounded_rectangle([(x1, y1), (x2, y2)], radius, fill=fill, outline=outline, width=width)

def generate_image():
    # Dimensiones de la imagen
    width, height = 1200, 800
    image = Image.new("RGB", (width, height), "#0F172A") # Slate 900 (Fondo oscuro moderno)
    draw = ImageDraw.Draw(image)
    
    # Intentar cargar una fuente por defecto del sistema
    try:
        title_font = ImageFont.truetype("arial.ttf", 28)
        subtitle_font = ImageFont.truetype("arial.ttf", 18)
        body_font = ImageFont.truetype("arial.ttf", 14)
        bold_font = ImageFont.truetype("arial.ttf", 15)
        code_font = ImageFont.truetype("cour.ttf", 13)
    except IOError:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
        bold_font = ImageFont.load_default()
        code_font = ImageFont.load_default()

    # --- TITULO PRINCIPAL ---
    draw.text((width // 2, 40), "ARQUITECTURA DE INTEGRACIÓN POR CAPAS", fill="#F8FAFC", font=title_font, anchor="mm")
    draw.text((width // 2, 75), "TRADING ROI EXPLAINER & TRANSACTION SIMULATOR API (GEMINI 3.5)", fill="#818CF8", font=subtitle_font, anchor="mm")
    draw.line([(50, 100), (width - 50, 100)], fill="#334155", width=2)
    
    # --- DIBUJAR CAJAS DE CAPAS (BLOQUES) ---

    # 1. Cliente / Consumo
    draw_rounded_rectangle(draw, 450, 130, 750, 200, 10, fill="#1E293B", outline="#475569", width=2)
    draw.text((600, 150), "CLIENTE REST / INTERFAZ CLI", fill="#38BDF8", font=bold_font, anchor="mm")
    draw.text((600, 175), "Peticiones HTTP o Comando '--stream'", fill="#94A3B8", font=body_font, anchor="mm")

    # Flecha 1
    draw.line([(600, 200), (600, 240)], fill="#818CF8", width=3)
    draw.polygon([(595, 235), (605, 235), (600, 243)], fill="#818CF8")

    # 2. Capa 1: FastAPI
    draw_rounded_rectangle(draw, 250, 240, 950, 340, 10, fill="#1E1B4B", outline="#4F46E5", width=2)
    draw.text((600, 265), "CAPA 1: INTERFAZ DE CONSUMO & AUTENTICACIÓN (FastAPI)", fill="#818CF8", font=bold_font, anchor="mm")
    draw.text((600, 290), "Verificación X-API-Key (HTTP 401 si falla / 200 OK si coincide)", fill="#C7D2FE", font=body_font, anchor="mm")
    draw.text((600, 315), "middleware: log_process_time() -> Medición exacta de latencia (p50 / p95)", fill="#94A3B8", font=body_font, anchor="mm")

    # Flecha 2
    draw.line([(600, 340), (600, 380)], fill="#818CF8", width=3)
    draw.polygon([(595, 375), (605, 375), (600, 383)], fill="#818CF8")

    # 3. Capa 3: Adaptador
    draw_rounded_rectangle(draw, 250, 380, 950, 480, 10, fill="#022C22", outline="#059669", width=2)
    draw.text((600, 405), "CAPA 3: ADAPTADOR DE NEGOCIO (Trading Adapter)", fill="#34D399", font=bold_font, anchor="mm")
    draw.text((600, 430), "Enmascaramiento PII ('Maria Gomez' -> 'M**** G****') | Extracción Estricta de Parámetros", fill="#A7F3D0", font=body_font, anchor="mm")
    draw.text((600, 455), "Cálculos de Trading: Deducción de Comisión del 0.5%, Compra Neta, Retornos y ROI (%)", fill="#94A3B8", font=body_font, anchor="mm")

    # Flechas divididas desde el Adaptador (hacia Conector e IA)
    # Flecha Izquierda (al Conector)
    draw.line([(400, 480), (400, 520)], fill="#34D399", width=3)
    draw.polygon([(395, 515), (405, 515), (400, 523)], fill="#34D399")
    
    # Flecha Derecha (a Gemini)
    draw.line([(800, 480), (800, 520)], fill="#34D399", width=3)
    draw.polygon([(795, 515), (805, 515), (800, 523)], fill="#34D399")

    # 4. Capa 2: Conector (Izquierda)
    draw_rounded_rectangle(draw, 100, 520, 520, 610, 10, fill="#1C1917", outline="#D97706", width=2)
    draw.text((310, 545), "CAPA 2: CONECTOR (Market Price)", fill="#F59E0B", font=bold_font, anchor="mm")
    draw.text((310, 570), "Modo Real: Cliente httpx asíncrono -> CoinGecko API", fill="#FDE68A", font=body_font, anchor="mm")
    draw.text((310, 590), "Modo Demo: Simulador local determinista offline", fill="#94A3B8", font=body_font, anchor="mm")

    # Retorno de precio al Adaptador (Flecha de vuelta)
    draw.line([(310, 520), (310, 480)], fill="#F59E0B", width=2)
    draw.polygon([(305, 485), (315, 485), (310, 477)], fill="#F59E0B")

    # 5. Capa 4: Gemini (Derecha)
    draw_rounded_rectangle(draw, 680, 520, 1100, 610, 10, fill="#1E1E38", outline="#6366F1", width=2)
    draw.text((890, 545), "CAPA 4: MOTOR DE IA (Gemini 3.5 Flash)", fill="#818CF8", font=bold_font, anchor="mm")
    draw.text((890, 570), "No Streaming: generateContent (Bloque completo)", fill="#C7D2FE", font=body_font, anchor="mm")
    draw.text((890, 590), "Streaming: streamGenerateContent (Tokens en vivo)", fill="#94A3B8", font=body_font, anchor="mm")

    # 6. Almacenamiento Local (Abajo del todo)
    draw_rounded_rectangle(draw, 350, 670, 850, 750, 10, fill="#0F172A", outline="#64748B", width=2)
    draw.text((600, 695), "ALMACENAMIENTO DE DATOS LOCALES (JSON DB)", fill="#94A3B8", font=bold_font, anchor="mm")
    draw.text((600, 715), "database/mock_db.json | database/benchmark_results.json (p50 / p95)", fill="#64748B", font=code_font, anchor="mm")

    # Conectar Adaptador con Almacenamiento (Flecha larga)
    draw.line([(600, 480), (600, 670)], fill="#64748B", width=2)
    draw.polygon([(595, 665), (605, 665), (600, 673)], fill="#64748B")

    # Guardar la imagen final
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "doc")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "arquitectura_integracion.png")
    image.save(output_path)
    print(f"Imagen de arquitectura generada y guardada con éxito en: {output_path}")

if __name__ == "__main__":
    generate_image()
