import asyncio
import os
import sys
from langfuse import Langfuse

# Forzar codificacion UTF-8 para evitar errores de consola en Windows con Emojis
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Asegurar PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings
from agents.financial_agent import FinancialAgentManager

async def run_evaluation():
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
        
        # 2. Inicializar el agente de IA (Gemini 3.5)
        manager = FinancialAgentManager(
            api_key=settings.GEMINI_API_KEY,
            model_name=settings.GEMINI_MODEL,
            demo_mode=False
        )
        
        # 3. Iterar sobre cada caso de prueba del dataset
        for i, item in enumerate(dataset.items, 1):
            id_caso = item.metadata.get("id_caso", f"caso_{i}")
            user_name = item.input["user_name"]
            user_query = item.input["message"]
            
            print(f"\n[Fase 1/3] Procesando {id_caso} | Usuario: {user_name}...")
            print(f"Consulta: '{user_query}'")
            
            # Iniciar traza observada vinculada al ítem del dataset de Langfuse
            with item.observe(
                run_name="Evaluacion_Gemini3.5_Flash",
                metadata={"model": settings.GEMINI_MODEL}
            ) as trace:
                
                # Ejecutar consulta real a Gemini 3.5
                print(f"[Fase 2/3] Enviando consulta sanitizada a Gemini 3.5...")
                response_text = await manager.run_query(
                    user_name=user_name,
                    user_query=user_query,
                    stream=False
                )
                
                # Registrar la salida cognitiva de la generación de la evaluación
                print(f"[Fase 3/3] Registrando resultado en la nube de Langfuse...")
                trace.generation(
                    name="Evaluacion_LLM_Output",
                    model=settings.GEMINI_MODEL,
                    input=user_query,
                    output=response_text
                )
                
                print(f"✅ Caso {id_caso} completado y guardado con éxito.")
                
        print("\n" + "=" * 70)
        print("🎉 ¡Corrida de evaluación de Dataset completada exitosamente!")
        print("Revisa los reportes, comparativas y scores ingresando a:")
        print("👉 us.cloud.langfuse.com (Sección: Datasets -> trading_agent_evaluation)")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error al correr la evaluación del Dataset: {str(e)}")
        print("=" * 70)

if __name__ == "__main__":
    asyncio.run(run_evaluation())
