import requests
import unicodedata
import os
import json
import time

from app.localidade_map import LOCALIDADE_MAP  

CACHE_DIR = "data/cache"
os.makedirs(CACHE_DIR, exist_ok=True)

BASE_URL = "https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/{id}.json"

def normalize(text):
    """Remove maiúsculas e espaços"""
    return unicodedata.normalize("NFKC", text).strip().lower()


def get_forecast(distrito: str, localidade: str):
    from app.logger import logger 

    norm_distrito = normalize(distrito)
    norm_localidade = normalize(localidade)

    for key, id_local in LOCALIDADE_MAP.items():
        d, l = key.split("|")
        if normalize(d) == norm_distrito and normalize(l) == norm_localidade:
            local_id = id_local
            break
    else:
        raise ValueError("Distrito ou localidade não encontrados")

    # Tenta carregar do cache
    cached = load_from_cache(local_id)
    if cached:
        logger.info(f"Cache usado para {localidade}, {distrito}")
        payload = cached
    else:
        url = BASE_URL.format(id=local_id)
        response = requests.get(url)
        if response.status_code != 200:
            raise RuntimeError(f"Falha ao obter dados do IPMA: {response.status_code}")
        payload = response.json()
        save_to_cache(local_id, payload)
        logger.info(f"Nova requisição feita para {localidade}, {distrito}")

    forecast_data = payload.get("data", [])
    latitude = forecast_data[0].get("latitude") if forecast_data else None
    longitude = forecast_data[0].get("longitude") if forecast_data else None

    return {
        "localidade": f"{localidade.strip()}, {distrito.strip()}",
        "latitude": latitude,
        "longitude": longitude,
        "previsao": forecast_data
    }


def get_forecast_humanized(distrito: str, localidade: str):
    forecast_raw = get_forecast(distrito, localidade)
    dias = forecast_raw["previsao"]

    dias_pt = []
    for d in dias:
        dias_pt.append({
            "Data": d.get("forecastDate"),
            "Temperatura mínima (°C)": d.get("tMin"),
            "Temperatura máxima (°C)": d.get("tMax"),
            "Probabilidade de precipitação (%)": d.get("precipitaProb"),
            "Direção do vento": d.get("predWindDir"),
            "Velocidade do vento (km/h)": d.get("classWindSpeed")
        })

    return {
        "Localidade": forecast_raw["localidade"],
        "Previsão": dias_pt
    }

def load_from_cache(id_local):
    path = os.path.join(CACHE_DIR, f"{id_local}.json")
    if os.path.exists(path) and time.time() - os.path.getmtime(path) < 3600:
        with open(path, "r") as f:
            return json.load(f)
    return None

def save_to_cache(id_local, data):
    path = os.path.join(CACHE_DIR, f"{id_local}.json")
    with open(path, "w") as f:
        json.dump(data, f)
