import { createRouter, createWebHistory } from 'vue-router';

// Importez vos composants de page
import HomePage from '../components/HelloWorld.vue'; // Page actuelle pour choisir le match
import Match3v3 from '../components/Match3v3.vue'; // Page 3v3
import Match11v11 from '../components/Match11v11.vue'; // Page 11v11

// Définissez les routes
const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage,
  },
  {
    path: '/3v3',
    name: 'Match3v3',
    component: Match3v3,
  },
  {
    path: '/11v11',
    name: 'Match11v11',
    component: Match11v11,
  },
];

// Créez le routeur
const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
