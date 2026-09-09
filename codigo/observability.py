import logging
import sys
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Forzar codificacion UTF-8 para evitar problemas de consola con caracteres especiales en Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Inicializar un Tracer Provider centralizado
provider = TracerProvider()

# Configurar un Exportador de Consola Simple para demostrar trazas impresas de forma espectacular
console_exporter = ConsoleSpanExporter(
    out=sys.stdout, 
    formatter=lambda span: f"[OTel Span] '{span.name}' | Parent: {span.parent.span_id if span.parent else 'None'} | Status: {span.status.status_code} | Duration: {(span.end_time - span.start_time) / 1000000:.2f}ms\n"
)
provider.add_span_processor(SimpleSpanProcessor(console_exporter))

# Registrar el proveedor de manera global en el framework de OpenTelemetry
trace.set_tracer_provider(provider)

# Crear el Tracer para instrumentar nuestras capas de negocio
tracer = trace.get_tracer("trading-explainer-api")

def instrument_app(app):
    """
    Instrumenta automaticamente FastAPI para registrar trazas HTTP web.
    """
    FastAPIInstrumentor.instrument_app(app)
