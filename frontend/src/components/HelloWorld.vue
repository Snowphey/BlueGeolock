<script>
export default {
  name: "HelloWorld",
  methods: {
    navigateTo(route) {
      this.$router.push({path: route});
    },
  },
};
</script>
<template>
  <div class="page-container">
    <!-- Logo -->
    <div class="logo-container">
      <img src="/assets/Blue_Geolock_logo_title.png" alt="Blue Lock Logo" class="logo" />
    </div>

    <!-- Match Selection -->
    <div class="matches-wrapper">
      <!-- 11V11 Match -->
      <div class="match-option" @click="navigateTo('/11v11')">
        <img src="/assets/icons/11v11/BlueLock/png/BL_Icon_Rin_Itoshi.png" alt="Player 1" class="player-img" />
        <div class="match-details">
          <h2>11V11</h2>
          <p>BLUE LOCK <br />VS<br />U-20 JAPAN</p>
        </div>
        <img src="/assets/icons/11v11/U20/png/BL_Icon_Sae_Itoshi.png" alt="Player 2" class="player-img" />
      </div>

      <!-- Title centered -->
      <div class="title-container">
        <h1 class="title">CHOOSE MATCH:</h1>
      </div>

      <!-- 3V3 Match -->
      <div class="match-option" @click="navigateTo('/3v3')">
        <div class="players-row">
          <img src="/assets/icons/3v3/BIN/png/BL_Icon_Shoei_Baro.png" alt="Barou" class="player-img" />
          <img src="/assets/icons/3v3/BIN/png/BL_Icon_Yoichi_Isagi.png" alt="Isagi" class="player-img" />
          <img src="/assets/icons/3v3/BIN/png/BL_Icon_Seishiro_Nagi.png" alt="Nagi" class="player-img" />
        </div>
        <div class="match-details">
          <h2>3V3</h2>
          <p>BAROU, ISAGI & NAGI<br /> VS<br />KUNIGAMI, CHIGIRI & REO</p>
        </div>
        <div class="players-row">
          <img src="/assets/icons/3v3/KCR/png/BL_Icon_Rensuke_Kunigami.png" alt="Kunigami" class="player-img" />
          <img src="/assets/icons/3v3/KCR/png/BL_Icon_Hyoma_Chigiri.png" alt="Chigiri" class="player-img" />
          <img src="/assets/icons/3v3/KCR/png/BL_Icon_Reo_Mikage.png" alt="Reo" class="player-img" />
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
  padding: 10px;
}

.logo-container {
  margin-bottom: 10px;
}

.logo {
  width: 750px; /* Taille réduite du logo */
}

.matches-wrapper {
  display: flex;
  justify-content: center; /* Alignement horizontal */
  align-items: center;
  gap: 20px; /* Espacement horizontal entre les éléments */
  position: relative;
}

.match-option {
  cursor: pointer;
  border: 2px solid #000;
  border-radius: 10px;
  padding: 15px;
  width: 450px;
  background-color: #f9f9f9;
  transition: background-color 0.3s, transform 0.3s;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.match-option:hover {
  background-color: #2831d2;
  transform: translateY(-5px);
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.2);
}

.title-container {
 margin: 50px;
}

.title {
  font-size: 22px;
  font-weight: bold;
  margin: 0;
}

.players-row {
  display: flex;
  justify-content: center;
  gap: 5px;
  margin-bottom: 5px;
}

.player-img {
  width: 100px;
  height: auto;
}

.match-details h2 {
  font-size: 18px;
  font-weight: bold;
}

.match-details p {
  margin: 0;
  line-height: 1.3;
  font-size: 14px;
}
</style>
