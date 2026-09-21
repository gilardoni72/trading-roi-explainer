import os
import sys
import json
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

    jsonl_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tests", "casos_ejemplo_trading.jsonl")
    if not os.path.exists(jsonl_path):
        print(f"❌ Error: No se encontró el archivo de casos en: {jsonl_path}")
        return

    langfuse = Langfuse()
    dataset_name = "trading_agent_evaluation"
    
    try:
        # 1. Crear el dataset en la nube
        print(f"[Langfuse] Creando dataset '{dataset_name}' en la nube...")
        dataset = langfuse.create_dataset(
            name=dataset_name,
            description="Dataset oficial de 20 casos de prueba para auditar calidad, enmascaramiento y consistencia (Marcelo Gilardoni)"
        )
        
        # 2. Leer dinámicamente los 20 ítems del archivo .jsonl
        print(f"[Langfuse] Leyendo casos de prueba desde: {jsonl_path}")
        test_cases = []
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    test_cases.append(json.loads(line.strip()))
        
        # 3. Subir los 20 ítems al dataset de Langfuse Cloud
        for i, case in enumerate(test_cases, 1):
            print(f"[Langfuse] Subiendo caso de prueba #{i:02d} ({case['id']})...")
            langfuse.create_dataset_item(
                dataset_name=dataset_name,
                input=case["input"],
                expected_output=case["expected_output"],
                metadata={"id_caso": case["id"]}
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
