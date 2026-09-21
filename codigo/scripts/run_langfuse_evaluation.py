import asyncio
import os
import sys
import json
import nest_asyncio
from langfuse import Langfuse

# Permitir bucles de eventos anidados para evitar conflictos con nest_asyncio en entornos interactivos
nest_asyncio.apply()

# Forzar codificacion UTF-8 para evitar errores de consola en Windows con Emojis
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Asegurar PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings
from agents.financial_agent import FinancialAgentManager

# Instanciar el agente de IA (Gemini 3.5)
manager = FinancialAgentManager(
    api_key=settings.GEMINI_API_KEY,
    model_name=settings.GEMINI_MODEL,
    demo_mode=False
)

async def evaluate_item(*, item, **kwargs):
    """
    Función de tarea asíncrona nativa para procesar cada ítem del dataset.
    """
    user_name = item.input["user_name"]
    user_query = item.input["message"]
    
    print(f"\n[Evaluando] ID: {item.id} | Usuario: {user_name}...")
    print(f"Consulta: '{user_query}'")
    
    try:
        response_text = await manager.run_query(
            user_name=user_name,
            user_query=user_query,
            stream=False
        )
        print("✅ Simulación completada con éxito.")
        return response_text
    except Exception as e:
        print(f"❌ Error procesando ítem: {str(e)}")
        return f"Error: {str(e)}"

async def run_evaluation_async():
    print("=" * 70)
    print("🚀 INICIANDO CORRIDA DE EVALUACIÓN SOBRE EL DATASET EN LANGFUSE CLOUD")
    print("=" * 70)
    
    # Verificar si están las credenciales configuradas
    if not os.environ.get("LANGFUSE_PUBLIC_KEY") or not os.environ.get("LANGFUSE_SECRET_KEY"):
        print("❌ Error: Las credenciales de Langfuse no están configuradas en tu archivo .env")
        print("Por favor, configura LANGFUSE_PUBLIC_KEY y LANGFUSE_SECRET_KEY antes de continuar.")
        return

    langfuse = Langfuse()
    dataset_name = "trading_agent_evaluation"
    
    try:
        # 1. Obtener el dataset de la nube
        print(f"[Langfuse] Descargando dataset '{dataset_name}' de la nube...")
        dataset = langfuse.get_dataset(dataset_name)
        
        # 2. Correr la evaluación de forma nativa utilizando 'run_experiment' de Langfuse
        # Esto crea automáticamente las trazas, las asocia al dataset y las sube a la nube.
        print(f"[Langfuse] Iniciando experimento asíncrono con {len(dataset.items)} casos de prueba...")
        results = dataset.run_experiment(
            name="Evaluacion_Gemini3.5_Flash",
            run_name="Run_Marcelo_Gilardoni",
            task=evaluate_item
        )
        
        # 3. Forzar el flush de todas las trazas de evaluacion antes de salir
        print("[Langfuse] Sincronizando y subiendo trazas pendientes a la nube...")
        langfuse.flush()
                
        print("\n" + "=" * 70)
        print("🎉 ¡Corrida de evaluación de Dataset completada exitosamente!")
        print("Revisa los reportes, comparativas y scores ingresando a:")
        print("👉 us.cloud.langfuse.com (Sección: Datasets -> trading_agent_evaluation)")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error al correr la evaluación del Dataset: {str(e)}")
        print("=" * 70)

def main():
    asyncio.run(run_evaluation_async())

if __name__ == "__main__":
    main()
