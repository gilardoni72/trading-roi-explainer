import asyncio
import os
import sys
import random

# Forzar codificacion UTF-8 para evitar errores de consola en Windows con Emojis
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Asegurar PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings
from agents.financial_agent import FinancialAgentManager

async def generate_dashboard_data():
    print("=" * 70)
    print("📊 POBLANDO DASHBOARD DE LANGFUSE CLOUD CON DATOS SIMULADOS")
    print("=" * 70)
    
    # Verificar credenciales de Langfuse
    if not os.environ.get("LANGFUSE_PUBLIC_KEY") or not os.environ.get("LANGFUSE_SECRET_KEY"):
        print("❌ Error: Las credenciales de Langfuse no están configuradas en tu archivo .env")
        print("Por favor, configura tu LANGFUSE_PUBLIC_KEY y LANGFUSE_SECRET_KEY.")
        return

    manager = FinancialAgentManager(
        api_key=settings.GEMINI_API_KEY,
        model_name=settings.GEMINI_MODEL,
        demo_mode=False
    )
    
    usuarios_demo = [
        "Marcelo Gilardoni", "Maria Gomez", "Juan Perez", "Carlos Ruiz", 
        "Ricardo Montalban", "Luis Miguel", "Shakira Ripoll", "Elon Musk", 
        "Lionel Messi", "Warren Buffett"
    ]
    
    activos = ["BTC", "ETH", "SOL"]
    
    consultas = [
        "Simular una inversion de ${monto} en {activo} si sube a {meta}",
        "Tengo ${monto} usd y quiero ver mi ROI en {activo} con meta de {meta}",
        "Quiero simular con {activo} un capital de ${monto} a {meta}",
        "Como se comportarian ${monto} en {activo} si llega a {meta}?"
    ]
    
    total_simulaciones = 12
    print(f"Lanzando {total_simulaciones} simulaciones aleatorias para poblar tus graficos...")
    
    for i in range(1, total_simulaciones + 1):
        user = random.choice(usuarios_demo)
        activo = random.choice(activos)
        
        # Definir precios base realistas para las metas
        base_price = 77000.0 if activo == "BTC" else (3500.0 if activo == "ETH" else 150.0)
        monto = random.randint(100, 5000)
        meta = round(base_price * random.uniform(1.10, 1.40), 2)
        
        query_template = random.choice(consultas)
        query = query_template.format(monto=monto, activo=activo, meta=meta)
        
        print(f"\n[{i:02d}/{total_simulaciones}] Procesando: {user} | {activo} | ${monto} USD...")
        
        try:
            # Ejecutar la simulación asíncrona real
            await manager.run_query(
                user_name=user,
                user_query=query,
                stream=False
            )
            print(f"✅ Transacción #{i:02d} guardada en base de datos e inyectada en Langfuse Cloud.")
            # Esperar una pequeña pausa para no saturar las cuotas de la API gratis (15 RPM max)
            await asyncio.sleep(4.0)
            
        except Exception as e:
            print(f"⚠️ Error en simulacion #{i}: {str(e)}")
            await asyncio.sleep(2.0)
            
    print("\n" + "=" * 70)
    print("🎉 ¡DASHBOARD POBLADO EXITOSAMENTE CON DATOS REALES!")
    print("Ingresa a us.cloud.langfuse.com y haz clic en 'Dashboards' o 'Tracing' para ver")
    print("tus graficos de costo en USD, conteo de tokens y uso de modelos cobrando vida.")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(generate_dashboard_data())
