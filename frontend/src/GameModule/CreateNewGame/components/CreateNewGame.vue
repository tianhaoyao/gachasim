<script lang="ts">
import { defineComponent, inject } from 'vue';
import { LoggedInUserKey } from '@/symbols';
import axios from '@/axios-instance';

type ComponentData = {
  form: {
    gameName: Nullable<string>;
    selectedImage: Nullable<File>;
  };
};

export default defineComponent({
  name: 'CreateNewGame',
  setup() {
    const loggedInUser = inject(LoggedInUserKey);

    return {
      loggedInUser,
    };
  },
  data(): ComponentData {
    return {
      form: {
        gameName: null,
        selectedImage: null,
      },
    };
  },
  methods: {
    onSubmit() {
      if (
        this.form.gameName === null ||
        this.form.selectedImage === null ||
        this.loggedInUser === null
      ) {
        return;
      }

      const formData = new FormData();
      formData.append('game_name', this.form.gameName);
      formData.append('image', this.form.selectedImage);
      formData.append('author_id', String(this.loggedInUser?.id));

      axios
        .post('/game/games/', formData)
        .then((response) => {})
        .catch((error) => {
          console.error(error);
        });
    },
    onChangeImageFile(event: Event) {
      const target = event.target as HTMLInputElement;
      const files = target.files;
      if (files && files[0]) {
        console.log('file', files[0]);
        this.form.selectedImage = files[0];
      }
    },
  },
});
</script>

<template>
  <router-link to="/home" class="button">DONE</router-link>
  <form @submit.prevent="onSubmit">
    <label for="gameName">Game Name:</label>
    <input id="gameName" v-model="form.gameName" type="text" />
    <label for="image">Image:</label>
    <input id="image" type="file" required @change="onChangeImageFile" />
    <button>Submit</button>
  </form>
</template>

<style></style>
