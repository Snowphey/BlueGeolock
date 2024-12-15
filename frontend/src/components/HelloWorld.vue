<script>
export default {
  name: "HelloWorld",
};
</script>


<template>
  <div class="page-container">
    <!-- Logo -->
    <div class="logo-container">
      <img src="/src/assets/Blue_Geolock_logo_title.png" alt="Blue Lock Logo" class="logo" />
    </div>

    <!-- Title -->
    <h1 class="title">CHOOSE MATCH:</h1>

    <!-- Match Selection -->
    <div class="matches-container">
      <!-- 11V11 Match -->
      <div class="match-option">
        <img src="/src/assets/BL_Icon_Rin_Itoshi.png" alt="Player 1" class="player-img" />
        <div class="match-details">
          <h2>11V11</h2>
          <p>BLUE LOCK <br />VS<br />U-20 JAPAN</p>
        </div>
        <img src="/src/assets/BL_Icon_Sae_Itoshi.png" alt="Player 2" class="player-img" />
      </div>

      <!-- 3V3 Match -->
      <div class="match-option">
        <div class="players-row">
          <img src="/src/assets/BL_Icon_Shoei_Baro.png" alt="Barou" class="player-img" />
          <img src="/src/assets/BL_Icon_Yoichi_Isagi.png" alt="Isagi" class="player-img" />
          <img src="/src/assets/BL_Icon_Seishiro_Nagi.png" alt="Nagi" class="player-img" />
        </div>
        <div class="match-details">
          <h2>3V3</h2>
          <p>BAROU, ISAGI & NAGI<br /> VS<br />KUNIGAMI, CHIGIRI & REO</p>
        </div>
        <div class="players-row">
          <img src="/src/assets/BL_Icon_Rensuke_Kunigami.png" alt="Kunigami" class="player-img" />
          <img src="/src/assets/BL_Icon_Hyoma_Chigiri.png" alt="Chigiri" class="player-img" />
          <img src="/src/assets/BL_Icon_Reo_Mikage.png" alt="Reo" class="player-img" />
        </div>
      </div>
    </div>
  </div>
</template>


<style scoped>
.page-container {
  text-align: center;
  font-family: Arial, sans-serif;
  background-color: #ffffff;
  color: #000;
  padding: 20px;
}

.logo-container {
  margin-bottom: 20px;  
}

.logo {
  width: 700px;
}

.title {
  font-size: 24px;
  margin-bottom: 20px 0;
  font-weight: bold;
}

.matches-container {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
  gap: 20px;
}

.match-option {
  border: 2px solid #000;
  border-radius: 10px;
  padding: 20px;
  width: 300px;
  background-color: #f9f9f9;
}

.players-row {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 10px;
}

.player-img {
  width: 60px;
  height: auto;
}

.match-details h2 {
  margin: 10px 0;
  font-size: 20px;
  font-weight: bold;
}

.match-details p {
  margin: 0;
  line-height: 1.5;
  font-size: 16px;
}
</style>
