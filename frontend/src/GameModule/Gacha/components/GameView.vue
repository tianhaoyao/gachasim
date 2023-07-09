<script setup lang="ts">
import { provide, reactive, ref, watch } from 'vue';
import GachaResult from './GachaResult.vue';
import { callApi } from '@/callApi';
import { RaritiesHashKey } from '../symbols';
import { RaritiesHash, Roll } from '../types';
import { useGameStore } from '@GameModule/stores/GameStore';
import { storeToRefs } from 'pinia';
import { Rarity } from '@RarityModule/models/Rarity';

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

  callApi<Array<Rarity>>({
    endpoint: `/game/rarities/`,
    params: { game_id: selectedGame.value.id },
  })
    .then((response) => {
      const raritiesHash = response.reduce((acc, curr) => {
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
