FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante da aplicação
COPY app /app/app

# Garante que o diretório de dados exista
RUN mkdir -p /app/data

# Expõe a porta da aplicação
EXPOSE 8000

# Comando para iniciar o servidor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
