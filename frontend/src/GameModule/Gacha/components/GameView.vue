<script setup lang="ts">
import { provide, reactive, ref, watch } from 'vue';
import GachaResult from './GachaResult.vue';
import axios from '@/axios-instance';
import { RaritiesHashKey } from '../symbols';
import { RaritiesHash, Roll } from '../types';
import { useGameStore } from '@GameModule/stores/GameStore';
import { storeToRefs } from 'pinia';

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

  fetchRarities();
});

const fetchRarities = () => {
  if (!selectedGame.value) {
    return;
  }

  axios
    .get(`/game/rarities/`, { params: { game_id: selectedGame.value.id } })
    .then((response) => {
      const raritiesHash = response.data.reduce((acc, curr) => {
        if (curr.pity != 0) {
          acc[curr.id] = curr;
        }
        return acc;
      }, {});

      setRaritiesHash(raritiesHash);
    })
    .catch((error) => {
      console.log(error);
    });
};

const onRoll = () => {
  if (!selectedGame.value) {
    return;
  }

  axios
    .get(`/game/${selectedGame.value.id}/gacha/?format=json&numrolls=${numRolls.value}`)
    .then((response) => {
      rollResults.value = response.data;
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
