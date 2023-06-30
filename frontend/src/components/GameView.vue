<template>
  <img :src="'http://127.0.0.1:8000' + game?.image" />
  <div class="game">
    <input v-model="numRolls" number />
    <button v-on:click="roll()">Reroll</button>
    <GachaResult :roll-result="rolls" :rates-info="rarityObj" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import GachaResult from './GachaResult.vue';
import axios from 'axios';
import { Rarity, RarityId } from '../models/Rarity';
import { Item } from '../models/Item';
import { Game } from '../models/Game';

declare type Roll = {
  rarity: Rarity;
  item: Item;
  pity: Record<RarityId, number>;
};

declare type ComponentData = {
  rolls: Array<Roll>;
  game?: Game;
  numRolls: number;
  rarityObj: Record<RarityId, Rarity>;
};

export default defineComponent({
  name: 'GameView',
  components: {
    GachaResult,
  },
  props: {
    gameId: { type: Number, required: true },
  },
  data(): ComponentData {
    return {
      rolls: [],
      game: undefined,
      numRolls: 10,
      rarityObj: {},
    };
  },
  watch: {
    gameId() {
      this.getImage();
      this.getRatesInfo();
      this.roll();
    },
  },
  mounted() {
    this.roll();
    this.getImage();
    this.getRatesInfo();
  },
  methods: {
    roll: function () {
      axios
        .get(`/game/${this.gameId}/gacha/?format=json&numrolls=${this.numRolls}`)
        .then((response) => {
          this.rolls = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getImage: function () {
      axios
        .get(`/game/${this.gameId}/`)
        .then((response) => {
          this.game = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getRatesInfo: function () {
      axios
        .get(`/game/rates/`, { params: { game: this.gameId } })
        .then((response) => {
          this.rarityObj = response.data.reduce((acc, curr) => {
            if (curr.pity != 0) {
              acc[curr.id] = curr;
            }
            return acc;
          }, {});
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
});
</script>

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
