<script setup lang="ts">
import { reactive } from 'vue';
import axios from '@/axios-instance';
import { useUserStore } from '@UserModule/stores/UserStore';
import { storeToRefs } from 'pinia';

type Form = {
  gameName: string;
  selectedImage: Nullable<File>;
};

const initialForm = {
  gameName: '',
  selectedImage: null,
};

defineOptions({
  name: 'CreateNewGame',
});

const form = reactive<Form>(initialForm);

const userStore = useUserStore();

const { user } = storeToRefs(userStore);

const onCreateNewGame = () => {
  if (!form.gameName || !form.selectedImage || !user.value) {
    return;
  }

  const formData = new FormData();

  formData.append('game_name', form.gameName);
  formData.append('image', form.selectedImage);
  formData.append('author_id', String(user.value.id));

  Object.assign(form, initialForm);

  axios
    .post('/game/games/', formData)
    .then((response) => {})
    .catch((error) => {
      console.error(error);
    });
};

const onChangeImageFile = (event: Event) => {
  const target = event.target as HTMLInputElement;

  const files = target.files;

  if (files && files[0]) {
    form.selectedImage = files[0];
  }
};
</script>

<template>
  <router-link to="/home" class="button">DONE</router-link>
  <form @submit.prevent="onCreateNewGame">
    <label for="gameName">Game Name:</label>
    <input id="gameName" v-model="form.gameName" type="text" />
    <label for="image">Image:</label>
    <input id="image" type="file" required @change="onChangeImageFile" />
    <button>Submit</button>
  </form>
</template>

<style></style>
