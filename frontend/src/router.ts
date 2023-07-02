import { createRouter, createWebHistory } from 'vue-router';
import CreateNew from './components/CreateNew.vue';
import CreateNewItem from '@ItemModule/CreateNewItem/components/CreateNewItem.vue';
import CreateNewRarity from '@RarityModule/CreateNewRarity/components/CreateNewRarity.vue';
import CreateNewGame from '@GameModule/CreateNewGame/components/CreateNewGame.vue';
import GameView from '@GameModule/Gacha/components/GameView.vue';

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    // Define your routes here
    { path: '', redirect: '/home' },
    { path: '/home', component: GameView },
    { path: '/create', component: CreateNew },
    { path: '/create/item', component: CreateNewItem },
    { path: '/create/game', component: CreateNewGame },
    { path: '/create/rarity', component: CreateNewRarity },
  ],
});
