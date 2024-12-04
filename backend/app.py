from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3
import requests
import os

API_URL = "https://api.energyzero.nl/v1/energyprices"

app = FastAPI()

# Expliciet de origins definiëren
origins = [
    "http://localhost:3000",
    "http://localhost",
    "http://localhost:80",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "/app/prices.db"

# Function to fetch and store prices
def fetch_prices():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        price = data.get("current_price")  # Adjust based on EnergyZero API structure
        if price is not None:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO prices (price) VALUES (?)", (price,))
            conn.commit()
            conn.close()

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS prices (id INTEGER PRIMARY KEY, price REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)"
    )
    conn.commit()
    conn.close()

@app.on_event("startup")
def on_startup():
    init_db()
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_prices, "interval", minutes=5)
    scheduler.start()

@app.get("/current-price")
def get_current_price():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT price, timestamp FROM prices ORDER BY timestamp DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"price": row[0], "timestamp": row[1]}
    return {"error": "No data available"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
