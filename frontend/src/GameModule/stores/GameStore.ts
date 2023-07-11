import { Game } from '@GameModule/models/Game';
import { defineStore } from 'pinia';

type GameStoreState = {
  selectedGame: Game | undefined;
};

type GameStoreGetters = {
  getSelectedGame: (state: GameStoreState) => Game | undefined;
};

type GameStoreActions = {
  setSelectedGame: (Game: Game) => void;
};

export const useGameStore = defineStore<'Game', GameStoreState, GameStoreGetters, GameStoreActions>(
  'Game',
  {
    state: () => ({
      selectedGame: undefined,
    }),
    getters: {
      getSelectedGame(state) {
        return state.selectedGame;
      },
    },
    actions: {
      // any amount of arguments, return a promise or not
      setSelectedGame(Game: Game) {
        // you can directly mutate the state
        this.selectedGame = Game;

        // redirect to home page if not already
        if (this.router.currentRoute.value.path !== '/home') {
          this.router.push('/home');
        }
      },
    },
  }
);
