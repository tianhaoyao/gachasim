<template>
  <nav class="navbar sticky-top navbar-expand-lg navbar-dark bg-dark">
    <ul class="navbar-nav">
      <li class="nav-item" v-for="game in games" :key="game.game_name">
        <a class="nav-link" href="#" @click="setCurrentGame(game.id)">{{ game.game_name }}</a>
      </li>
      <li class="nav-item" key="createNew">
        <router-link to="/create">
          <a class="nav-link"> Create New </a>
        </router-link>
      </li>
    </ul>
  </nav>
  <GameView :gameId="current_game" />
</template>

<script>
import GameView from './GameView.vue';
import axios from 'axios';

export default {
  name: 'GameSelection',
  components: {
    GameView,
  },
  data() {
    return {
      games: {},
      current_game: 1,
    };
  },
  mounted() {
    this.getgames();
  },
  methods: {
    getgames: function () {
      axios
        .get(`/game/games/`)
        .then((response) => {
          this.games = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    setCurrentGame(game) {
      this.current_game = game;
    },
  },
};
</script>

<style></style>
