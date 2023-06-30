<template>
  <img :src="'http://127.0.0.1:8000' + gameimage.image">
  <div class="game">
    <input v-model="numrolls" number>
    <button v-on:click="roll()">Reroll</button>
    <GachaResult :rollResult="rolls" :ratesInfo="rarityObj"></GachaResult>
  </div>
</template>

<script>
import GachaResult from "./GachaResult.vue";
import axios from 'axios'

export default {
  name: 'GameView',
  props: {
    gameId: Number
  },
  components: {
    GachaResult,
  },
  data() {
    return {
      rolls: {},
      gameimage: "",
      ratesInfo: {},
      numrolls: 10,
      rarityObj: {},
    }
  },
  mounted() {
    this.roll()
    this.getimage()
    this.getRatesInfo()
  },
  watch: {
    gameId() {
      this.getimage()
      this.getRatesInfo()
      this.roll()
    }
  },
  methods: {
    roll: function () {
      axios
        .get(`/game/${this.gameId}/gacha/?format=json&numrolls=${this.numrolls}`)
        .then(response => {
          this.rolls = response.data
        })
        .catch(error => {
          console.log(error)
        })
    },
    getimage: function () {
      axios
        .get(`/game/${this.gameId}/`)
        .then(response => {
          this.gameimage = response.data
        })
        .catch(error => {
          console.log(error)
        })
    },
    getRatesInfo: function () {
      axios
        .get(`/game/rates/`, { params: { game: this.gameId } })
        .then(response => {
          this.ratesInfo = response.data
          for (var i = 0; i < this.ratesInfo.length; i++) {
            let rateObject = this.ratesInfo[i]

            if (rateObject.pity != 0) {
              this.rarityObj[rateObject.rarity] = rateObject
            }
          }
        })
        .catch(error => {
          console.log(error)
        })

    }
  }
}
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
