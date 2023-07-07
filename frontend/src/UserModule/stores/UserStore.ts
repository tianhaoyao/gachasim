import { User } from '@UserModule/models/User';
import { defineStore } from 'pinia';

type UserStoreState = {
  user: User | undefined;
};

type UserStoreGetters = {
  getUser: (state: UserStoreState) => User | undefined;
};

type UserStoreActions = {
  setUser: (user: User) => void;
};

export const useUserStore = defineStore<'user', UserStoreState, UserStoreGetters, UserStoreActions>(
  'user',
  {
    state: () => ({
      user: undefined,
    }),
    getters: {
      getUser(state) {
        return state.user;
      },
    },
    actions: {
      // any amount of arguments, return a promise or not
      setUser(user: User) {
        // you can directly mutate the state
        this.user = user;

        // redict to home page if not already
        if (this.router.currentRoute.value.path !== '/home') {
          this.router.push('/home');
        }
      },
    },
  }
);
