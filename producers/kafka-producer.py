import json
import random
import time
from kafka import KafkaProducer
from typing import Dict, List, Tuple

class FootballPlayerProducer:
    def __init__(self, player_data: Dict, bootstrap_servers: List[str], topic: str, team_name: str):
        """
        Initialize a Kafka producer for a football player
        
        :param player_data: Dictionary containing player details
        :param bootstrap_servers: List of Kafka bootstrap servers
        :param topic: Kafka topic to publish coordinates
        :param team_name: Name of the team
        """
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
        self.player_data = player_data
        self.topic = topic
        self.team_name = team_name
        
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
        
    def generate_new_position(self) -> Tuple[float, float]:
        """
        Generate a new position based on player's role and initial position
        
        :return: Tuple of (latitude, longitude)
        """
        role = self.player_data['role']
        min_distance, max_distance = self.movement_constraints[role]
        
        # Add team-specific movement bias
        team_bias_lat = 0.001 if self.team_name == 'blue_lock' else -0.001
        team_bias_lon = 0.001 if self.team_name == 'blue_lock' else -0.001
        
        # Random walk with role-based constraints and team bias
        lat_change = random.uniform(-max_distance, max_distance) + team_bias_lat
        lon_change = random.uniform(-max_distance, max_distance) + team_bias_lon
        
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
            while True:
                self.publish_position()
                time.sleep(interval)
        except KeyboardInterrupt:
            print(f"Stopping producer for {self.player_data['first_name']} {self.player_data['last_name']}")
        finally:
            self.producer.close()

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
    
    def generate_new_position(self) -> Tuple[float, float]:
        """
        Generate more random ball movement
        """
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
            while True:
                self.publish_position()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("Stopping ball producer")
        finally:
            self.producer.close()

def load_player_data(file_path: str) -> List[Dict]:
    """
    Load player data from JSON file
    
    :param file_path: Path to the JSON file
    :return: List of player dictionaries
    """
    with open(file_path, 'r') as f:
        return json.load(f)

def main():
    import threading
    
    bootstrap_servers = ['kafka:9092']
    topic = 'coordinates'
    
    # Load player data for both teams
    blue_lock_team = load_player_data('blue_lock_data.json')
    u20_team = load_player_data('u_20_data.json')
    
    # Create producers for each player and the ball
    producers = []
    
    # Blue Lock Team Players
    for player in blue_lock_team:
        producer = FootballPlayerProducer(player, bootstrap_servers, topic, 'blue_lock')
        thread = threading.Thread(target=producer.start_publishing)
        thread.start()
        producers.append(producer)
    
    # U20 Team Players
    for player in u20_team:
        producer = FootballPlayerProducer(player, bootstrap_servers, topic, 'u20')
        thread = threading.Thread(target=producer.start_publishing)
        thread.start()
        producers.append(producer)
    
    # Ball
    ball_producer = BallProducer(bootstrap_servers, topic)
    ball_thread = threading.Thread(target=ball_producer.start_publishing)
    ball_thread.start()
    producers.append(ball_producer)

    # Wait for all threads
    for thread in threading.enumerate():
        if thread != threading.main_thread():
            thread.join()

if __name__ == '__main__':
    main()