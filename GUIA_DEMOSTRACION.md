# 🚀 Guía de Demostración en Vivo - Trabajo Final de Integración
## 📈 Trading ROI Explainer & Transaction Simulator API (Con Gemini 3.5 & OpenTelemetry)

Esta guía contiene los pasos altamente detallados y ordenados para realizar una **demostración en vivo espectacular** de tu trabajo final ante el jurado o docente del curso de **Estrategias de Integración** en el **BSG Institute**. 

El proyecto une una capa de servicios web en **FastAPI**, un **Adaptador Financiero** con enmascaramiento de datos personales (PII) y cálculo de ROI/comisiones, un **Conector de Precios** asíncrono (CoinGecko), un motor cognitivo con **Gemini 3.5** de Google, y un sistema de diagnóstico empresarial con **OpenTelemetry**.

---

## 📋 Requisitos Previos de la Demostración
1.  Asegúrate de contar con una terminal de PowerShell lista.
2.  El intérprete de Python virtual ya está equipado con todas las dependencias instaladas (`fastapi`, `google-generativeai`, `opentelemetry`, `pytest`, `fpdf`, `numpy`, etc.).
3.  Tu API Key de Gemini real se encuentra configurada en el archivo `config.py` de forma activa.

---

## 🎯 PASO 1: Demostración de Gemini 3.5 en Consola (Streaming vs No Streaming)
Muestra la diferencia visual e interactiva entre consumir un modelo de lenguaje de forma síncrona convencional versus streaming de tokens en tiempo real, señalando la sanitización de datos (enmascaramiento).

### 1.1 Ejecución CON STREAMING (Rendimiento Óptimo de UX)
*   **Comando a ejecutar en tu terminal:**
    ```powershell
    & "C:\OpenCode\sesion_3\.venv\Scripts\python.exe" "C:\OpenCode\1-integracion-tbf\codigo\scripts\demo_gemini_streaming.py" --stream
    ```
*   **Qué señalar e indicar al profesor en vivo (Guión de demostración):**
    1.  **Caja de Comprobación de Enmascaramiento:** Resalta en pantalla la sección `🔍 PROMPT DE SISTEMA Y DATOS SANITIZADOS`. Muestra al profesor que el nombre real `"Maria Gomez"` fue interceptado por tu adaptador y reemplazado en el prompt por `"M**** G****"`, protegiendo la privacidad de los datos (PII).
    2.  **Prevención de Prompt Injection:** Señala cómo el mensaje libre se limpia y se extraen estrictamente los parámetros financieros (`activo="BTC"`, `monto=1500.0`, `precio_meta=80000.0`) para que ningún texto libre malicioso llegue a Gemini.
    3.  **Fluidez del Stream:** Muestra cómo los tokens de respuesta se imprimen en pantalla de manera **instantánea y secuencial** (latencia menor a 1 segundo), dando una experiencia interactiva idéntica a ChatGPT.
    4.  **Cálculos del Adaptador:** Destaca la exactitud matemática del informe: comisión del 0.5% deducida ($7.50 USD), cantidad neta comprada (0.019006 BTC) y ROI neto calculado (1.36%).

### 1.2 Ejecución SIN STREAMING (Comportamiento Síncrono Tradicional)
*   **Comando a ejecutar en tu terminal:**
    ```powershell
    & "C:\OpenCode\sesion_3\.venv\Scripts\python.exe" "C:\OpenCode\1-integracion-tbf\codigo\scripts\demo_gemini_streaming.py"
    ```
*   **Qué señalar en vivo:**
    1.  La terminal esperará unos 20 segundos de forma estática antes de imprimir nada.
    2.  Muestra que el reporte aparece "de golpe". Explica al profesor que esto justifica técnicamente por qué elegiste el patrón de **Streaming** para tu diseño de producción, reduciendo el tiempo de espera psicológica del cliente final.

---

## ⚡ PASO 2: Levantar el Servidor Web y Demostración de Seguridad
Muestra cómo tu endpoint del backend se encuentra totalmente "cerrado con llave" ante accesos no autorizados.

1.  **Inicia el servidor web de FastAPI:**
    ```powershell
    & "C:\OpenCode\sesion_3\.venv\Scripts\python.exe" -m uvicorn main:app --reload --host 127.0.0.1 --port 8000 --app-dir "C:\OpenCode\1-integracion-tbf\codigo"
    ```
2.  **Abre tu navegador e ingresa a la interfaz interactiva:**
    👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**
3.  **Prueba de Seguridad (Endpoint Cerrado):**
    *   Despliega el endpoint `POST /api/v1/trading/explain` y haz clic en **"Try it out"**.
    *   Presiona **"Execute"** sin configurar ninguna autorización. Señala cómo la API bloquea el acceso inmediatamente y retorna un código de error **`HTTP 401 Unauthorized`** (Punto de Control 1 cumplido).
    *   Ahora, ingresa la clave de acceso configurada (`trading-secret-key-123`) en la cabecera **`X-API-Key`** de Swagger, y presiona **"Execute"**. Verás cómo el servidor valida la firma y te entrega una respuesta **`HTTP 200 OK`** exitosa.

---

## 🔍 PASO 3: Demostración de Observabilidad con OpenTelemetry (OTel)
Esta sección demuestra el grado de madurez técnica del proyecto, mostrando cómo se identifican de forma científica latencias y errores.

*   **Mientras el servidor de FastAPI del Paso 2 sigue corriendo, observa los logs en tu terminal de comandos:**

