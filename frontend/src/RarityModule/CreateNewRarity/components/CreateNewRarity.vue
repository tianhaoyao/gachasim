<script lang="ts">
import { Game } from '@GameModule/models/Game';
import axios from 'axios';
import { defineComponent } from 'vue';
import keyBy from 'lodash/keyBy';

type ComponentData = {
  form: {
    gameId: Nullable<number>;
    rarityName: string;
    chance: string;
    pity: string;
    softPity: string;
    softPityChance: string;
    color: string;
  };
  includePity: boolean;
  includeSoftPity: boolean;
  games: Array<Game>;
  gamesHash: Record<number, Game>;
};

export default defineComponent({
  name: 'CreateNewRate',
  data(): ComponentData {
    return {
      form: {
        gameId: null,
        rarityName: '',
        chance: '',
        pity: '',
        softPity: '',
        softPityChance: '',
        color: '#ffffff',
      },
      includePity: false,
      includeSoftPity: false,
      games: [],
      gamesHash: {},
    };
  },
  computed: {
    selectedGameName(): string {
      return this.gamesHash[this.form.gameId ?? -1]?.game_name ?? '';
    },
  },
  mounted() {
    this.fetchGames();
  },
  methods: {
    onSubmit() {
      // Validate the form fields and construct the request payload
      if (this.includePity && !this.form.pity) {
        console.error('Please enter a value for Pity');
        return;
      }

      if (
        (this.includeSoftPity && !this.form.softPityChance) ||
        (this.includeSoftPity && !this.form.softPity)
      ) {
        console.error('Please enter a value for Soft Pity Chance');
        return;
      }

      const payload = {
        game_id: this.form.gameId,
        rarity_name: this.form.rarityName,
        chance: this.form.chance,
        pity: this.includePity ? this.form.pity : 0,
        softpity: this.includeSoftPity ? this.form.softPity : 0,
        softpitychance: this.includeSoftPity ? this.form.softPityChance : 0,
        color: this.form.color,
      };

      axios
        .post('/game/rarities/', payload)
        .then((response) => {
          console.log(response.data);
          // Handle success response
          console.log(payload);
        })
        .catch((error) => {
          console.error(error);
          console.log(payload);
          console.log(error.response);
        });
    },
    fetchGames() {
      axios
        .get('/game/games/')
        .then((response) => {
          this.games = response.data;
          this.gamesHash = keyBy(this.games, 'id');
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
});
</script>

<template>
  <router-link to="/home" class="button">DONE</router-link>
  <form @submit.prevent="onSubmit">
    <label for="game">Game:</label>
    <select v-model="form.gameId">
      <option v-for="game in games" :key="game.id" :value="game.id">{{ game.game_name }}</option>
    </select>

    <label for="rarity">Rarity:</label>
    <input id="rarity" v-model="form.rarityName" type="text" />

    <label for="chance">Chance:</label>
    <input id="chance" v-model="form.chance" type="number" />

    <label for="pity">Include Pity:</label>
    <input id="pity" v-model="includePity" type="checkbox" />

    <div v-if="includePity">
      <label for="pityValue">Pity:</label>
      <input id="pityValue" v-model="form.pity" type="text" />

      <label for="includeSoftPity">Include Soft Pity:</label>
      <input id="includeSoftPity" v-model="includeSoftPity" type="checkbox" />
    </div>

    <div v-if="includeSoftPity">
      <label for="softPity">Soft Pity:</label>
      <input id="softPityChance" v-model="form.softPity" type="text" />

      <label for="softPityChance">Soft Pity Chance:</label>
      <input id="softPityChance" v-model="form.softPityChance" type="text" />
    </div>

    <label for="color">Color:</label>
    <color-input id="color" v-model="form.color" />

    rate:{{ form.rarityName }} chance{{ form.chance }} game: {{ selectedGameName }} softPity:
    {{ form.softPity }} softPityChance: {{ form.softPityChance }} color: {{ form.color }}
    <button type="submit">Submit</button>
  </form>
</template>

<style></style>
