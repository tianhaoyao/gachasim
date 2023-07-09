<script setup lang="ts">
import { Game, GameId } from '@GameModule/models/Game';
import { Rarity, RarityId } from '@RarityModule/models/Rarity';
import axios from '@/axios-instance';
import { onMounted, reactive, ref } from 'vue';
import keyBy from 'lodash/keyBy';

type Form = {
  gameId: Nullable<GameId>;
  rarityId: Nullable<RarityId>;
  itemName: string;
  selectedImage: Nullable<File>;
  chance: number;
};

const initialForm = {
  gameId: null,
  rarityId: null,
  itemName: '',
  selectedImage: null,
  chance: 0,
};

defineOptions({
  name: 'CreateNewItem',
});

const form = reactive<Form>(initialForm);

const games = ref<Array<Game>>([]);

const rarities = ref<Array<Rarity>>([]);

const raritiesHash = ref<Record<RarityId, Rarity>>({});

const selectedRarityName = form.rarityId
  ? raritiesHash.value?.[form.rarityId]?.rarity_name ?? ''
  : '';

onMounted(() => {
  fetchGames();
});

const fetchGames = () => {
  axios
    .get('/game/games/')
    .then((response) => {
      games.value = response.data;
    })
    .catch((error) => {});
};

const fetchRarities = () => {
  if (form.gameId === null) return;

  axios
    .get(`/game/rarities/`, { params: { game_id: form.gameId } })
    .then((response) => {
      const fetchedRarities = response.data;
      rarities.value = fetchedRarities;
      raritiesHash.value = keyBy(fetchedRarities, 'id');
    })
    .catch((error) => {
      console.error(error);
    });
};

const onSubmit = () => {
  if (!form.chance || !form.itemName || !form.rarityId || !form.selectedImage) return;

  const formData = new FormData();

  formData.append('rarity_id', form.rarityId.toString());
  formData.append('item_name', form.itemName);
  formData.append('image', form.selectedImage);
  formData.append('chance', Number(form.chance).toString());

  Object.assign(form, initialForm);

  axios
    .post('/game/items/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    .then((response) => {})
    .catch((error) => {});
};

const handleImageChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const files = target.files;
  if (files !== null && files.length > 0) {
    form.selectedImage = files[0];
  }
};
</script>

<template>
  <router-link to="/home" class="button">DONE</router-link>
  <form @submit.prevent="onSubmit">
    <label for="game">Game:</label>
    <select v-model="form.gameId" @change="fetchRarities">
      {{
        rarities
      }}
      <option v-for="game in games" :key="game.id" :value="game.id">
        {{ game.game_name }}
      </option>
    </select>

    <label for="rate">Rarities:</label>
    <select v-model="form.rarityId">
      <option v-for="rarity in rarities" :key="rarity.id" :value="rarity.id">
        {{ rarity.rarity_name }}
      </option>
    </select>

    <label for="item_name">Item Name:</label>
    <input id="item_name" v-model="form.itemName" type="text" required />

    <label for="image">Image:</label>
    <input id="image" type="file" required @change="handleImageChange" />

    <label for="chance">Chance:</label>
    <input id="chance" v-model="form.chance" type="float" required />
    rate:{{ selectedRarityName }} itename:{{ form.itemName }} image:
    {{ form.selectedImage?.name ?? '' }} chance{{ form.chance }}
    <button type="submit">Submit</button>
  </form>
</template>

<style></style>
