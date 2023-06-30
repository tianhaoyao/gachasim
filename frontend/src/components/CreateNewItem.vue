<template>
  <router-link to="/home" class="button">DONE</router-link>
  <form @submit="submitForm">
    <label for="game">Game:</label>
    <select v-model="gameid" @change="loadRates">
      {{
        rates
      }}
      <option v-for="game in games" :key="game.id" :value="game.id">{{ game.game_name }}</option>
    </select>

    <label for="rate">Rate:</label>
    <select v-model="rate">
      <option v-for="rate in rates" :key="rate.id" :value="rate.id">{{ rate.rarity }}</option>
    </select>

    <label for="item_name">Item Name:</label>
    <input type="text" id="item_name" v-model="itemName" required />

    <label for="image">Image:</label>
    <input type="file" id="image" @change="handleImageChange" required />

    <label for="chance">Chance:</label>
    <input type="float" id="chance" v-model="chance" required />
    rate:{{ rate }} itename:{{ itemName }} image: {{ image }} chance{{ chance }}
    <button type="submit">Submit</button>
  </form>
</template>

<script>
import axios from 'axios';

export default {
  name: 'CreateNewItem',
  data() {
    return {
      gameid: null,
      rate: null,
      itemName: '',
      image: null,
      chance: 0.0,
      games: {},
      rates: {},
    };
  },
  mounted() {
    this.fetchGames();
  },
  methods: {
    submitForm(event) {
      event.preventDefault();
      const formData = new FormData();
      formData.append('rate', this.rate);
      formData.append('item_name', this.itemName);
      formData.append('image', this.image);
      formData.append('chance', parseFloat(this.chance));
      console.log('data', { rate: this.rate, itemName: this.itemName });
      console.log(this.itemName);
      console.log(this.chance);
      console.log(this.image);

      axios
        .post('/game/items/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        .then((response) => {
          console.log(response.data);
          // Handle success response
          console.log(formData);
        })
        .catch((error) => {
          console.error(error);
          console.log(formData);
          console.log(error.response);
        });
    },
    handleImageChange(event) {
      this.image = event.target.files[0];
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
    loadRates() {
      axios
        .get(`/game/rates/`, { params: { game: this.gameid } })
        .then((response) => {
          this.rates = response.data;
          console.log(this.gameid);
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>

<style></style>
