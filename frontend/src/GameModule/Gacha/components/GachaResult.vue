<script setup lang="ts">
import GachaResultCard from './GachaResultCard.vue';
import { Roll } from '../types';

type Props = {
  rollResults: Array<Roll>;
};

defineOptions({
  name: 'GachaResult',
  components: {
    GachaResultCard,
  },
});

const props = defineProps<Props>();
</script>

<template>
  <div class="container">
    <div class="row row-cols-md-5 card-container">
      <div v-for="(roll, index) in props.rollResults" :key="index" class="col">
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
