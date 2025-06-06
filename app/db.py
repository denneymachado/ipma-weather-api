import sqlite3
import os
import json
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'ipma.db')

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS forecast_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            distrito TEXT NOT NULL,
            localidade TEXT NOT NULL,
            data DATE NOT NULL,
            conteudo TEXT NOT NULL,
            atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(distrito, localidade, data)
        )
    """)
    conn.commit()
    conn.close()

def get_cached_forecast(distrito: str, localidade: str, data: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT conteudo FROM forecast_cache
        WHERE distrito = ? AND localidade = ? AND data = ?
    """, (distrito, localidade, data))
    row = cursor.fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return None

def cache_forecast(distrito: str, localidade: str, data: str, conteudo: dict):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO forecast_cache (distrito, localidade, data, conteudo, atualizado_em)
        VALUES (?, ?, ?, ?, ?)
    """, (
        distrito,
        localidade,
        data,
        json.dumps(conteudo, ensure_ascii=False),
        datetime.utcnow()
    ))
    conn.commit()
    conn.close()
