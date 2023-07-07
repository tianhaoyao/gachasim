<script lang="ts">
import { defineComponent } from 'vue';
import NavBar from './components/NavBar.vue';
import { ThemeProvider } from 'vue3-styled-components';
import { theme } from './theme';

export default defineComponent({
  name: 'App',
  components: {
    NavBar,
    ThemeProvider,
  },
  setup() {
    return { theme };
  },
});
</script>

<template>
  <ThemeProvider :theme="theme">
    <NavBar />
    <RouterView />
  </ThemeProvider>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
