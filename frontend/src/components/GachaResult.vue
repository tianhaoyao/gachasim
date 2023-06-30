<template>
  <div class="container">
    <div class="row row-cols-md-5 card-container">
      <div class="col" v-for="(roll, index) in rollResult" :key="index">
        <div class="card h-100" :style="{ backgroundColor: roll.rate.color }">
          <img :src="'http://127.0.0.1:8000' + roll.item.image" class="card-img-top" />
          <div class="card-body">
            <h5 class="card-title">{{ roll.item.item_name }}</h5>
          </div>
          <div class="card-footer">
            <div class="progress" v-for="(pity, rarity) in roll.pity" :key="rarity">
              <div
                class="progress-bar progress-bar-striped progress-bar-animated"
                role="progressbar"
                :style="{
                  width: calculatePercent(pity, ratesInfo[rarity]?.pity),
                  backgroundColor: getColor(
                    pity,
                    ratesInfo[rarity]?.softpity,
                    ratesInfo[rarity]?.color,
                  ),
                }"
                :aria-valuenow="pity"
                aria-valuemin="0"
                :aria-valuemax="ratesInfo[rarity]?.pity"
              >
                {{ pity }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  props: {
    rollResult: Object,
    ratesInfo: Object,
  },
  methods: {
    calculatePercent: function (num, denom) {
      return Math.min(Math.max(Math.floor((num / denom) * 100), 0), 100) + '%';
    },
    getColor: function (num, soft, color) {
      if (num > soft && soft != 0) {
        return '#FF0000';
      }
      return color;
    },
  },
};
</script>

<style>
.card-container > .col {
  margin-bottom: 20px;
}

.progress {
  margin-bottom: 2px;
}
</style>
