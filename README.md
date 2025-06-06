# IPMA Weather API 🇵🇹

REST API para previsão do tempo em Portugal, com dados públicos fornecidos pelo IPMA (Instituto Português do Mar e da Atmosfera).

> Projetado para ser simples, acessível e utilizável tanto por pessoas quanto por sistemas automatizados.

---

## 🌐 Endpoints disponíveis

### `/previsao`
Previsão técnica completa para uma localidade/distrito.
- **Parâmetros**: `distrito`, `localidade`, `format=json|csv`
- **Exemplo**: `/previsao?distrito=Lisboa&localidade=Lisboa`
- 🔄 Usa cache local com SQLite para evitar chamadas repetidas à API externa.

### `/previsao-usuario`
Versão amigável da previsão, com títulos compreensíveis e dados simplificados.
- **Parâmetros**: `distrito`, `localidade`, `format=json|csv`
- **Exemplo**: `/previsao-usuario?distrito=Lisboa&localidade=Lisboa`

### `/locais-disponiveis`
Lista todos os pares `distrito|localidade` disponíveis para consulta.

### `/status`
Mostra informações sobre o tempo de execução da API, itens em cache e arquivos de log.

### `/docs`
Interface interativa de documentação Swagger para teste e exploração da API.

---

## 🗃️ Cache em SQLite

A API utiliza cache local persistente em SQLite. As previsões são armazenadas por `distrito`, `localidade` e `data`, e são reaproveitadas automaticamente em chamadas subsequentes, otimizando a performance.

Local: `data/ipma.db`

---

## 🚀 Como executar localmente

### Docker (recomendado)

```bash
make build
make run
```

Ou manualmente:

```bash
docker build -t ipma-api .
docker run -it --rm -p 8000:8000 -v $(pwd)/data:/app/data ipma-api
```

Acesse em: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Testes automatizados

Rodar todos os testes com:

```bash
make test
```

Ou diretamente:

```bash
PYTHONPATH=. pytest tests/
```

---

## 📁 Estrutura de diretórios

```
ipma_weather_api/
├── app/
│   ├── main.py
│   ├── scraper.py
│   ├── logger.py
│   ├── localidade_map.py
│   ├── db.py
│   └── static/
│       └── favicon.ico
├── data/
│   ├── ipma.db
│   ├── cache/
│   └── logs/
├── tests/
│   └── test_api.py
├── Dockerfile
├── requirements.txt
├── Makefile
├── pytest.ini
├── README.md
└── .gitignore
```

---

## ⚖️ Licença

Este projeto está licenciado sob a [MIT License](https://opensource.org/licenses/MIT), permitindo uso livre, modificação e distribuição com atribuição adequada.

---

## 📬 Contacto

Desenvolvido por: **Denney Machado**  
LinkedIn: https://www.linkedin.com/in/denneymachado/