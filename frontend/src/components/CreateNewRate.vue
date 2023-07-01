<script>
import axios from 'axios';

export default {
  name: 'CreateNewRate',
  data() {
    return {
      form: {
        game: null,
        rarity: null,
        chance: null,
        pity: null,
        softpity: null,
        softpitychance: null,
        color: '#ffffff',
      },
      includePity: false,
      includeSoftPity: false,
      games: {},
    };
  },
  mounted() {
    this.fetchGames();
  },
  methods: {
    submitForm(event) {
      event.preventDefault();
      // Validate the form fields and construct the request payload
      if (this.includePity && !this.form.pity) {
        console.error('Please enter a value for Pity');
        return;
      }

      if (
        (this.includeSoftPity && !this.form.softpitychance) ||
        (this.includeSoftPity && !this.form.softpity)
      ) {
        console.error('Please enter a value for Soft Pity Chance');
        return;
      }

      const payload = {
        game: this.form.game,
        rarity: this.form.rarity,
        chance: this.form.chance,
        pity: this.includePity ? this.form.pity : 0,
        softpity: this.includeSoftPity ? this.form.softpity : 0,
        softpitychance: this.includeSoftPity ? this.form.softpitychance : 0,
        color: this.form.color,
      };

      axios
        .post('/game/rates/', payload)
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
          console.log(this.games);
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>

<template>
  <router-link to="/home" class="button">DONE</router-link>
  <form @submit="submitForm">
    <label for="game">Game:</label>
    <select v-model="form.game">
      <option v-for="game in games" :key="game.id" :value="game.id">{{ game.game_name }}</option>
    </select>

    <label for="rarity">Rarity:</label>
    <input type="text" id="rarity" v-model="form.rarity" />

    <label for="chance">Chance:</label>
    <input type="text" id="chance" v-model="form.chance" />

    <label for="pity">Include Pity:</label>
    <input type="checkbox" id="pity" v-model="includePity" />

    <div v-if="includePity">
      <label for="pityValue">Pity:</label>
      <input type="text" id="pityValue" v-model="form.pity" />

      <label for="includeSoftPity">Include Soft Pity:</label>
      <input type="checkbox" id="includeSoftPity" v-model="includeSoftPity" />
    </div>

    <div v-if="includeSoftPity">
      <label for="softPity">Soft Pity:</label>
      <input type="text" id="softPityChance" v-model="form.softpity" />

      <label for="softPityChance">Soft Pity Chance:</label>
      <input type="text" id="softPityChance" v-model="form.softpitychance" />
    </div>

    <label for="color">Color:</label>
    <color-input id="color" v-model="form.color" />

    rate:{{ form.rarity }} chance{{ form.chance }} game: {{ form.game }} softpity:
    {{ form.softpity }} softpitychance: {{ form.softpitychance }} color: {{ form.color }}
    <button type="submit">Submit</button>
  </form>
</template>

<style></style>
