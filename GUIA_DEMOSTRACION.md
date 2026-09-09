# 🚀 Guía de Demostración en Vivo - Trabajo Final de Integración
## 📈 Trading ROI Explainer & Transaction Simulator API (Con Gemini 3.5, OTel & Langfuse)

Esta guía contiene la secuencia detallada de comandos, pasos e indicaciones para realizar una **demostración en vivo impecable y espectacular** de tu trabajo final ante el jurado o docente del curso en el **BSG Institute**.

Sigue cada paso al pie de la letra. Todos los comandos han sido probados y están listos para ser copiados y ejecutados directamente en tu terminal de **PowerShell**.

---

## 📋 PASO 0: Preparación Inicial de la Consola
Antes de comenzar la exposición, abre una terminal de **PowerShell** en tu computadora, posiciónate en la carpeta raíz de tu proyecto final y activa el entorno virtual de Python ejecutando los siguientes comandos literales:

```powershell
# 1. Ir a la carpeta del proyecto final
cd C:\OpenCode\1-integracion-tbf

# 2. Activar el entorno virtual de Python
.venv\Scripts\Activate.ps1
```

---

## 🎯 PASO 1: Demostración del Agente Gemini 3.5 en Consola (Streaming vs No Streaming)
Muestra visualmente la gran diferencia en la experiencia de usuario (UX) entre el consumo síncrono convencional y el streaming de tokens en tiempo real, enseñando además cómo se realiza la sanitización y el enmascaramiento automático de datos personales (PII).

### 1.1 Ejecución CON STREAMING (Rendimiento Óptimo de UX)
*   **Comando a ejecutar en tu terminal:**
    ```powershell
    & "C:\OpenCode\sesion_3\.venv\Scripts\python.exe" "C:\OpenCode\1-integracion-tbf\codigo\scripts\demo_gemini_streaming.py" --stream
    ```
*   **Qué señalar en vivo (Guión):**
    1.  **Caja de Comprobación de Enmascaramiento:** Señala en la consola la sección `🔍 PROMPT DE SISTEMA Y DATOS SANITIZADOS`. Muestra que tu adaptador interceptó el nombre real del usuario `"Maria Gomez"` y lo enmascaró a `"M**** G****"` para resguardar su privacidad antes de enviarlo a los servidores de Google.
    2.  **Mitigación de Inyecciones:** Señala que la consulta informal se ha limpiado, enviando al LLM únicamente variables numéricas frías y tipadas (`monto_usd=1500.0`, `precio_meta=80000.0`).
    3.  **Velocidad de Respuesta:** Muestra cómo los tokens (palabras) fluyen en la pantalla de inmediato (en menos de 1 segundo), dando una sensación interactiva idéntica a ChatGPT o Claude.
    4.  **Cálculos del Adaptador:** Destaca la exactitud matemática del reporte: comisión del 0.5% deducida ($7.50 USD), cantidad neta comprada (0.019006 BTC) y ROI neto de 1.36%.

### 1.2 Ejecución SIN STREAMING (Comportamiento Síncrono Convencional)
*   **Comando a ejecutar en tu terminal:**
    ```powershell
    & "C:\OpenCode\sesion_3\.venv\Scripts\python.exe" "C:\OpenCode\1-integracion-tbf\codigo\scripts\demo_gemini_streaming.py"
    ```
*   **Qué señalar en vivo (Guión):**
    1.  La terminal esperará unos 20-30 segundos de forma estática en silencio total antes de mostrar la respuesta de golpe.
    2.  Explica que esto justifica técnicamente por qué elegiste el patrón de **Streaming** para tu diseño de producción, optimizando el tiempo percibido por el cliente final.

---

## ⚡ PASO 2: Levantar el Servidor Web y Demostración de Seguridad
Muestra cómo tu endpoint del backend se encuentra totalmente "cerrado con llave" ante accesos no autorizados.

1.  **Inicia el servidor web de FastAPI:**
    ```powershell
    & "C:\OpenCode\sesion_3\.venv\Scripts\python.exe" -m uvicorn main:app --reload --host 127.0.0.1 --port 8000 --app-dir "C:\OpenCode\1-integracion-tbf\codigo"
    ```
