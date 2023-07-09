<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useUserStore } from '@UserModule/stores/UserStore';
import { useGameStore } from '@GameModule/stores/GameStore';
import { Game } from '@GameModule/models/Game';
import { callApi } from '@/callApi';
import { storeToRefs } from 'pinia';

defineOptions({
  name: 'NavBar',
});

const games = ref<Array<Game>>([]);

const userStore = useUserStore();

const { user } = storeToRefs(userStore);

const { setSelectedGame } = useGameStore();

const fetchGames = () => {
  callApi<Array<Game>>({ endpoint: '/game/games/' })
    .then((response) => {
      games.value = response;
    })
    .catch((error) => {
      console.log(error);
    });
};

onMounted(() => {
  fetchGames();
});
</script>

<template>
  <nav class="navbar sticky-top navbar-expand-lg navbar-dark bg-dark">
    <ul class="navbar-nav">
      <li class="nav-item">
        <router-link to="/home">
          <a class="nav-link"> Home </a>
        </router-link>
      </li>
      <li v-for="game in games" :key="game.id" class="nav-item">
        <a class="nav-link" href="#" @click="setSelectedGame(game)">{{ game.game_name }}</a>
      </li>
      <li class="nav-item">
        <router-link to="/create">
          <a class="nav-link"> Create New </a>
        </router-link>
      </li>
    </ul>
    <ul class="navbar-nav ml-auto">
      <li v-if="user" class="nav-item">
        <span class="navbar-text"> Logged in as {{ user.username }} </span>
      </li>
      <li v-if="!user" class="nav-item">
        <router-link to="/login">
          <a class="nav-link"> Login </a>
        </router-link>
      </li>
      <li v-if="!user" class="nav-item">
        <router-link to="/register">
          <a class="nav-link"> Register </a>
        </router-link>
      </li>
    </ul>
  </nav>
</template>
