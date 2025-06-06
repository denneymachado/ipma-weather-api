# Nome da imagem Docker
IMAGE_NAME = ipma-api

# Caminho do diretório do app
APP_DIR = app

# Caminho do diretório de dados
DATA_DIR = data

# Comando para ativar virtualenv local
VENV_ACTIVATE = . .venv/bin/activate

# ========================================
# CONSTRUÇÃO E EXECUÇÃO COM DOCKER
# ========================================

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run -it --rm -p 8000:8000 -v $(PWD)/$(DATA_DIR):/app/$(DATA_DIR) $(IMAGE_NAME)

# ========================================
# DESENVOLVIMENTO LOCAL
# ========================================

dev:
	uvicorn $(APP_DIR).main:app --reload --host 127.0.0.1 --port 8000

# ========================================
# TESTES E DEPENDÊNCIAS
# ========================================

test:
	PYTHONPATH=. pytest tests/

deps:
	pip install -r requirements.txt

# ========================================
# LIMPEZA
# ========================================

clean:
	rm -rf $(DATA_DIR)/cache/*.json
	rm -rf $(DATA_DIR)/logs/*.log
	find . -type d -name "__pycache__" -exec rm -r {} +