2.  **Abre tu navegador de internet e ingresa a la interfaz Swagger:**
    👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**
3.  **Prueba de Seguridad (Endpoint Cerrado):**
    *   Despliega el endpoint `POST /api/v1/trading/explain` y haz clic en **"Try it out"**.
    *   Presiona **"Execute"** sin configurar ninguna cabecera de autorización. Señala cómo la API bloquea el acceso inmediatamente y retorna un código de error **`HTTP 401 Unauthorized`** (Punto de Control 1 cumplido).
    *   Ahora, ingresa la clave de acceso configurada (`trading-secret-key-123`) en la cabecera **`X-API-Key`** de Swagger, y presiona **"Execute"**. Verás cómo el servidor valida la firma y te entrega una respuesta **`HTTP 200 OK`** exitosa.

---

## 🔍 PASO 3: Demostración de Observabilidad con OpenTelemetry (OTel)
Muestra cómo se realiza la auditoría y monitoreo por Spans en tiempo real.

*   **Mientras el servidor de FastAPI del Paso 2 sigue corriendo, observa los logs en tu terminal de comandos:**

### 3.1 Desglose de Spans en Consola
Al realizar una consulta exitosa, señala al profesor que OpenTelemetry instrumenta cada capa de forma automática, imprimiendo las duraciones parciales exactas por capa en consola:
*   `[OTel Span] 'get_asset_price'`: Latencia del conector asíncrono a la API de CoinGecko (~15 ms).
*   `[OTel Span] 'simulate_transaction'`: Latencia de los cálculos locales del adaptador (~23 ms).
*   `[OTel Span] 'run_query'`: Latencia de la llamada cognitiva a Gemini 3.5 en Google (~1120 ms).
*   *Explica que esto demuestra científicamente que el principal cuello de botella es la llamada externa a Gemini, y no tus bases de datos o adaptadores locales.*

### 3.2 Correlación de Logs (Trace ID & Span ID)
Señala cómo cada línea de log tradicional del servidor FastAPI incluye ahora de manera inyectada y automática los identificadores de correlación:
`[TraceId: 7f81b2c499... | SpanId: a01b3c...]`
*Explica al docente que si tuvieras miles de usuarios consultando simultáneamente en producción, con este TraceId único puedes rastrear de forma unificada toda la historia de una sola petición.*

### 3.3 Diagnóstico de Errores en Vivo (La prueba de fuego)
Simula un fallo enviando un activo no válido como `"XYZ"` para demostrar cómo OpenTelemetry registra la causa raíz.
*   **Comando HTTP para simular el fallo (Ejecútalo desde otra terminal):**
    ```powershell
    Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/trading/explain" `
      -Method Post `
      -Headers @{"X-API-Key"="trading-secret-key-123"} `
      -ContentType "application/json" `
      -Body '{"user_name":"Maria Gomez", "message":"Invertir en XYZ"}'
    ```
*   **Qué señalar en vivo:**
    Muestra cómo en la terminal del servidor de FastAPI, OpenTelemetry marca el Span de base de datos o conector con estado **`ERROR`** e inyecta los metadatos exactos de la excepción: `"error.type": "HTTP 404 Not Found"`.

### 3.4 Simulación de Falla en Base de Datos (Integridad & ACID)
Demuestra el comportamiento estricto y consistente de transaccionalidad financiera de tu sistema.
*   **Cómo probarlo en Windows (En vivo):**
    1. Ve al archivo `C:\OpenCode\1-integracion-tbf\codigo\database\mock_db.json`.
    2. Haz clic derecho -> **Propiedades**.
    3. Marca la casilla **"Solo lectura" (Read-only)** y dale Aplicar/Aceptar.
    4. Realiza una llamada al endpoint desde Swagger o ejecuta el script de consola.
