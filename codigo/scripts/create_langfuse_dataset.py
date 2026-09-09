import os
import sys
from langfuse import Langfuse

# Forzar codificacion UTF-8 para evitar errores de consola en Windows con Emojis
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Asegurar PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings

def create_dataset():
    print("=" * 70)
    print("📈 CREANDO DATASET DE EVALUACIÓN EN LANGFUSE CLOUD")
    print("=" * 70)
    
    # Verificar si están las credenciales configuradas
    if not os.environ.get("LANGFUSE_PUBLIC_KEY") or not os.environ.get("LANGFUSE_SECRET_KEY"):
        print("❌ Error: Las credenciales de Langfuse no están configuradas en tu archivo .env")
        print("Por favor, configura LANGFUSE_PUBLIC_KEY y LANGFUSE_SECRET_KEY antes de continuar.")
        return

    langfuse = Langfuse()
    dataset_name = "trading_agent_evaluation"
    
    try:
        # 1. Crear el dataset en la nube
        print(f"[Langfuse] Creando dataset '{dataset_name}' en la nube...")
        dataset = langfuse.create_dataset(
            name=dataset_name,
            description="Dataset oficial para evaluar calidad, enmascaramiento y consistencia del Asesor de Trading (Marcelo Gilardoni)"
        )
        
        # 2. Definir los ítems del dataset
        test_cases = [
            {
                "input": {
                    "user_name": "Maria Gomez",
                    "message": "Tengo $1500 USD y quiero simular una inversion en BTC si sube a $80000"
                },
                "expected_output": "Debe dirigirse al usuario como 'M**** G****', deducir $7.50 USD de comisión (0.5%) y calcular un ROI de 1.36%."
            },
            {
                "input": {
                    "user_name": "Juan Perez",
                    "message": "Tengo $500 usd para invertir en SOL si llega a $200"
                },
                "expected_output": "Debe dirigirse al usuario como 'J*** P****', deducir $2.50 USD de comisión (0.5%) y calcular la tenencia de SOL basada en $497.50 netos."
            },
            {
                "input": {
                    "user_name": "Carlos Ruiz",
                    "message": "Quiero simular con ETH $1000 con meta de $4000"
                },
                "expected_output": "Debe dirigirse al usuario como 'C***** R***', deducir $5.00 USD de comisión (0.5%) y calcular el ROI correspondiente de Ethereum."
            }
        ]
        
        # 3. Subir los ítems al dataset
        for i, case in enumerate(test_cases, 1):
            print(f"[Langfuse] Subiendo caso de prueba #{i} (Usuario: {case['input']['user_name']})...")
            dataset.create_item(
                input=case["input"],
                expected_output=case["expected_output"],
                metadata={"id_caso": f"caso_prueba_{i}"}
            )
            
        print("\n" + "=" * 70)
        print(f"✅ ¡Dataset '{dataset_name}' creado con {len(test_cases)} casos de prueba cargados con éxito!")
        print("Puedes visualizar el Dataset ingresando a tu consola en us.cloud.langfuse.com")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error al crear el Dataset: {str(e)}")
        print("Verifica que tus claves LANGFUSE_PUBLIC_KEY y LANGFUSE_SECRET_KEY en '.env' sean las correctas.")
        print("=" * 70)

if __name__ == "__main__":
    create_dataset()
