<script lang="ts">
import { Game } from '@GameModule/models/Game';
import { Rarity, RarityId } from '@RarityModule/models/Rarity';
import axios from '@/axios-instance';
import { defineComponent } from 'vue';
import keyBy from 'lodash/keyBy';

type ComponentData = {
  form: {
    gameId: Nullable<number>;
    rarityId: Nullable<RarityId>;
    itemName: Nullable<string>;
    selectedImage: Nullable<File>;
    chance: number;
  };
  games: Array<Game>;
  rarities: Array<Rarity>;
  raritiesHash: Record<RarityId, Rarity>;
};

export default defineComponent({
  name: 'CreateNewItem',
  data(): ComponentData {
    return {
      form: {
        gameId: null,
        rarityId: null,
        itemName: '',
        selectedImage: null,
        chance: 0.0,
      },
      games: [],
      rarities: [],
      raritiesHash: {},
    };
  },
  computed: {
    selectedRarityName(): string {
      return this.raritiesHash?.[this.form.rarityId ?? -1]?.rarity_name ?? '';
    },
    isInvalidForm(): boolean {
      return (
        !this.form.chance || !this.form.itemName || !this.form.rarityId || !this.form.selectedImage
      );
    },
  },
  mounted() {
    this.fetchGames();
  },
  methods: {
    onSubmit() {
      if (
        !this.form.chance ||
        !this.form.itemName ||
        !this.form.rarityId ||
        !this.form.selectedImage
      )
        return;

      const formData = new FormData();
      formData.append('rate', this.form.rarityId.toString());
      formData.append('item_name', this.form.itemName);
      formData.append('image', this.form.selectedImage);
      formData.append('chance', Number(this.form.chance).toString());

      axios
        .post('/game/items/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        .then((response) => {})
        .catch((error) => {});
    },
    handleImageChange(event: Event) {
      const target = event.target as HTMLInputElement;
      const files = target.files;
      if (files !== null && files.length > 0) {
        this.form.selectedImage = files[0];
      }
    },
    fetchGames() {
      axios
        .get('/game/games/')
        .then((response) => {
          this.games = response.data;
        })
        .catch((error) => {});
    },
    fetchRarities() {
      if (this.form.gameId === null) return;

      axios
        .get(`/game/rarities/`, { params: { game_id: this.form.gameId } })
        .then((response) => {
          const rarities = response.data;
          this.rarities = rarities;
          console.log(this.form.gameId);
          this.raritiesHash = keyBy(rarities, 'id');
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
    <select v-model="form.gameId" @change="fetchRarities">
      {{
        rarities
      }}
      <option v-for="game in games" :key="game.id" :value="game.id">{{ game.game_name }}</option>
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
    {{ form.selectedImage }} chance{{ form.chance }}
    <button type="submit">Submit</button>
  </form>
</template>

<style></style>
