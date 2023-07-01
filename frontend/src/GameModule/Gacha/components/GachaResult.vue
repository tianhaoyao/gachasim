<script lang="ts">
import { defineComponent, PropType } from 'vue';
import { getColor, calculatePercent } from '../utils';
import { RarityId, Rarity } from '@RarityModule/models/Rarity';
import { Item } from '@ItemModule/models/Item';
import GachaResultCard from './GachaResultCard.vue';

type Roll = {
  rarity: Rarity;
  item: Item;
  pity: Record<RarityId, number>;
};

export default defineComponent({
  name: 'GachaResult',
  components: {
    GachaResultCard,
  },
  props: {
    rollResults: {
      type: Array as PropType<Array<Roll>>,
      required: true,
    },
  },
  methods: {
    getColor,
    calculatePercent,
  },
});
</script>

<template>
  <div class="container">
    <div class="row row-cols-md-5 card-container">
      <div v-for="(roll, index) in rollResults" :key="index" class="col">
        <GachaResultCard :roll="roll" />
      </div>
    </div>
  </div>
</template>

<style>
.card-container > .col {
  margin-bottom: 20px;
}

.progress {
  margin-bottom: 2px;
}
</style>
