<script>
import axios from '@/axios-instance';
import { useUserStore } from '@UserModule/stores/UserStore';
import { mapActions } from 'pinia';

export default {
  name: 'LoginPage',
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
    ...mapActions(useUserStore, ['setUser']),
    getUserInfo() {
      axios
        .get('/auth/user-details/')
        .then((response) => {
          // Save the access token in local storage or Vuex store
          this.setUser(response.data);
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
