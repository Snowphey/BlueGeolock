import json
import psycopg2
from kafka import KafkaConsumer

class GPSConsumer:
    def __init__(self, bootstrap_servers, topic, pg_params):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset='latest',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        self.pg_conn = psycopg2.connect(**pg_params)
        self.pg_cursor = self.pg_conn.cursor()

    def consume_and_store(self):
        for message in self.consumer:
            coords = message.value
            self.store_coordinates(coords)

    def store_coordinates(self, coords):
        query = """
        INSERT INTO gps_coordinates (first_name, last_name, latitude, longitude)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (first_name, last_name)
        DO UPDATE SET latitude = EXCLUDED.latitude, longitude = EXCLUDED.longitude, timestamp = now();
        """
        self.pg_cursor.execute(query, (
            coords['first_name'],
            coords['last_name'], 
            coords['latitude'], 
            coords['longitude']
        ))
        self.pg_conn.commit()

# Paramètres de connexion PostgreSQL
pg_params = {
    'dbname': 'gps_tracking',
    'user': 'postgres',
    'password': 'tracking_password',
    'host': 'postgres'
}

consumer = GPSConsumer(['kafka:9092'], 'coordinates', pg_params)
consumer.consume_and_store()