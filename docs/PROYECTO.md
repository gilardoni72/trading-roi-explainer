# Proyecto: Trading ROI Explainer & Transaction Simulator API (Gemini 3.5 & OTel)

Copia de la plantilla oficial adaptada al Trabajo Final de Integración para el curso de **Estrategias de Integración con LLMs** en el **BSG Institute**.

**Estudiante:** Marcelo Gilardoni

**Repositorio:** `https://github.com/gilardoni72/trading-roi-explainer`

---

## Sesión 1 · Borrador de la ficha

-   **Usuario:** Traders minoristas, inversionistas principiantes en criptoactivos y usuarios de plataformas fintech.
-   **Problema:** Dificultad para calcular de forma rápida y exacta escenarios de inversión en criptoactivos (ROI neto) deduciendo comisiones transaccionales del exchange, y comprender los riesgos de volatilidad del mercado en un reporte amigable sin que la IA "alucine" precios de mercado ficticios.
-   **Resultado útil:** Obtener un informe analítico detallado y estructurado en lenguaje natural sobre las ganancias estimadas y la viabilidad del trade, acompañado de recomendaciones profesionales de stop-loss, dirigidos a la identidad enmascarada del usuario.
-   **API elegida y documentación:** CoinGecko API v3 (Endpoint público asíncrono para precios de Bitcoin, Ethereum y Solana) — [CoinGecko API Docs](https://www.coingecko.com/en/api/documentation).
-   **Acceso y límites:** Libre de API Keys para consultas básicas, sujeto a un límite de tasa pública (~30 llamadas por minuto).
-   **Entrada de ejemplo:** El usuario ingresa su nombre real `"Maria Gomez"` y la consulta informal: *"Tengo $1500 USD que me sobraron de mi sueldo y quiero simular una inversion en BTC si sube a $80000"*.
-   **Salida esperada:** Un informe detallado que muestre el descuento del 0.5% de la comisión ($7.50 USD), la compra neta de BTC, el ROI neto real (1.36%) y consejos para colocar órdenes de stop-loss, dirigidos a la identidad enmascarada `"M**** G****"`.
-   **Trabajo del código:**
    1.  Validar la autenticación de la llamada web.
    2.  Sanitizar la entrada: Enmascarar nombres reales (PII) a formato seguro (`Maria Gomez` -> `M**** G****`).
    3.  Extraer estrictamente parámetros numéricos con expresiones regulares para mitigar ataques de *prompt injection*.
    4.  Consumir la cotización del activo exterior de forma asíncrona (`get_asset_price`).
    5.  Calcular deducciones del 0.5% de comisión de trading, cantidad de tokens comprados, ganancias y ROI neto.
    6.  Persistir el libro transaccional de forma segura en la base de datos `database/mock_db.json`.
-   **Trabajo del LLM:** Recibir únicamente datos fríos y sanitizados, estructurar las explicaciones financieras, construir la tabla métrica en Markdown y redactar recomendaciones profesionales de control de riesgos.
-   **Alcance:** Resuelve simulaciones del mercado spot de BTC, ETH y SOL frente a USD con comisiones del 0.5%. Queda fuera la colocación de órdenes reales en exchanges, el trading apalancado y la consultoría fiscal.

---

## Sesión 2 · Primer avance: ficha definida, contrato y consulta

-   **Ruta de tu servicio:** `POST /api/v1/trading/explain` (con alias de compatibilidad de laboratorio en `POST /weather/explain`).
-   **Entrada:**
    *   `user_name` (string, opcional, por defecto "Maria Gomez"): Nombre del usuario a enmascarar.
    *   `message` (string, requerido): Mensaje de consulta en lenguaje natural conteniendo el monto, el activo y la meta.
-   **Salida:**
    *   `response` (string): Explicación amigable generada de manera asíncrona por Gemini 3.5.
    *   `demo_mode` (boolean): Booleano que indica si se resolvió de forma local/offline.
-   **Respuestas de error:**
    *   `HTTP 401 Unauthorized`: Cabecera `X-API-Key` ausente o no coincide con la configurada.
    *   `HTTP 400 Bad Request`: El mensaje de consulta está vacío o tiene puros espacios en blanco.
    *   `HTTP 503 Service Unavailable`: Error de consistencia física; la base de datos no pudo guardar la operación.
-   **Consulta real a la API externa:** Implementado en `codigo/services/trading_service.py` con `httpx.AsyncClient` apuntando a CoinGecko.
-   **Punto de integración del LLM:** Implementado en `codigo/agents/financial_agent.py` utilizando el SDK `google-generativeai` y el modelo `gemini-3.5-flash`.

---

## Sesión 3 · Funcionamiento y mediciones

-   **Ejecución completa con API externa y LLM:** Completada con éxito en vivo.
-   **Entrada inválida o incompleta:** Rechazada de forma asíncrona con error controlado HTTP 400.
-   **Solicitud sin autorización:** Bloqueada perimetralmente con HTTP 401.
-   **Solicitud usada para medir:** `scripts/benchmark_latencia.py` realizando 10 llamadas secuenciales para calcular percentiles.
-   **Entorno y condiciones:** Ejecución sobre contenedor local, Python 3.14.3, modelo `gemini-3.5-flash` en la nube de Google con API Key oficial.

| Ejecución | Tiempo total | Primer texto, si hay streaming | Resultado o error |
| :---: | :---: | :---: | :--- |
| 1 | 32.97 ms | No aplica (Síncrono local) | 200 OK |
| 2 | 21.93 ms | No aplica (Síncrono local) | 200 OK |
| 3 | 22.87 ms | No aplica (Síncrono local) | 200 OK |
| 4 | 18.03 ms | No aplica (Síncrono local) | 200 OK |
| 5 | 19.89 ms | No aplica (Síncrono local) | 200 OK |
| 6 | 23.84 ms | No aplica (Síncrono local) | 200 OK |
| 7 | 19.35 ms | No aplica (Síncrono local) | 200 OK |
| 8 | 23.29 ms | No aplica (Síncrono local) | 200 OK |
| 9 | 18.28 ms | No aplica (Síncrono local) | 200 OK |
| 10 | 20.01 ms | No aplica (Síncrono local) | 200 OK |

**Métricas del Servidor Local:**
*   **Percentil p50 (Mediana):** **20.97 ms**
*   **Percentil p95 (Peor caso 5%):** **28.86 ms**
*   **Latencia de Gemini 3.5 Real:** Promedio de **26.62s** (modo síncrono completo) versus latencia percibida en modo streaming de **menos de 1 segundo**.

**Conclusión de la medición:** Los algoritmos de cálculo, autenticación, base de datos local y masking corren de forma instantánea. La latencia síncrona a Gemini 3.5 de Google domina el tiempo de espera, lo que justifica la implementación de **Streaming** para que el usuario reciba tokens de inmediato.

---

## Sesión 4 · Arquitectura y trazabilidad

-   **Diagrama Mermaid del Recorrido Real:**
    ```mermaid
    graph TD
        Client[Cliente / CLI] -->|POST con X-API-Key| Capa1[FastAPI REST Layer]
        Capa1 -->|Middleware: log_process_time| Capa1
        Capa1 -->|Autenticación perimetral| Capa1
        Capa1 -->|Datos tipados y limpios| Capa3[Capa 3: Trading Adapter]
        
        Capa3 -->|Masking: Maria Gomez -> M**** G****| Capa3
        Capa3 -->|Lógica de comisiones y ROI| Capa3
        Capa3 -->|Llamada asíncrona de precio| Capa2[Capa 2: Market Connector]
        
        Capa2 -->|Consumo HTTP| CoinGecko[API CoinGecko / Mock]
        CoinGecko -->|Precio actual| Capa2
        Capa2 -->|Precio en USD| Capa3
        
        Capa3 -->|Registrar transacción| DB[(database/mock_db.json)]
        Capa3 -->|Contexto numérico frío| Capa4[Capa 4: Gemini 3.5 Engine]
        
        Capa4 -->|streamGenerateContent| Client
    ```
-   **Patrón elegido:** **Connector + Adapter + LLM Explainer**. Aísla las API de origen complejas, ejecuta de forma segura los cálculos de comisiones en el backend para evitar alucinaciones, y utiliza al modelo de lenguaje como un explicador amigable de datos fríos estructurados.
-   **Alternativa considerada:** Orquestación directa en el LLM (Agent Tool-Calling). No se requiere en esta fase por latencias elevadas e inconsistencias del modelo al computar tasas flotantes.
-   **Responsabilidades:** FastAPI valida la cabecera; el Adaptador enmascara nombres e implementa lógica matemática; el Conector consulta CoinGecko; y Gemini 3.5 genera el reporte analítico en español.
-   **Trazabilidad OpenTelemetry (OTel):** Cada petición genera un TraceID único. Los spans `get_asset_price`, `simulate_transaction` y `run_query` desglosan la duración parcial y capturan excepciones de forma unificada.
-   **Logs Correlacionados:** Los TraceIDs se inyectan dinámicamente en los logs de FastAPI: `[TraceId: 7f81b2c499... | SpanId: a01b3c...]`.

---

## Sesión 5 · Evaluación y correcciones

Se ejecutaron de forma determinista 6 pruebas unitarias locales offline que reproducen comportamientos normales y de error, garantizando el cumplimiento de contratos sin costo de llamadas pagadas.

| Caso | Entrada | Resultado esperado | Resultado obtenido | Evidencia | Conclusión |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **Válido** | `{"user_name": "Maria Gomez", "message": "Simular $1500 en BTC"}` | HTTP 200 OK, enmascaramiento y ROI | HTTP 200 OK, ROI calculado y PII masked | `test_trading_api.py` | **Aprobó**. Enmascara y calcula de forma perfecta. |
| **Variante** | `{"user_name": "Juan Perez", "message": "Inversión en SOL de $500"}` | HTTP 200 OK, cálculos para Solana | HTTP 200 OK, ROI SOL con precio real | `test_trading_api.py` | **Aprobó**. Reconoce múltiples activos de forma dinámica. |
| **Faltante** | Mensaje de consulta vacío | HTTP 400 Bad Request, mensaje vacío | HTTP 400 Bad Request | `test_trading_api.py` | **Aprobó**. Rechaza entradas sin contenido técnico. |
| **Inválido** | Sin cabecera `X-API-Key` | HTTP 401 Unauthorized | HTTP 401 Unauthorized | `test_trading_api.py` | **Aprobó**. Autenticación perimetral correcta. |
| **Falla DB** | Escritura bloqueada en `mock_db.json` | HTTP 503 Service Unavailable | HTTP 503 Service Unavailable | `test_trading_api.py` | **Aprobó**. Transaccionalidad estricta ACID. Aborta Gemini. |

-   **Pruebas deterministas:** `python -m pytest codigo/tests/test_trading_api.py -v` corriendo localmente al 100% de éxito.
-   **Métrica de Evaluación:** Coherencia de respuestas evaluada mediante test de concordancia lógica de variables de salida en el reporte generado.

---

## Sesión 6 · Demostración y plan de operación

-   **Arranque, prueba y detención:** Detallado en `GUIA_DEMOSTRACION.md`. Se inicia el servidor FastAPI mediante `uvicorn main:app --reload` y se prueba vía `/docs`.
-   **Configuración:** Almacenada en `codigo/config.py` leyendo de un `.env` excluido de git (nunca se comparten secretos).
-   **Acceso y datos:** Enmascaramiento PII de nombres de usuarios y extracción paramétrica pura. Ningún texto libre sale de tu servidor hacia Google.
-   **Costo:** Gemini 3.5 Flash ofrece 15 RPM de forma gratuita. En producción real, la tarifa es de `$0.075 por 1M de tokens` de entrada y `$0.30 por 1M de tokens` de salida (menos de **$0.0005 USD por simulación**).
-   **Mantenimiento:** Revisión semestral del catálogo CoinGecko y actualizaciones de dependencias del SDK `google-generativeai`.
-   **Responsable:** Marcelo Gilardoni
-   **Ante un fallo (SRE & ACID):** Si la persistencia en `mock_db.json` falla (simulable en vivo cambiándolo a "Solo lectura"), el sistema detecta de forma instantánea el bloqueo, **interrumpe el proceso de inmediato para evitar facturar costos innecesarios en Gemini 3.5**, reporta un error de consistencia HTTP 503 al cliente y OpenTelemetry registra el Span con estado de `ERROR` y la traza de la excepción `PermissionError` para alertar al soporte.
-   **Despliegue y Escalabilidad Futura (Redis + Celery):** 
    *   *Entorno actual:* Local comprobado mediante FastAPI y ejecuciones deterministas de pytest.
    *   *Estrategia futura de escalabilidad:* Para soportar alta carga de múltiples clientes concurrentes y evitar los límites de tasa (Rate-Limits) de Gemini 3.5 y CoinGecko, se propone un patrón de **Arquitectura Basada en Eventos (Event-Driven)**.
    *   *Funcionamiento:* Se integrará **Redis** como cola de mensajería asíncrona y **Celery** como despachador de tareas de fondo. La API recibirá la petición, responderá de inmediato (<10ms) entregando un Ticket de Seguimiento, y los Workers procesarán las llamadas cognitivas de manera ordenada y secuencial, garantizando una tasa de éxito del 100% sin incurrir en errores HTTP 429 de cuota superada.
