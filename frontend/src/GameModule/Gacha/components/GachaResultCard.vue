<script setup lang="ts">
import { Roll } from '../types';
import { getColor, calculatePercent } from '../utils';
import { RaritiesHashKey } from '../symbols';
import { injectStrict } from '@/utils';

type Props = {
  roll: Roll;
};

defineOptions({
  name: 'GachaResultCard',
  methods: {
    getColor,
    calculatePercent,
  },
});

defineProps<Props>();

const raritiesHash = injectStrict(RaritiesHashKey);
</script>

<template>
  <div v-if="raritiesHash" class="card h-100" :style="{ backgroundColor: roll.rarity.color }">
    <img :src="'http://127.0.0.1:8000' + roll.item.image" class="card-img-top" />
    <div class="card-body">
      <h5 class="card-title">{{ roll.item.item_name }}</h5>
    </div>
    <div class="card-footer">
      <div v-for="(pityCount, rarityId) in roll.pity" :key="rarityId" class="progress">
        <div
          class="progress-bar progress-bar-striped progress-bar-animated"
          role="progressbar"
          :style="{
            width: calculatePercent({ pityCount, rarityPity: raritiesHash[rarityId]?.pity }),
            backgroundColor: getColor({
              pityCount,
              softPity: raritiesHash[rarityId]?.softpity,
              color: raritiesHash[rarityId]?.color,
            }),
          }"
          :aria-valuenow="pityCount"
          aria-valuemin="0"
          :aria-valuemax="raritiesHash[rarityId]?.pity"
        >
          {{ pityCount }}
        </div>
      </div>
    </div>
  </div>
</template>
