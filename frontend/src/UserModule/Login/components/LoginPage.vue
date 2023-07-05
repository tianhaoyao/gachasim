<script>
import { SetLoggedInUserKey, LoggedInUserKey } from '@/symbols';
import axios from '@/axios-instance';
import { inject } from 'vue';

export default {
  name: 'LoginPage',
  setup() {
    const setLoggedInUser = inject(SetLoggedInUserKey);
    const loggedInUser = inject(LoggedInUserKey);

    return {
      setLoggedInUser,
      loggedInUser,
    };
  },
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    login() {
      axios
        .post('/auth/token/', {
          username: this.username,
          password: this.password,
        })
        .then((response) => {
          // Save the access token in local storage or Vuex store
          const accessToken = response.data.access;
          localStorage.setItem('accessToken', accessToken);
          this.getUserInfo();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getUserInfo() {
      axios
        .get('/auth/user-details/')
        .then((response) => {
          // Save the access token in local storage or Vuex store
          this.setLoggedInUser(response.data);
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>

<template>
  <div>
    <input v-model="username" placeholder="Username" />
    <input v-model="password" placeholder="Password" type="password" />
    <button @click="login">Login</button>
  </div>
</template>