*   **Qué señalar en vivo:**
    1. **Aborto Seguro:** Muestra cómo el sistema detecta de forma instantánea que la base de datos está bloqueada e **interrumpe de inmediato la ejecución** antes de consumir tokens o costos en Gemini 3.5.
    2. **Mensaje de Consistencia al Cliente:** Resalta la respuesta de error controlada entregada al usuario: *"Error de consistencia de datos: No se pudo registrar la simulación en base de datos. Por favor reintente."*
    3. *(¡No olvides desmarcar la casilla de "Solo lectura" de `mock_db.json` al finalizar la demostración para que todo vuelva a la normalidad!)*

---

## 📈 PASO 4: Observabilidad en la Nube con Langfuse (LLM Ops)
Muestra el monitoreo en la nube para auditar costos, prompts y tokens en tiempo real.

*   **Cómo probarlo (En vivo):**
    1. Abre tu navegador de internet en **Langfuse Cloud**: 👉 **[us.cloud.langfuse.com](https://us.cloud.langfuse.com)** e inicia sesión.
    2. Realiza una simulación exitosa de inversión para el usuario `"Maria Gomez"`.
*   **Qué señalar en vivo en el Panel de Langfuse:**
    1. **Trazas (Traces):** Muestra el listado de ejecuciones de la simulación de trading.
    2. **Costos en USD:** Señala cómo Langfuse calcula de forma automática el costo en dólares de tu simulación con Gemini 3.5 (ejemplo: `$0.0002 USD`), demostrando control de presupuesto.
    3. **Enmascaramiento de Identidad:** Señala que el identificador registrado es **`M**** G****`**, demostrando que tus políticas de privacidad protegen los datos del usuario antes de subirlos a la nube.
    4. **Generaciones & Prompts:** Explica cómo la plataforma registra la llamada cognitiva, el prompt del sistema y la respuesta generada por el LLM.

---

## 🧪 PASO 5: Evaluación de Calidad Automatizada con Datasets en Langfuse
Demuestra al profesor el estándar de oro para evaluar y blindar el comportamiento del LLM contra alucinaciones.

*   **Comandos a ejecutar paso a paso en tu terminal de PowerShell:**

1.  **Paso 1: Crear el Dataset en la nube:**
    Ejecuta el siguiente comando para crear de forma autónoma el dataset `trading_agent_evaluation` en tu consola con 3 casos de prueba preestablecidos:
    ```powershell
    & "C:\OpenCode\sesion_3\.venv\Scripts\python.exe" "C:\OpenCode\1-integracion-tbf\codigo\scripts\create_langfuse_dataset.py"
    ```

2.  **Paso 2: Ejecutar la corrida de evaluación en vivo:**
    Corre la evaluación para descargar los ítems, procesarlos con tu agente de Gemini y registrar las comparativas y puntajes en la nube:
    ```powershell
    & "C:\OpenCode\sesion_3\.venv\Scripts\python.exe" "C:\OpenCode\1-integracion-tbf\codigo\scripts\run_langfuse_evaluation.py"
    ```

*   **Qué señalar en vivo en el Panel de Langfuse:**
    1. Abre la pestaña **"Datasets"** en tu consola de Langfuse Cloud.
    2. Selecciona **`trading_agent_evaluation`** y enseña los 3 casos de prueba almacenados.
    3. Ve a la pestaña **"Runs"** para mostrar la comparativa lado a lado entre la Entrada, la Respuesta generada por Gemini y el Resultado Esperado de Referencia.

---

## 📊 PASO 6: Aseguramiento de Calidad y Entregas (Métricas p50 / p95)
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

## 📂 PASO 7: Muestreo de la Carpeta de Documentación (PDFs Listos)
Muestra al docente que en la carpeta **`doc/`** cuentas con informes y diagramas con calidad de producción:
1.  **`proyecto_integracion_trading_roi.pdf`**: El plan de una página oficial e informe arquitectónico por capas.
2.  **`flujo_datos_y_arquitectura.pdf`**: Reporte técnico de 7 fases y diagrama de arquitectura moderno (`arquitectura_integracion.png`).
3.  **`observabilidad_proyecto.pdf`**: Documentación técnica del diseño de OpenTelemetry.
4.  **`guia_demostracion.pdf`**: Esta guía compilada para que el profesor se la pueda llevar en PDF.

---

### ¡Tu demostración en vivo está lista para brillar y obtener la nota máxima! 🚀📈
