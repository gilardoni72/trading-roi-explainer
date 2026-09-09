import pytest
from fastapi.testclient import TestClient
import sys
import os

# Asegurar que el directorio de codigo este en el PYTHONPATH para las importaciones
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Forzar DEMO_MODE para ejecucion de tests unitarios offline deterministas
os.environ["DEMO_MODE"] = "True"
os.environ["API_KEY"] = "test-secret-key-999"

from main import app, settings

client = TestClient(app)

def test_health_endpoint():
    """Verifica que la raiz de la API responda correctamente y este online"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"
    assert response.json()["mode"] == "DEMO (Offline)"

def test_explain_trading_endpoint_unauthorized_missing_header():
    """Verifica que el endpoint de trading falle con 401 si falta la cabecera X-API-Key"""
    payload = {
        "user_name": "Maria Gomez",
        "message": "Tengo $1500 USD y quiero invertir en BTC si llega a $80000"
    }
    response = client.post("/api/v1/trading/explain", json=payload)
    assert response.status_code == 401
    assert "cabecera 'X-API-Key' es requerida" in response.json()["detail"]

def test_explain_trading_endpoint_unauthorized_wrong_key():
    """Verifica que el endpoint falle con 401 si la clave es incorrecta"""
    payload = {
        "user_name": "Maria Gomez",
        "message": "Tengo $1500 USD y quiero invertir en BTC si llega a $80000"
    }
    headers = {"X-API-Key": "clave-erronea-de-prueba"}
    response = client.post("/api/v1/trading/explain", json=payload, headers=headers)
    assert response.status_code == 401
    assert "incorrecta" in response.json()["detail"]

def test_explain_trading_endpoint_authorized_success():
    """Verifica que el endpoint de trading responda 200 y realice el calculo y enmascaramiento con la clave correcta"""
    payload = {
        "user_name": "Maria Gomez",
        "message": "Tengo $1500 USD y quiero invertir en BTC si llega a $80000"
    }
    headers = {"X-API-Key": "test-secret-key-999"}
    response = client.post("/api/v1/trading/explain", json=payload, headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert "response" in data
    # El analisis debe reflejar el enmascaramiento de Maria Gomez (M**** G****) y los calculos de BTC
    assert "BTC" in data["response"]
    assert "M**** G****" in data["response"]
    assert "MOCK MODE" in data["response"]
    assert data["demo_mode"] is True

def test_explain_trading_endpoint_validation_empty_message():
    """Verifica que falle con 400 si el mensaje de consulta esta vacio"""
    payload = {
        "user_name": "Maria Gomez",
        "message": "   "
    }
    headers = {"X-API-Key": "test-secret-key-999"}
    response = client.post("/api/v1/trading/explain", json=payload, headers=headers)
    assert response.status_code == 400
    assert "vacio" in response.json()["detail"]

def test_explain_alias_endpoint_success():
    """Verifica que el alias de compatibilidad /weather/explain funcione correctamente"""
    payload = {
        "user_name": "Juan Perez",
        "message": "Tengo $500 usd para invertir en SOL si llega a $200"
    }
    headers = {"X-API-Key": "test-secret-key-999"}
    response = client.post("/weather/explain", json=payload, headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert "SOL" in data["response"]
    assert "J*** P****" in data["response"]
