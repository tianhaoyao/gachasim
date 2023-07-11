<script setup lang="ts">
import { Game, GameId } from '@GameModule/models/Game';
import { Rarity, RarityId } from '@RarityModule/models/Rarity';
import { computed, onMounted, reactive, ref, watch } from 'vue';
import keyBy from 'lodash/keyBy';
import { fetchGames } from '@GameModule/api/game';
import { fetchRarities } from '@RarityModule/api/rarity';
import { createNewItem } from '@ItemModule/api/item';

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

const gameId = computed(() => {
  return form.gameId;
});

const games = ref<Array<Game>>([]);

const rarities = ref<Array<Rarity>>([]);

const raritiesHash = ref<Record<RarityId, Rarity>>({});

const selectedRarityName = form.rarityId
  ? raritiesHash.value?.[form.rarityId]?.rarity_name ?? ''
  : '';

onMounted(async () => {
  const fetchedGames = await fetchGames();

  games.value = fetchedGames;
});

watch(gameId, async (gameId) => {
  if (!gameId) return;

  const fetchedRarities = await fetchRarities({ gameId });

  rarities.value = fetchedRarities;

  raritiesHash.value = keyBy(fetchedRarities, 'id');
});

const onCreateNewItem = () => {
  if (!form.chance || !form.itemName || !form.rarityId || !form.selectedImage) return;

  Object.assign(form, initialForm);

  // TODO: Figure out why it still needs type assertion after the condition above
  createNewItem(form as Parameters<typeof createNewItem>[0]);
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
  <form @submit.prevent="onCreateNewItem">
    <label for="game">Game:</label>
    <select v-model="form.gameId">
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
