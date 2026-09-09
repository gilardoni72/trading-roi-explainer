import os
import time
import logging
from fastapi import FastAPI, Request, HTTPException, Depends, Header, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from config import settings
from agents.financial_agent import FinancialAgentManager
from observability import instrument_app, trace

# Configurar logging basico
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Instanciar aplicacion FastAPI
app = FastAPI(
    title="📈 Trading ROI Explainer & Transaction Simulator API",
    description="API inteligente que integra simulacion financiera con agentes de lenguaje natural para evaluar retornos de inversion (ROI).",
    version="1.0.0"
)

# Instrumentar con OpenTelemetry de forma automatica para trazas HTTP
instrument_app(app)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Dependencia de Seguridad: Validacion de API Key (Cerrar el endpoint) ---
async def verify_api_key(x_api_key: str = Header(None, alias="X-API-Key")):
    """
    Verifica que la peticion contenga la cabecera 'X-API-Key' valida.
    Si falta o no coincide con la configurada, retorna error 401.
    """
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error de autenticacion: La cabecera 'X-API-Key' es requerida y esta ausente."
        )
    if x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error de autenticacion: La clave proporcionada en 'X-API-Key' es incorrecta."
        )
    return x_api_key

# --- Esquemas de entrada y salida ---
class TradingRequest(BaseModel):
    user_name: str = Field(default="Maria Gomez", description="Nombre real del usuario (PII) que sera enmascarado por el sistema")
    message: str = Field(
        ..., 
        description="Consulta de inversion en lenguaje natural",
        json_schema_extra={"example": "Tengo $1500 USD que me sobraron y quiero simular una inversion en BTC si sube a $80000"}
    )

class TradingResponse(BaseModel):
    response: str = Field(..., description="Explicacion y analisis detallado generado por el Agente LLM")
    demo_mode: bool = Field(..., description="Indica si la peticion se ejecuto en modo de demostracion offline")

# Instancia global del Agente de Finanzas (Inyeccion de Dependencia)
agent_manager = FinancialAgentManager(
    api_key=settings.GEMINI_API_KEY,
    model_name=settings.GEMINI_MODEL,
    demo_mode=settings.DEMO_MODE
)

# --- Middleware de Monitoreo de Procesamiento ---
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000
    
    # Obtener contexto de OpenTelemetry para correlacion de logs
    current_span = trace.get_current_span()
    ctx = current_span.get_span_context()
    trace_id_str = f"TraceId: {format(ctx.trace_id, '032x')}" if ctx.is_valid else "TraceId: None"
    span_id_str = f"SpanId: {format(ctx.span_id, '16x')}" if ctx.is_valid else "SpanId: None"
    
    # Log estructurado correlacionado con OpenTelemetry y latencia real (critico para medir p50 y p95)
    logger.info(
        f"[{trace_id_str} | {span_id_str}] "
        f"{request.method} {request.url.path} "
        f"→ {response.status_code} "
        f"[{process_time:.2f}ms]"
    )
    
    # Retornar tiempo de procesamiento en la cabecera
    response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
    return response

# --- Endpoints ---

@app.get("/", tags=["Sistema"])
def read_root():
    """Ruta raiz para verificar el estado de salud de la API"""
    return {
        "status": "online",
        "api": "Trading ROI Explainer & Transaction Simulator API",
        "mode": "DEMO (Offline)" if settings.DEMO_MODE else "REAL (Online)",
        "docs": "/docs",
        "security": "X-API-Key protegida",
        "config": {
            "model": settings.GEMINI_MODEL,
            "demo_mode": settings.DEMO_MODE
        }
    }

@app.post(
    "/api/v1/trading/explain", 
    response_model=TradingResponse, 
    tags=["Asesor Inteligente"],
    dependencies=[Depends(verify_api_key)]
)
async def explain_trading_roi(request: TradingRequest):
    """
    ENDPOINT CERRADO CON CLAVE (Sujeto a Autenticacion X-API-Key).
    Procesa una consulta financiera, enmascara el nombre real para proteccion de datos (PII),
    ejecuta el calculo financiero asincrono de comisiones y ROI, e invoca al LLM para explicarlo.
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="El mensaje de consulta no puede estar vacio.")
        
    try:
        explanation = await agent_manager.run_query(
            user_name=request.user_name,
            user_query=request.message
        )
        return TradingResponse(
            response=explanation,
            demo_mode=settings.DEMO_MODE
        )
    except IOError as ioe:
        logger.error(f"Error de consistencia de base de datos: {str(ioe)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(ioe)
        )
    except Exception as e:
        logger.error(f"Error procesando la peticion de trading: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor al procesar la transaccion: {str(e)}"
        )

# Endpoint adicional para compatibilidad con la estructura tradicional del laboratorio
@app.post(
    "/weather/explain", 
    response_model=TradingResponse, 
    tags=["Compatibilidad Laboratorio"],
    dependencies=[Depends(verify_api_key)]
)
async def explain_weather_alias(request: TradingRequest):
    """
    Alias /weather/explain mapeado directamente para cumplir de forma literal con el test del laboratorio
    utilizando el nuevo modelo financiero.
    """
    return await explain_trading_roi(request)
