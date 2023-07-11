<script setup lang="ts">
import { provide, reactive, ref, watch } from 'vue';
import GachaResult from './GachaResult.vue';
import { callApi } from '@/callApi';
import { RaritiesHashKey } from '../symbols';
import { RaritiesHash, Roll } from '../types';
import { useGameStore } from '@GameModule/stores/GameStore';
import { storeToRefs } from 'pinia';
import keyBy from 'lodash/keyBy';
import { fetchRarities } from '@RarityModule/api/rarity';

defineOptions({
  name: 'GameView',
});

const gameStore = useGameStore();

const { selectedGame } = storeToRefs(gameStore);

const raritiesHash = reactive<RaritiesHash>({});

const setRaritiesHash = (res: RaritiesHash) => {
  Object.assign(raritiesHash, res);
};

provide(RaritiesHashKey, raritiesHash);

const rollResults = ref<Array<Roll>>([]);

const numRolls = ref<number>(10);

watch(selectedGame, async (selectedGame) => {
  if (!selectedGame) {
    return;
  }

  const rarities = await fetchRarities({
    gameId: selectedGame.id,
  });

  const raritiesHash = keyBy(rarities, 'id');

  setRaritiesHash(raritiesHash);
});

const onRoll = () => {
  if (!selectedGame.value) {
    return;
  }

  callApi<Array<Roll>>({
    endpoint: `/game/${selectedGame.value.id}/gacha/`,
    params: {
      format: 'json',
      numrolls: numRolls.value,
    },
  })
    .then((response) => {
      rollResults.value = response;
    })
    .catch((error) => {
      console.log(error);
    });
};
</script>

<template>
  <template v-if="!selectedGame"><div>Select a game first</div></template>
  <template v-else>
    <img :src="selectedGame.image" />
    <div class="game">
      <input v-model="numRolls" number />
      <button @click="onRoll">Reroll</button>
      <GachaResult :roll-results="rollResults" />
    </div>
  </template>
</template>

<style scoped>
h3 {
  margin: 40px 0 0;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
