<script lang="ts">
import { SetSelectedGameKey, LoggedInUserKey } from '@/symbols';
import { Game } from '@GameModule/models/Game';
import axios from 'axios';
import { defineComponent, inject } from 'vue';

type NavBarData = {
  games: Array<Game>;
};

export default defineComponent({
  name: 'NavBar',
  setup() {
    const setSelectedGame = inject(SetSelectedGameKey);
    const loggedInUser = inject(LoggedInUserKey);

    return {
      setSelectedGame,
      loggedInUser,
    };
  },
  data(): NavBarData {
    return {
      games: [],
    };
  },
  mounted() {
    this.fetchGames();
  },
  methods: {
    fetchGames: function () {
      axios
        .get(`/game/games/`)
        .then((response) => {
          this.games = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
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
        <a class="nav-link" href="#" @click="setSelectedGame?.(game)">{{ game.game_name }}</a>
      </li>
      <li class="nav-item">
        <router-link to="/create">
          <a class="nav-link"> Create New </a>
        </router-link>
      </li>
    </ul>
    <ul class="navbar-nav ml-auto">
      <li v-if="loggedInUser" class="nav-item">
        <span class="navbar-text"> Logged in as {{ loggedInUser.username }} </span>
      </li>
      <li v-if="!loggedInUser" class="nav-item">
        <router-link to="/login">
          <a class="nav-link"> Login </a>
        </router-link>
      </li>
      <li v-if="!loggedInUser" class="nav-item">
        <router-link to="/register">
          <a class="nav-link"> Register </a>
        </router-link>
      </li>
    </ul>
  </nav>
</template>
