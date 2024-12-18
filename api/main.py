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
        SELECT first_name, last_name, latitude, longitude, timestamp 
        FROM (
            SELECT first_name, last_name, latitude, longitude, timestamp,
                   ROW_NUMBER() OVER (PARTITION BY first_name, last_name ORDER BY timestamp DESC) as rn
            FROM gps_coordinates
        ) t 
        WHERE rn = 1
    """)
    
    results = cursor.fetchall()
    coordinates = [
        {
            "first_name": row[0],
            "last_name": row[1],
            "latitude": row[2],
            "longitude": row[3],
            "timestamp": row[4].isoformat()
        } for row in results
    ]
    
    conn.close()
    return coordinates

@app.websocket("/ws/coordinates")
async def websocket_coordinates(websocket: WebSocket):
    await websocket.accept()
    conn = psycopg2.connect(**pg_params)

    try:
        while True:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT ON (first_name, last_name) 
                    first_name,
                    last_name,
                    latitude,
                    longitude,
                    timestamp
                FROM gps_coordinates
                ORDER BY first_name, last_name, timestamp DESC;
            """)
            
            results = cursor.fetchall()
            coordinates = [
                {
                    "first_name": row[0],
                    "last_name": row[1],
                    "latitude": float(row[2]),
                    "longitude": float(row[3]),
                    "timestamp": row[4].isoformat()
                } for row in results
            ]
            
            await websocket.send_json(coordinates)
            await asyncio.sleep(1)  # Adjust the sleep time as needed
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM gps_coordinates")
        conn.commit()
        conn.close()
        await websocket.close()