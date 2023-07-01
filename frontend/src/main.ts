import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import App from './App.vue';
import CreateNew from './components/CreateNew.vue';
import CreateNewItem from './components/CreateNewItem.vue';
import CreateNewRate from './components/CreateNewRate.vue';
import CreateNewGame from './components/CreateNewGame.vue';
import GameView from '@GameModule/Gacha/components/GameView.vue';
import axios from 'axios';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.js';
import ColorInput from 'vue-color-input';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    // Define your routes here
    { path: '', redirect: '/home' },
    { path: '/home', component: GameView },
    { path: '/create', component: CreateNew },
    { path: '/create/item', component: CreateNewItem },
    { path: '/create/game', component: CreateNewGame },
    { path: '/create/rate', component: CreateNewRate },
  ],
});

axios.defaults.baseURL = 'http://127.0.0.1:8000/';

const app = createApp(App);
app.use(router);
app.mount('#app');
app.component('ColorInput', ColorInput);
