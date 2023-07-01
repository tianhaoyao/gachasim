<script>
import axios from 'axios';

export default {
  name: 'CreateNewGame',
  data() {
    return {
      gameName: null,
      image: null,
    };
  },
  methods: {
    submitForm(event) {
      event.preventDefault();

      const payload = {
        game: this.gameName,
        image: this.image,
      };

      axios
        .post('/game/games/', payload)
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
    handleImageChange(event) {
      this.image = event.target.files[0];
    },
  },
};
</script>

<template>
  <router-link to="/home" class="button">DONE</router-link>
  <form @submit="submitForm">
    <label for="gameName">Game Name:</label>
    <input type="text" id="gameName" v-model="gameName" />

    <label for="image">Image:</label>
    <input type="file" id="image" @change="handleImageChange" required />

    <button type="submit">Submit</button>
  </form>
</template>

<style></style>
