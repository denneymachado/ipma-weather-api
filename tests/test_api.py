import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.parametrize("endpoint,params", [
    ("/previsao", {"distrito": "Lisboa", "localidade": "Lisboa"}),
    ("/previsao-usuario", {"distrito": "Lisboa", "localidade": "Lisboa"}),
    ("/status", {}),
    ("/locais-disponiveis", {})
])
def test_endpoints_status_code_200(endpoint, params):
    response = client.get(endpoint, params=params)
    assert response.status_code == 200

def test_previsao_json_format():
    response = client.get("/previsao", params={"distrito": "Lisboa", "localidade": "Lisboa", "format": "json"})
    assert response.status_code == 200
    data = response.json()
    assert "previsao" in data
    assert isinstance(data["previsao"], list)

def test_previsao_csv_format():
    response = client.get("/previsao", params={"distrito": "Lisboa", "localidade": "Lisboa", "format": "csv"})
    assert response.status_code == 200
    assert "text/csv" in response.headers["Content-Type"]
    assert "forecastDate" in response.text  # CSV header expected

def test_locais_disponiveis_content():
    response = client.get("/locais-disponiveis")
    assert response.status_code == 200
    data = response.json()
    assert "locais" in data
    assert isinstance(data["locais"], list)
    assert any("Aveiro" in item for item in data["locais"])

