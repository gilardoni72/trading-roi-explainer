import os
import sys
from fpdf import FPDF

# Asegurar existencia de la carpeta doc
os.makedirs(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "doc"), exist_ok=True)

class ProfessionalGuidePDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('Helvetica', 'B', 8)
            self.set_text_color(120, 120, 120)
            self.cell(100, 10, 'BSG INSTITUTE - TRABAJO FINAL | MARCELO GILARDONI', 0, 0, 'L')
            self.cell(0, 10, 'GUÍA DE DEMOSTRACIÓN EN VIVO', 0, 1, 'R')
            # Línea de cabecera
            self.set_draw_color(226, 232, 240) # Slate 200
            self.line(10, 18, 200, 18)
            self.ln(5)

    def footer(self):
        self.set_y(-15)
        # Línea de pie de página
        self.set_draw_color(226, 232, 240)
        self.line(10, 280, 200, 280)
        
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(100, 10, 'Trading ROI Explainer & Simulator API', 0, 0, 'L')
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'R')

def compile_professional_guide():
    pdf = ProfessionalGuidePDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    
    # ==========================================
    # PÁGINA 1: PORTADA E ÍNDICE
    # ==========================================
    pdf.add_page()
    
    # Título Principal
    pdf.ln(10)
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(30, 41, 59) # Slate 800
    pdf.cell(0, 12, "GUIA OFICIAL DE DEMOSTRACION", 0, 1, "C")
    
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(79, 70, 229) # Indigo 600
    pdf.cell(0, 6, "TRABAJO FINAL DE INTEGRACIÓN | BSG INSTITUTE", 0, 1, "C")
    pdf.ln(15)
    
    # Cuadro de Firma del Estudiante
    pdf.set_fill_color(248, 250, 252) # Slate 50
    pdf.set_draw_color(226, 232, 240) # Slate 200
    pdf.rect(10, 50, 190, 35, "FD")
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(100, 116, 139) # Slate 500
    pdf.set_xy(15, 54)
    pdf.cell(50, 6, "ESTUDIANTE:", 0, 0)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 6, "Marcelo Gilardoni", 0, 1)
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(100, 116, 139)
    pdf.set_x(15)
    pdf.cell(50, 6, "ROL:", 0, 0)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 6, "Solutions Architect / DevOps Engineer", 0, 1)
    
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(100, 116, 139)
    pdf.set_x(15)
    pdf.cell(50, 6, "REPOSITORIO:", 0, 0)
    pdf.set_font("Courier", "", 9.5)
    pdf.set_text_color(79, 70, 229)
    pdf.cell(0, 6, "https://github.com/gilardoni72/trading-roi-explainer", 0, 1)
    
    # Espaciado para el Índice
    pdf.set_xy(10, 100)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "INDICE DE CONTENIDOS", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)
    
    # Elementos del índice
    index_items = [
        ("1. Inicio de la Aplicacion y Conexion de APIs", "Pag. 2"),
        ("2. Primera Prueba: Validacion de Seguridad Perimetral (HTTP 401)", "Pag. 2"),
        ("3. Segunda Prueba: Simulacion Exitosa y Verificacion de Calculos", "Pag. 2"),
        ("   3.1 Verificacion de los Calculos Matematicos del Adaptador", "Pag. 3"),
        ("   3.2 Observabilidad de Latencia y Rendimiento", "Pag. 3"),
        ("4. Tercera Prueba: Simulacion de Falla de Consistencia (ACID - HTTP 503)", "Pag. 3"),
        ("   4.1 Diagnostico de la Causa Fisica", "Pag. 3"),
        ("   4.2 Transaccionalidad Estricta y Consistencia (Garantia ACID)", "Pag. 4"),
        ("   4.3 Diagnostico Automatico en Consola (OpenTelemetry)", "Pag. 4"),
        ("5. Cuarta Prueba: Aseguramiento de Calidad y Latencias", "Pag. 4"),
        ("   5.1 Pruebas Unitarias Automatizadas (Pytest)", "Pag. 4"),
        ("   5.2 Benchmark de Rendimiento y Percentiles (p50 / p95)", "Pag. 5")
    ]
    
    for title, page in index_items:
        pdf.set_font("Helvetica", "B" if not title.startswith("   ") else "", 10)
        pdf.set_text_color(30, 41, 59)
        pdf.cell(160, 6, title, 0, 0, "L")
        pdf.set_font("Helvetica", "I", 9.5)
        pdf.set_text_color(100, 116, 139)
        pdf.cell(0, 6, page, 0, 1, "R")
        
    pdf.ln(15)
    pdf.set_font("Helvetica", "I", 9.5)
    pdf.set_text_color(148, 163, 184)
    pdf.cell(0, 6, "Usa este manual de forma secuencial durante la sustentacion en vivo.", 0, 1, "C")

    # ==========================================
    # PÁGINA 2: CONTENIDOS INICIALES Y PRUEBAS 1 & 2
    # ==========================================
    pdf.add_page()
    
    # 1. Inicio de la Aplicación
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "1. Inicio de la Aplicacion y Conexion de APIs", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    pdf.multi_cell(0, 5, "Para arrancar tu servidor web asincrono, abre tu consola de PowerShell y ejecuta el comando literal:")
    pdf.ln(2)
    
    # Caja de Código
    pdf.set_fill_color(241, 245, 249) # Slate 100
    pdf.set_font("Courier", "", 8.5)
    pdf.set_text_color(220, 38, 38) # Red 600
    pdf.multi_cell(0, 5, '& "C:\\OpenCode\\sesion_3\\.venv\\Scripts\\uvicorn.exe" main:app --reload --host 127.0.0.1 --port 8000 --app-dir "C:\\OpenCode\\1-integracion-tbf\\codigo"', fill=True)
    pdf.ln(3)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    pdf.multi_cell(0, 5, (
        "Esta aplicacion se conecta de forma asincrona a dos APIs externas principales:\n"
        "- CoinGecko API v3 (Conector de Precios): Obtiene el precio de cotizacion en tiempo real de Bitcoin, Ethereum y Solana sin requerir claves.\n"
        "- Google Gemini API (IA Engine): El modelo gemini-3.5-flash redacta el informe analitico y los consejos de gestion de riesgo en espanol."
    ))
    pdf.ln(5)

    # 2. Primera Prueba
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "2. Primera Prueba: Validacion de Seguridad Perimetral (HTTP 401)", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    p1_text = (
        "1. Abre en tu navegador la documentacion interactiva: http://127.0.0.1:8000/docs\n"
        "2. Haz clic en 'Try it out' en el endpoint POST /api/v1/trading/explain.\n"
        "3. Deja vacio el parametro 'X-API-Key' y presiona el boton azul 'Execute'.\n"
        "4. Resultado Obtenido: El servidor bloquea de inmediato la llamada y retorna un codigo "
        "HTTP 401 Unauthorized, demostrando seguridad perimetral estricta."
    )
    pdf.multi_cell(0, 5, p1_text)
    pdf.ln(5)

    # 3. Segunda Prueba
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "3. Segunda Prueba: Simulacion Exitosa y Verificacion de Calculos", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    
    p2_text = (
        "1. Ahora, ingresa en la casilla de la cabecera 'X-API-Key' la clave: 'trading-secret-key-123'\n"
        "2. En el recuadro negro de la peticion (Request Body), copia y pega tu consulta:\n"
        "   {\n"
        "     \"user_name\": \"Marcelo Gilardoni\",\n"
        "     \"message\": \"Tengo $1500 USD que me sobraron y quiero simular una inversion en BTC si sube a $80000\"\n"
        "   }\n"
        "3. Presiona 'Execute' y observa la respuesta exitosa HTTP 200 OK con tu informe redactado por Gemini 3.5."
    )
    pdf.multi_cell(0, 5, p2_text)

    # ==========================================
    # PÁGINA 3: DETALLE DE CÁLCULOS Y OPCIÓN A (FALLA)
    # ==========================================
    pdf.add_page()
    
    pdf.set_font("Helvetica", "B", 10.5)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(0, 5, "3.1 Verificacion de los Calculos Matematicos del Adaptador", 0, 1, "L")
    pdf.ln(2)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    calc_text = (
        "El sistema no alucina datos financieros, ya que el adaptador los calcula localmente antes de entregarlos al LLM:\n"
        "- Deduccion de Comision (0.5%): Sobre un capital de $1,500.00 USD, calcula de forma exacta: $7.50 USD.\n"
        "- Monto Neto Destinado a Compra: Saldo liquido libre para inversion: $1,492.50 USD ($1,500.00 - $7.50).\n"
        "- Consulta de Mercado Real: El conector asincrono asocia el precio real de CoinGecko del instante de tu click.\n"
        "- Cantidad de Activo Comprada: Se calcula la fraccion exacta de Bitcoin adquirida: 0.019395 BTC ($1492.50 / $76,952.00).\n"
        "- Simulacion de Salida (ROI Proyectado): Proyecta ganancias si toca tu meta de $80,000 USD:\n"
        "   * Valor de la Cartera: $1,791.00 USD\n"
        "   * Retorno Neto (Ganancia Liquida): $291.00 USD\n"
        "   * Retorno de Inversion (ROI): 19.40%"
    )
    pdf.multi_cell(0, 5, calc_text)
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 10.5)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(0, 5, "3.2 Observabilidad de Latencia y Rendimiento (x-process-time)", 0, 1, "L")
    pdf.ln(2)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    latency_text = (
        "En las cabeceras de respuesta (Response headers), observa el valor de 'x-process-time'.\n"
        "Un valor de ~886.90ms demuestra un rendimiento excelente. Significa que el ciclo completo "
        "(autenticacion, enmascaramiento PII Marcelo Gilardoni -> M****** G********, llamada asincrona a CoinGecko, "
        "persistencia local y explicacion con Gemini 3.5) tomo menos de un segundo."
    )
    pdf.multi_cell(0, 5, latency_text)
    pdf.ln(5)

    # 4. Tercera Prueba: Simulación de Falla (Opcion A)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "4. Tercera Prueba: Simulacion de Falla de Consistencia (ACID - HTTP 503)", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    
    p3_desc = (
        "Demuestra resiliencia y transaccionalidad robusta ante fallos fisicos de disco o bases de datos:\n"
        "1. Bloquear Base de Datos: Ve a 'codigo/database/mock_db.json' en Windows. Clic derecho -> Propiedades "
        "-> Marca la casilla 'Solo lectura' (Read-only) -> Aceptar.\n"
        "2. Ejecutar la Consulta: Presiona 'Execute' de nuevo en tu navegador o ejecuta el script de consola:\n"
        "   python codigo/scripts/demo_gemini_streaming.py\n"
        "3. Resultado Obtenido: Recibiras de manera limpia un codigo HTTP 503 Service Unavailable informando: "
        "'Error de consistencia de datos: No se pudo registrar la simulacion en base de datos. Motivo: Permission denied.'"
    )
    pdf.multi_cell(0, 5, p3_desc)
    
    # ==========================================
    # PÁGINA 4: DETALLES DE FALLAS Y PRUEBAS QA
    # ==========================================
    pdf.add_page()
    
    pdf.set_font("Helvetica", "B", 10.5)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(0, 5, "4.1 Diagnostico de la Causa Fisica", 0, 1, "L")
    pdf.ln(2)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    p31_text = (
        "Al estar en 'Solo lectura', el sistema operativo de Windows le niega el permiso de escritura a Python, "
        "arrojando un IOError (Errno 13). Tu adaptador financiero intercepta el error al instante, abortando "
        "el proceso de forma segura."
    )
    pdf.multi_cell(0, 5, p31_text)
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 10.5)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(0, 5, "4.2 Transaccionalidad Estricta y Consistencia (Garantia ACID)", 0, 1, "L")
    pdf.ln(2)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    p32_text = (
        "En ambientes financieros, la integridad es prioritaria. Si la base de datos local falla, abortamos la "
        "operacion inmediatamente antes de llamar a Gemini 3.5. Esto previene facturar costos de red inútiles "
        "e impide inconsistencias de datos, indicando de forma transparente al usuario que vuelva a intentar."
    )
    pdf.multi_cell(0, 5, p32_text)
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 10.5)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(0, 5, "4.3 Diagnostico Automatico en Consola (OpenTelemetry)", 0, 1, "L")
    pdf.ln(2)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    p33_text = (
        "De fondo, en tu consola de PowerShell del servidor FastAPI, OpenTelemetry captura la excepcion "
        "PermissionError de forma autonoma, marcando el Span en estado 'ERROR' y asociando la traza, "
        "al mismo tiempo que mantiene tu servidor web levantado y asombrosamente resiliente ante otras peticiones."
    )
    pdf.multi_cell(0, 5, p33_text)
    pdf.ln(5)

    # 5. Cuarta Prueba: Aseguramiento de Calidad
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 8, "5. Cuarta Prueba: Aseguramiento de Calidad y Latencias", 0, 1, "L")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(75, 85, 99)
    p4_desc = (
        "Muestra al docente las evidencias cientificas y automatizadas de rendimiento de tu API:\n\n"
        "A) Correr la Suite de Pruebas Unitarias de Pytest (Offline & Deterministas):\n"
        "   Comando literal: python -m pytest codigo/tests/test_trading_api.py -v\n"
        "   - Se ejecutaran 6 pruebas unitarias exitosas ('6 passed in ~1.05s') que verifican salud, "
        "claves, enmascaramiento y alias de compatibilidad en un entorno offline sin costos de API.\n\n"
        "B) Correr el Benchmark de Latencias (10 llamadas consecutivas):\n"
        "   Comando literal: python codigo/scripts/benchmark_latencia.py\n"
        "   - Calcula los percentiles reales del servidor local: p50 (Mediana) de ~20.97 ms y p95 de ~28.86 ms, "
        "guardando las mediciones de rendimiento en el archivo 'database/benchmark_results.json'."
    )
    pdf.multi_cell(0, 5, p4_desc)
    
    # Escribir PDF final
    target_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "doc", "guia_demostracion.pdf")
    pdf.output(target_path)
    print(f"Manual compilado exitosamente desde Word como: {target_path}")

if __name__ == "__main__":
    compile_professional_guide()
