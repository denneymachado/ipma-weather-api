from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse, Response, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import csv
import io
import os
import time
from app.scraper import get_forecast, get_forecast_humanized
from app.logger import logger
from app.localidade_map import LOCALIDADE_MAP
from app.db import init_db, get_cached_forecast, cache_forecast
from datetime import date

init_db()

app = FastAPI(
    title="IPMA Weather API",
    description="API para previsão do tempo em Portugal com base no IPMA",
    version="1.0.0"
)

start_time = time.time()

# Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monta pasta de estáticos e favicon
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round((time.time() - start) * 1000)
    client_host = request.client.host
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {duration}ms - IP: {client_host}")
    return response

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(os.path.join("app", "static", "favicon.ico"))

@app.get("/previsao", summary="Previsão técnica", description="Retorna previsão detalhada para programadores, pesquisadores e sistemas.")
def previsao(distrito: str, localidade: str, format: str = Query("json", enum=["json", "csv"])):
    try:
        hoje = str(date.today())
        cache = get_cached_forecast(distrito, localidade, hoje)
        
        if cache:
            data = cache
        else:
            data = get_forecast(distrito, localidade)
            cache_forecast(distrito, localidade, hoje, data)

        if format == "csv":
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=data["previsao"][0].keys())
            writer.writeheader()
            writer.writerows(data["previsao"])
            return Response(
                content=output.getvalue(),
                media_type="text/csv",
                headers={"Content-Disposition": "attachment; filename=previsao.csv"}
            )


        return JSONResponse(content=data)

    except Exception as e:
        logger.error(f"Erro em /previsao: {e}")
        return JSONResponse(status_code=400, content={"detail": str(e)})
    
@app.get("/previsao-usuario", summary="Previsão para meros mortais", description="Retorna previsão com variáveis simples para usuários comuns.")
def previsao_usuario(distrito: str, localidade: str, format: str = Query("json", enum=["json", "csv"])):
    try:
        data = get_forecast_humanized(distrito, localidade)

        if format == "csv":
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=data["Previsão"][0].keys())
            writer.writeheader()
            writer.writerows(data["Previsão"])
            return Response(
                content=output.getvalue(),
                media_type="text/csv",
                headers={"Content-Disposition": "attachment; filename=previsao.csv"}
            )


        return JSONResponse(content=data)

    except Exception as e:
        logger.error(f"Erro em /previsao-usuario: {e}")
        return JSONResponse(status_code=400, content={"detail": str(e)})

@app.get("/status", summary="Status da API", description="Mostra o tempo de atividade e uso de cache/logs.")
def status():
    uptime_seconds = int(time.time() - start_time)
    horas, resto = divmod(uptime_seconds, 3600)
    minutos, segundos = divmod(resto, 60)
    uptime_str = f"{horas}h {minutos}min {segundos}s"

    num_logs = len(os.listdir("data/logs")) if os.path.exists("data/logs") else 0
    num_cache = len(os.listdir("data/cache")) if os.path.exists("data/cache") else 0

    return {
        "status": "ok",
        "uptime": uptime_str,
        "itens_em_cache": num_cache,
        "arquivos_de_log": num_logs
    }

@app.get("/locais-disponiveis", summary="Lista de localidades disponíveis", description="Retorna todos os pares distrito/localidade válidos.")
def locais_disponiveis():
    locais = sorted(list(LOCALIDADE_MAP.keys()))
    return {"locais": locais}
