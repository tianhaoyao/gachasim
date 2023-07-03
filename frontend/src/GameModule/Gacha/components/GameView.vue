<script lang="ts">
import { defineComponent, inject, provide, reactive } from 'vue';
import GachaResult from './GachaResult.vue';
import axios from '@/axios-instance';
import { Game } from '@GameModule/models/Game';
import { SelectedGameKey } from '@/symbols';
import { RaritiesHashKey } from '../symbols';
import { RaritiesHash, Roll } from '../types';

type GameViewData = {
  rollResults: Array<Roll>;
  game?: Game;
  numRolls: number;
};

export default defineComponent({
  name: 'GameView',
  components: {
    GachaResult,
  },
  setup() {
    const selectedGame = inject(SelectedGameKey);

    const raritiesHash = reactive<RaritiesHash>({});

    const setRaritiesHash = (res: RaritiesHash) => {
      Object.assign(raritiesHash, res);
    };

    provide(RaritiesHashKey, raritiesHash);

    return {
      selectedGame,
      setRaritiesHash,
    };
  },
  data(): GameViewData {
    return {
      rollResults: [],
      numRolls: 10,
    };
  },
  watch: {
    selectedGame() {
      this.fetchRarities();
    },
  },
  mounted() {
    this.fetchRarities();
  },
  methods: {
    onRoll: function () {
      if (!this.selectedGame) {
        return;
      }

      axios
        .get(`/game/${this.selectedGame.id}/gacha/?format=json&numrolls=${this.numRolls}`)
        .then((response) => {
          this.rollResults = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    fetchRarities: function () {
      if (!this.selectedGame) {
        return;
      }
      axios
        .get(`/game/rarities/`, { params: { game_id: this.selectedGame.id } })
        .then((response) => {
          const raritiesHash = response.data.reduce((acc, curr) => {
            if (curr.pity != 0) {
              acc[curr.id] = curr;
            }
            return acc;
          }, {});

          this.setRaritiesHash(raritiesHash);
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
});
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
