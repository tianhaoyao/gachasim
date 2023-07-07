<script lang="ts">
import { Game } from '@GameModule/models/Game';
import axios from 'axios';
import { mapState, mapActions } from 'pinia';
import { defineComponent } from 'vue';
import { useUserStore } from '@UserModule/stores/UserStore';
import { useGameStore } from '@GameModule/stores/GameStore';

type NavBarData = {
  games: Array<Game>;
};

export default defineComponent({
  name: 'NavBar',
  data(): NavBarData {
    return {
      games: [],
    };
  },
  computed: {
    ...mapState(useUserStore, ['user']),
  },
  mounted() {
    this.fetchGames();
  },
  methods: {
    ...mapActions(useGameStore, ['setSelectedGame']),
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
