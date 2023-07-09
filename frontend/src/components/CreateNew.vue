<script setup lang="ts">
defineOptions({
  name: 'CreateNew',
});
</script>

<template>
  <router-link to="/home" class="button">DONE</router-link>
  <router-link to="/create/item" class="button">Create New Item</router-link>
  <router-link to="/create/rarity" class="button">Create New Rarity</router-link>
  <router-link to="/create/game" class="button">Create New Game</router-link>
</template>

<style></style>
