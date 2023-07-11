<script setup lang="ts">
import { reactive } from 'vue';
import { useUserStore } from '@UserModule/stores/UserStore';
import { storeToRefs } from 'pinia';
import { createNewGame } from '@GameModule/api/game';

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

  createNewGame({
    gameName: form.gameName,
    selectedImage: form.selectedImage,
    authorId: user.value.id,
  });

  Object.assign(form, initialForm);
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
