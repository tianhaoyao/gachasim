<script setup lang="ts">
import { Game } from '@GameModule/models/Game';
import axios from '@/axios-instance';
import { onMounted, reactive, ref } from 'vue';
import keyBy from 'lodash/keyBy';

type Form = {
  gameId: Nullable<number>;
  rarityName: string;
  chance: string;
  pity: string;
  softPity: string;
  softPityChance: string;
  color: string;
};

const initialForm = {
  gameId: null,
  rarityName: '',
  chance: '',
  pity: '',
  softPity: '',
  softPityChance: '',
  color: '#ffffff',
};

defineOptions({
  name: 'CreateNewRate',
});

const form = reactive<Form>(initialForm);

const includePity = ref(false);

const includeSoftPity = ref(false);

const games = ref<Array<Game>>([]);

const gamesHash = ref<Record<number, Game>>({});

const selectedGameName = form.gameId ? gamesHash[form.gameId]?.game_name ?? '' : '';

onMounted(() => {
  fetchGames();
});

const onSubmit = () => {
  // Validate the form fields and construct the request payload
  if (includePity.value && !form.pity) {
    console.error('Please enter a value for Pity');
    return;
  }

  if (
    (includeSoftPity.value && !form.softPityChance) ||
    (includeSoftPity.value && !form.softPity)
  ) {
    console.error('Please enter a value for Soft Pity Chance');
    return;
  }

  const payload = {
    game_id: form.gameId,
    rarity_name: form.rarityName,
    chance: form.chance,
    pity: includePity.value ? form.pity : 0,
    softpity: includeSoftPity.value ? form.softPity : 0,
    softpitychance: includeSoftPity.value ? form.softPityChance : 0,
    color: form.color,
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
};

const fetchGames = () => {
  axios
    .get('/game/games/')
    .then((response) => {
      const fetchedGames = response.data;
      games.value = fetchedGames;
      gamesHash.value = keyBy(fetchedGames, 'id');
    })
    .catch((error) => {
      console.error(error);
    });
};
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
