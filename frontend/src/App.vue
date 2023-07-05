<script lang="ts">
import { computed, defineComponent, provide, reactive } from 'vue';
import { Game } from '@GameModule/models/Game';
import { User } from '@UserModule/models/User';
import {
  SelectedGameKey,
  SetSelectedGameKey,
  LoggedInUserKey,
  SetLoggedInUserKey,
} from '@/symbols';
import NavBar from './components/NavBar.vue';
import { useRouter, useRoute } from 'vue-router';
import { ThemeProvider } from 'vue3-styled-components';
import { theme } from './theme';

type AppState = {
  selectedGame?: Game;
  loggedInUser?: User;
};

export default defineComponent({
  name: 'App',
  components: {
    NavBar,
    ThemeProvider,
  },
  setup() {
    const state = reactive<AppState>({
      selectedGame: undefined,
      loggedInUser: undefined,
    });

    const router = useRouter();

    const route = useRoute();

    const path = computed(() => route.path);

    const selectedGame = computed(() => state.selectedGame);

    const setSelectedGame = (game: Game) => {
      state.selectedGame = game;
      // redirect user back to home whenever selecting a new game if not on home
      if (path.value !== '/home') {
        router.push('/home');
      }
    };

    provide(SelectedGameKey, selectedGame);
    provide(SetSelectedGameKey, setSelectedGame);

    const loggedInUser = computed(() => state.loggedInUser);

    const setLoggedInUser = (user: User) => {
      state.loggedInUser = user;
      // redirect user back to home whenever selecting a new game if not on home
      if (path.value !== '/home') {
        router.push('/home');
      }
    };

    provide(LoggedInUserKey, loggedInUser);
    provide(SetLoggedInUserKey, setLoggedInUser);

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
