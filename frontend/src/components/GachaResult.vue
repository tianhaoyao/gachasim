<template>
  <div class="container">
    <div class="row row-cols-md-5 card-container">
      <div class="col" v-for="(roll, index) in rollResult" :key="index">
        <div class="card h-100" :style="{ backgroundColor: roll.rarity.color }">
          <img :src="'http://127.0.0.1:8000' + roll.item.image" class="card-img-top" />
          <div class="card-body">
            <h5 class="card-title">{{ roll.item.item_name }}</h5>
          </div>
          <div class="card-footer">
            <div class="progress" v-for="(pityCount, rarityId) in roll.pity" :key="rarityId">
              <div
                class="progress-bar progress-bar-striped progress-bar-animated"
                role="progressbar"
                :style="{
                  width: calculatePercent({ pityCount, rarityPity: ratesInfo[rarityId]?.pity }),
                  backgroundColor: getColor({
                    pityCount,
                    softPity: ratesInfo[rarityId]?.softpity,
                    color: ratesInfo[rarityId]?.color,
                  }),
                }"
                :aria-valuenow="pityCount"
                aria-valuemin="0"
                :aria-valuemax="ratesInfo[rarityId]?.pity"
              >
                {{ pityCount }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
import { defineComponent, PropType } from 'vue';
import { getColor, calculatePercent } from './utils';
import { RarityId, Rarity } from '../models/Rarity';
import { Item } from '../models/Item';

type Roll = {
  rarity: Rarity;
  item: Item;
  pity: Record<RarityId, number>;
};

export default defineComponent({
  props: {
    rollResult: {
      type: Array as PropType<Array<Roll>>,
    },
    ratesInfo: {
      type: Object as PropType<Record<RarityId, Rarity>>,
      required: true,
    },
  },
  methods: {
    getColor,
    calculatePercent,
  },
  // mounted: function () {
  //   console.log(this.rollResult);
  // },
});
</script>

<style>
.card-container > .col {
  margin-bottom: 20px;
}

.progress {
  margin-bottom: 2px;
}
</style>
