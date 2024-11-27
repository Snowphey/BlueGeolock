import json
import time
import socket
import random
import math
from kafka import KafkaProducer
import threading

class RealisticGPSProducer:
    def __init__(self, machine_id, bootstrap_servers, topic, base_lat, base_lon, max_speed_km_per_hour=50):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.topic = topic
        self.machine_id = machine_id
        
        # État initial
        self.current_lat = base_lat
        self.current_lon = base_lon
        
        # Paramètres de mouvement
        self.max_speed = max_speed_km_per_hour / 3600  # conversion en degrés/seconde
        self.direction = random.uniform(0, 2 * math.pi)  # Direction initiale aléatoire

    def haversine_distance(self, lat1, lon1, lat2, lon2):
        """Calcule la distance entre deux points GPS"""
        R = 6371  # Rayon de la Terre en km
        
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat/2)**2 + 
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c

    def generate_next_coordinates(self):
        """
        Génère des coordonnées cohérentes basées sur un mouvement brownien
        avec des changements de direction graduels
        """
        # Changement de direction minimal (+-15 degrés)
        direction_change = random.uniform(-math.pi/12, math.pi/12)
        self.direction += direction_change

        # Calcul du déplacement
        dx = self.max_speed * math.cos(self.direction)
        dy = self.max_speed * math.sin(self.direction)

        # Conversion des degrés
        new_lat = self.current_lat + dy / 111  # 1 degré latitude ≈ 111 km
        new_lon = self.current_lon + dx / (111 * math.cos(math.radians(self.current_lat)))

        return {
            'id': self.machine_id,
            'latitude': new_lat,
            'longitude': new_lon,
            'speed': self.max_speed * 3600,  # km/h
            'direction': math.degrees(self.direction)
        }

    def update_current_position(self, new_coords):
        """Met à jour la position courante"""
        self.current_lat = new_coords['latitude']
        self.current_lon = new_coords['longitude']

    def send_coordinates(self):
        while True:
            coords = self.generate_next_coordinates()
            self.producer.send(self.topic, key=self.machine_id.encode(), value=coords)
            self.update_current_position(coords)
            
            # Temps d'attente pour simuler un déplacement réaliste
            time.sleep(5)  # Mise à jour toutes les 5 secondes

# Configurations pour deux machines
# IP1: Un trajet autour de Paris
producer_ip1 = RealisticGPSProducer(
    machine_id='ip1',
    bootstrap_servers=['kafka:9092'], 
    topic='coordinates', 
    base_lat=48.8566,  # Latitude de Paris
    base_lon=2.3522,   # Longitude de Paris
    max_speed_km_per_hour=50  # 50 km/h
)

# IP2: Un trajet autour de Lyon
producer_ip2 = RealisticGPSProducer(
    machine_id='ip2',
    bootstrap_servers=['kafka:9092'], 
    topic='coordinates', 
    base_lat=45.7640,  # Latitude de Lyon
    base_lon=4.8357,   # Longitude de Lyon
    max_speed_km_per_hour=70  # 70 km/h
)

# Lancement des producers
threading.Thread(target=producer_ip1.send_coordinates).start()
threading.Thread(target=producer_ip2.send_coordinates).start()