### 3.1 Desglose de Spans en Consola (Estructura de Tiempos)
*   **Qué señalar en vivo:**
    Señala al profesor que OpenTelemetry instrumenta cada capa del sistema de forma automática. Al realizar una consulta exitosa, se imprimen en consola las trazas de tiempo desglosadas por capa:
    *   `[OTel Span] 'get_asset_price'`: Latencia exacta del conector a la API de precios externa (~15 ms).
    *   `[OTel Span] 'simulate_transaction'`: Latencia de los cálculos financieros locales (~23 ms).
    *   `[OTel Span] 'run_query'`: Latencia de la llamada cognitiva a Gemini 3.5 en Google (~1120 ms).
    *   *Explica que esto demuestra de forma cuantitativa que el cuello de botella es la llamada externa a Gemini, y no tus bases de datos o adaptadores locales.*

### 3.2 Correlación de Logs (Trace ID & Span ID)
*   **Qué señalar en vivo:**
    Muestra cómo cada línea de log tradicional impresa por tu servidor FastAPI incluye ahora de manera inyectada y automática los identificadores de correlación:
    `[TraceId: 7f81b2c499... | SpanId: a01b3c...]`
    *Explica al docente que si tuvieras miles de usuarios consultando simultáneamente en producción, con este TraceId único puedes rastrear de forma unificada toda la historia de una sola petición, correlacionando logs con trazas en Jaeger o Grafana.*

### 3.3 Diagnóstico de Errores en Vivo (La prueba de fuego)
Simula un fallo enviando un ticker que no exista para demostrar cómo OpenTelemetry registra la causa raíz.
*   **Cómo probarlo:** Envía un JSON con un activo no válido como `"XYZ"` al endpoint de trading.
*   **Qué señalar en vivo:**
    Muestra cómo OpenTelemetry detecta la excepción, marca el span del conector con estado **`ERROR`** e inyecta los metadatos exactos de la excepción: `"error.type": "HTTP 404 Not Found"`, describiendo el motivo del error. Al mismo tiempo, resalta que el middleware de FastAPI captura el fallo y mantiene la API online, evitando caídas inesperadas del servicio (*resiliencia*).

### 3.4 Simulación de Falla en Base de Datos (Integridad & ACID)
Demuestra el comportamiento estricto y consistente de transaccionalidad financiera de tu sistema.
*   **Cómo probarlo en Windows (En vivo):**
    1. Ve al archivo `codigo/database/mock_db.json`.
    2. Haz clic derecho -> **Propiedades**.
    3. Marca la casilla **"Solo lectura" (Read-only)** y dale Aplicar/Aceptar.
    4. Ejecuta el script de demostración o llama al endpoint de trading.
*   **Qué señalar en vivo:**
    1. **Aborto Seguro:** Muestra cómo el sistema detecta de forma instantánea que la base de datos está bloqueada y **abortar de inmediato la ejecución** antes de consumir tokens o costos en Gemini 3.5.
    2. **Mensaje Consistente al Cliente:** Resalta la respuesta de error controlada entregada al usuario: *"Error de consistencia de datos: No se pudo registrar la simulación en base de datos. Por favor reintente."*
    3. **Trazabilidad de Error:** Observa cómo OpenTelemetry registra de inmediato un Span en estado **`ERROR`** con la excepción `PermissionError` y el mensaje de error de acceso en disco.
    4. *(¡No olvides desmarcar la casilla de "Solo lectura" al finalizar la demostración para que todo vuelva a la normalidad!)*

---

## 📊 PASO 4: Aseguramiento de Calidad y Entregas (Métricas p50 / p95)
Muestra las evidencias de calidad técnica y los percentiles de rendimiento calculados de forma empírica:

1.  **Ejecuta el script de Benchmark de Latencias (10 peticiones secuenciales consecutivas):**
    ```powershell
    & "C:\OpenCode\sesion_3\.venv\Scripts\python.exe" "C:\OpenCode\1-integracion-tbf\codigo\scripts\benchmark_latencia.py"
    ```
    *Señala la tabla de percentiles impresa en pantalla: p50 (Mediana) y p95 (Peor caso del 5%). Explica que estas mediciones se guardan en el archivo `codigo/database/benchmark_results.json` para auditar el rendimiento.*
2.  **Corre la Suite de Pruebas Unitarias (Tests con Pytest):**
    ```powershell
    & "C:\OpenCode\sesion_3\.venv\Scripts\python.exe" -m pytest "C:\OpenCode\1-integracion-tbf\codigo\tests\test_trading_api.py" -v
    ```
    *Muestra cómo se ejecutan 6 pruebas unitarias exitosas que verifican la salud de la API, las API Keys correctas e incorrectas, el enmascaramiento y las excepciones en menos de 2 segundos.*

---

## 📂 PASO 5: Muestreo de la Carpeta de Documentación (PDFs Listos)
Muestra al docente que en la carpeta **`doc/`** cuentas con informes y diagramas con calidad de producción:
1.  **`proyecto_integracion_trading_roi.pdf`**: El plan de una página oficial e informe arquitectónico por capas.
2.  **`flujo_datos_y_arquitectura.pdf`**: Reporte técnico de 7 fases y diagrama de arquitectura moderno (`arquitectura_integracion.png`).
3.  **`observabilidad_proyecto.pdf`**: Documentación técnica del diseño de OpenTelemetry.
4.  **`guia_demostracion.pdf`**: Esta guía compilada para que el profesor se la pueda llevar en PDF.

---

### ¡Tu demostración en vivo está lista para brillar y obtener la nota máxima! 🚀📈
