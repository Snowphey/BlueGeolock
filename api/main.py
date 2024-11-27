from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import asyncio
import json

app = FastAPI()

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paramètres de connexion PostgreSQL
pg_params = {
    'dbname': 'gps_tracking',
    'user': 'postgres',
    'password': 'tracking_password',
    'host': 'postgres'
}

@app.get("/latest_coordinates")
async def get_latest_coordinates():
    conn = psycopg2.connect(**pg_params)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT machine_id, latitude, longitude, timestamp 
        FROM (
            SELECT machine_id, latitude, longitude, timestamp,
                   ROW_NUMBER() OVER (PARTITION BY machine_id ORDER BY timestamp DESC) as rn
            FROM gps_coordinates
        ) t 
        WHERE rn = 1
    """)
    
    results = cursor.fetchall()
    coordinates = [
        {
            "machine_id": row[0],
            "latitude": row[1],
            "longitude": row[2],
            "timestamp": row[3].isoformat()
        } for row in results
    ]
    
    conn.close()
    return coordinates

@app.websocket("/ws/coordinates")
async def websocket_coordinates(websocket: WebSocket):
    await websocket.accept()

    conn = psycopg2.connect(**pg_params)

    while True:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT ON (machine_id) 
                machine_id,
                latitude,
                longitude,
                timestamp
            FROM gps_coordinates
            ORDER BY machine_id, timestamp DESC;
        """)
        
        results = cursor.fetchall()
        coordinates = [
            {
                "machine_id": row[0],
                "latitude": float(row[1]),
                "longitude": float(row[2]),
                "timestamp": row[3].isoformat()
            } for row in results
        ]
        
        await websocket.send_json(coordinates)
        await asyncio.sleep(5)