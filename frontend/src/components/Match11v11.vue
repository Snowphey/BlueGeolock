
<script>
import blue_lock_team from '/blue_lock_data.json';
import u20_team from '/u_20_data.json';

export default {
  name: 'Match11v11',
  data: function() {
    return {
      socket: null,
    }
  },
  methods: {
    navigateTo(route) {
      this.$router.push({path: route});
    },
  },
  beforeRouteEnter(to, from, next) {
    fetch('http://localhost:5000/start_match', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ match_type: '11v11' })
    })
    .then(response => response.json())
    .then(data => {
      console.log('Match started:', data);
      next();
    })
    .catch(error => {
      console.error('There was an error starting the match:', error);
    });
  },
  beforeRouteLeave(to, from, next) {
    if(this.socket) {
      this.socket.onclose = function(event) {
            if (event.wasClean) {
                console.log(`Connection closed cleanly, code=${event.code} reason=${event.reason}`);
            } else {
                console.error('Connection died');
            }

            fetch('http://localhost:5000/stop_match', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
            })
            .then(response => response.json())
            .then(data => {
              console.log('Match stopped:', data);
              next();
            })
            .catch(error => {
              console.error('There was an error stopping the match:', error);
            });
        };

      console.log('Closing socket...');
      this.socket.close();
    } else {
      next();
    }
  },
  mounted() {
      var map = L.map('map', {
        crs: L.CRS.Simple
      });

      let height = 700;
      let width = 1500;

      var bounds = [[0,0], [height,width]];
      L.imageOverlay('/assets/terrain.png', bounds).addTo(map);

      map.fitBounds(bounds);

      let ballIcon = L.icon({
                  iconUrl: '/assets/icons/11v11/ball.png',
                  iconSize: [40, 40],
                  popupAnchor: [0, -20]
              });

      let ballMarker = L.Marker.movingMarker([[0.5 * height, 0.5 * width]], [2000], { icon: ballIcon })
                  .addTo(map)
                  .bindPopup('Ball');

      let iconSize = [100, 100];
      let popupAnchor = [0, -30];

      let playerMarkers = {};

      function addPlayerMarkers(team, teamName) {
          team.forEach(player => {
              let playerIcon = L.icon({
                  iconUrl: `/assets/icons/11v11/${teamName}/png/BL_Icon_${player.first_name}_${player.last_name}.png`,
                  iconSize: iconSize,
                  popupAnchor: popupAnchor
              });

              let playerMarker = L.Marker.movingMarker([[player.latitude * height, player.longitude * width]], [2000], { icon: playerIcon })
                  .addTo(map)
                  .bindPopup(`Player: ${player.first_name} ${player.last_name}<br>Number: ${player.number}<br>Team: ${teamName}<br>Position: ${player.role}`);

              playerMarkers[`${player.first_name}_${player.last_name}`] = playerMarker;
          });
      }

      function movePlayerMarker(firstName, lastName, newLatitude, newLongitude) {
          let key = `${firstName}_${lastName}`;
          let playerMarker = playerMarkers[key];
          if (playerMarker) {
              if (!playerMarker.isStarted()) {
                        playerMarker.start();
              }
              playerMarker.moveTo([newLatitude * height, newLongitude * width], 2000);
          } else {
              console.error(`Player marker for ${firstName} ${lastName} not found.`);
          }
      }

      addPlayerMarkers(blue_lock_team, 'BlueLock');
      addPlayerMarkers(u20_team, 'U20');

      this.socket = new WebSocket(`ws://localhost:8000/ws/coordinates`);

      this.socket.onopen = function(e) {
          console.log('WebSocket connection established');
      };

      this.socket.onmessage = function(event) {
          let coordinates = JSON.parse(event.data);
          
          coordinates.forEach(coord => {
              if (coord.first_name === 'Football' && coord.last_name === 'Ball') {
                  if (!ballMarker.isStarted()) {
                    ballMarker.start();
                  }
                  ballMarker.moveTo([coord.latitude * height, coord.longitude * width], 2000);
              } else {
                  if(blue_lock_team.some(player => player.first_name === coord.first_name && player.last_name === coord.last_name) ||
                     u20_team.some(player => player.first_name === coord.first_name && player.last_name === coord.last_name)) {
                    movePlayerMarker(coord.first_name, coord.last_name, coord.latitude, coord.longitude);
                  }
              }
          });
      };

      this.socket.onerror = function(error) {
          console.error(`[error] ${error.message}`);
      };
  },
};
</script>

<template>
  <div class="page-container">
    <div class="logo-container" @click="navigateTo('/')">
      <img src="/assets/Blue_Geolock_logo_title.png" alt="Blue Lock Logo" class="logo" />
    </div>

    <div>
      <h1>Page 11v11</h1>
    </div>
    
    <div id="map" ref="mapElement"></div>
  </div>
</template>

<style scoped>
/* Ajoutez vos styles ici */
#map { 
  height: 700px; 
}

.page-container {
  text-align: center;
  font-family: Arial, sans-serif;
  background-color: #ffffff;
  color: #000;
  padding: 10px;
}

.logo {
  width: 120px; /* Taille réduite du logo */
  cursor: pointer;
  border: 2px solid #000;
  border-radius: 10px;
  padding: 15px;
  background-color: #f9f9f9;
  transition: background-color 0.3s, transform 0.3s;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.logo:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.2);
}
</style>
