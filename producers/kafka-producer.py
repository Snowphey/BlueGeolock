import json
import threading
import time
import sys
import os
from flask import Flask, request, jsonify
import subprocess
from kafka import KafkaProducer
from typing import Dict, List, Tuple
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

class FootballPlayerProducer:
    def __init__(self, player_data: Dict, bootstrap_servers: List[str], topic: str):
        """
        Initialize a Kafka producer for a football player
        
        :param player_data: Dictionary containing player details
        :param bootstrap_servers: List of Kafka bootstrap servers
        :param topic: Kafka topic to publish coordinates
        """
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
        self.player_data = player_data
        self.topic = topic
        
        # Initial position
        self.current_lat = player_data['latitude']
        self.current_lon = player_data['longitude']
        
        # Movement constraints based on role
        self.movement_constraints = {
            'goalkeeper': (0.001, 0.005),  # Smaller area near initial position
            'central_defender': (0.002, 0.01),  # Moderate movement area
            'left_defender': (0.001, 0.008),
            'right_defender': (0.001, 0.008),
            'defensive_midfielder': (0.002, 0.01),
            'offensive_midfielder': (0.003, 0.015),
            'left_winger': (0.002, 0.01),
            'right_winger': (0.002, 0.01),
            'striker': (0.003, 0.015)  # Larger movement area
        }
        self.running = True
        
    def generate_new_position(self) -> Tuple[float, float]:
        """
        Generate a new position based on player's role and initial position
        
        :return: Tuple of (latitude, longitude)
        """
        import random
        role = self.player_data['role']
        min_distance, max_distance = self.movement_constraints[role]
        
        # Random walk with role-based constraints and team bias
        lat_change = random.uniform(-max_distance, max_distance)
        lon_change = random.uniform(-max_distance, max_distance)
        
        new_lat = max(0, min(1, self.current_lat + lat_change))
        new_lon = max(0, min(1, self.current_lon + lon_change))
        
        return new_lat, new_lon
    
    def publish_position(self):
        """
        Publish player's position to Kafka topic
        """
        new_lat, new_lon = self.generate_new_position()
        
        # Update current position
        self.current_lat = new_lat
        self.current_lon = new_lon
        
        # Prepare message
        message = {
            'first_name': self.player_data['first_name'],
            'last_name': self.player_data['last_name'],
            'latitude': new_lat,
            'longitude': new_lon
        }
        
        # Publish to Kafka
        self.producer.send(self.topic, message)
        self.producer.flush()
    
    def start_publishing(self, interval: float = 2.0):
        """
        Start continuously publishing player positions
        
        :param interval: Time between position updates in seconds
        """
        try:
            while self.running:
                self.publish_position()
                time.sleep(interval)
        except KeyboardInterrupt:
            print(f"Stopping producer for {self.player_data['first_name']} {self.player_data['last_name']}")
        finally:
             self.producer.close()
    
    def stop(self):
        self.running = False

class BallProducer:
    def __init__(self, bootstrap_servers: List[str], topic: str):
        """
        Special producer for the ball with more random movement
        """
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
        self.topic = topic
        
        # Initial ball position (middle of the field)
        self.current_lat = 0.5
        self.current_lon = 0.5
        self.running = True
    
    def generate_new_position(self) -> Tuple[float, float]:
        """
        Generate more random ball movement
        """
        import random
        lat_change = random.uniform(-0.002, 0.002)
        lon_change = random.uniform(-0.002, 0.002)
        
        new_lat = max(0, min(1, self.current_lat + lat_change))
        new_lon = max(0, min(1, self.current_lon + lon_change))
        
        return new_lat, new_lon
    
    def publish_position(self):
        """
        Publish ball's position to Kafka topic
        """
        new_lat, new_lon = self.generate_new_position()
        
        # Update current position
        self.current_lat = new_lat
        self.current_lon = new_lon
        
        # Prepare message
        message = {
            'first_name': 'Football',
            'last_name': 'Ball',
            'latitude': new_lat,
            'longitude': new_lon
        }
        
        # Publish to Kafka
        self.producer.send(self.topic, message)
        self.producer.flush()
    
    def start_publishing(self, interval: float = 2.0):
        """
        Start continuously publishing ball positions
        
        :param interval: Time between position updates in seconds
        """
        try:
            while self.running:
                self.publish_position()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("Stopping ball producer")
        finally:
            self.producer.close()
            
    def stop(self):
        self.running = False

def load_player_data(file_path: str) -> List[Dict]:
    """
    Load player data from JSON file
    
    :param file_path: Path to the JSON file
    :return: List of player dictionaries
    """
    with open(file_path, 'r') as f:
        return json.load(f)

producers = []
threads = []

def start_match(match_type: str):
    bootstrap_servers = ['kafka:9092']
    topic = 'coordinates'
    
    global producers
    producers = []
    global threads
    threads = []

    # Load player data based on match type
    if match_type == '3v3':
        first_team = load_player_data('bin_data.json')
        second_team = load_player_data('kcr_data.json')
    elif match_type == '11v11':
        first_team = load_player_data('blue_lock_data.json')
        second_team = load_player_data('u_20_data.json')
    else:
        print("Invalid match type. Please specify '3v3' or '11v11'.")
        return

    # Create producers for each player and the ball
    # 1st team players
    for player in first_team:
        producer = FootballPlayerProducer(player, bootstrap_servers, topic)
        thread = threading.Thread(target=producer.start_publishing)
        thread.start()
        producers.append(producer)
        threads.append(thread)
    
    # 2nd team players
    for player in second_team:
        producer = FootballPlayerProducer(player, bootstrap_servers, topic)
        thread = threading.Thread(target=producer.start_publishing)
        thread.start()
        producers.append(producer)
        threads.append(thread)
    
    # Ball
    ball_producer = BallProducer(bootstrap_servers, topic)
    ball_thread = threading.Thread(target=ball_producer.start_publishing)
    ball_thread.start()
    producers.append(ball_producer)
    threads.append(ball_thread)

def stop_match():
    global producers
    global threads
    if producers:
        for producer in producers:
            producer.stop()
    if threads:
      for thread in threads:
        if thread != threading.main_thread():
            thread.join()
    producers = []
    threads = []
    print("Match stopped and producers closed")

@app.route('/start_match', methods=['POST'])
def start_match_route():
    data = request.get_json()
    match_type = data.get('match_type')
    
    if not match_type or match_type not in ['3v3', '11v11']:
        return jsonify({'status': 'error', 'message': 'Invalid match type'}), 400
    try:
        start_match(match_type)
        return jsonify({'status': 'success', 'message': f'Match {match_type} started'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error starting match: {str(e)}'}), 500
   
@app.route('/stop_match', methods=['POST'])
def stop_match_route():
    try:
        stop_match()
        return jsonify({'status': 'success', 'message': 'Match stopped'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error stopping match: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)