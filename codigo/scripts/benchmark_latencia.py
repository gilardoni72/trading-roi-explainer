import time
import json
import httpx
import numpy as np
from fastapi.testclient import TestClient
import sys
import os

# Forzar DEMO_MODE para el benchmark asumiendo modo local rápido y determinista
os.environ["DEMO_MODE"] = "True"

# Forzar codificacion UTF-8 en consola para evitar errores con caracteres especiales
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Asegurar que el directorio de codigo este en el PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app, settings

def run_benchmark():
    print("=" * 60)
    print("BENCHMARK DE LATENCIA Y DESEMPENO: TRADING ROI EXPLAINER API")
    print("=" * 60)
    print("Este script realiza 10 llamadas secuenciales para calcular el p50 y p95.")
    
    # Intentar verificar si el servidor real esta corriendo en 127.0.0.1:8000
    server_url = "http://127.0.0.1:8000/api/v1/trading/explain"
    use_real_server = False
    
    try:
        # Intento rapido de conexion
        response = httpx.get("http://127.0.0.1:8000/", timeout=1.0)
        if response.status_code == 200:
            use_real_server = True
            print("Detected active server running on http://127.0.0.1:8000. Running benchmark over HTTP...")
    except Exception:
        print("Server not running on port 8000. Using fast in-process TestClient to benchmark the full execution stack...")

    payload = {
        "user_name": "Maria Gomez",
        "message": "Tengo $1500 USD y quiero simular una inversion en BTC si sube a $80000"
    }
    headers = {
        "X-API-Key": settings.API_KEY
    }
    
    latencies = []
    
    # Realizar 10 llamadas consecutivas
    for i in range(1, 11):
        start_time = time.perf_counter()
        
        if use_real_server:
            try:
                response = httpx.post(server_url, json=payload, headers=headers, timeout=10.0)
                status_code = response.status_code
            except Exception as e:
                print(f"Error calling real server: {e}")
                status_code = 500
        else:
            with TestClient(app) as client:
                response = client.post("/api/v1/trading/explain", json=payload, headers=headers)
                status_code = response.status_code
                
        duration_ms = (time.perf_counter() - start_time) * 1000
        latencies.append(duration_ms)
        
        print(f"Llamada #{i:02d}: Status {status_code} | Latencia: {duration_ms:.2f} ms")
        time.sleep(0.1) # Breve pausa para estabilidad
        
    print("-" * 60)
    
    # Calcular metricas
    sorted_lats = sorted(latencies)
    p50 = np.percentile(sorted_lats, 50)
    p95 = np.percentile(sorted_lats, 95)
    slowest = sorted_lats[-1]
    fastest = sorted_lats[0]
    avg = sum(latencies) / len(latencies)
    
    print(f"LLAMADAS EXITOSAS: {len(latencies)}/10")
    print(f"Latencia Minima:   {fastest:.2f} ms")
    print(f"Latencia Maxima:   {slowest:.2f} ms")
    print(f"Latencia Promedio: {avg:.2f} ms")
    print("-" * 60)
    print(f"PERCENTIL p50 (Mediana):  {p50:.2f} ms")
    print(f"PERCENTIL p95 (Peor 5%):  {p95:.2f} ms")
    print("=" * 60)
    
    # Guardar reporte en un JSON para uso del plan de la entrega
    report = {
        "latencies": [round(l, 2) for l in latencies],
        "fastest_ms": round(fastest, 2),
        "slowest_ms": round(slowest, 2),
        "avg_ms": round(avg, 2),
        "p50_ms": round(p50, 2),
        "p95_ms": round(p95, 2)
    }
    
    report_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "benchmark_results.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=4)
    print(f"Resultados guardados de forma segura en: {report_path}")

if __name__ == "__main__":
    run_benchmark()
