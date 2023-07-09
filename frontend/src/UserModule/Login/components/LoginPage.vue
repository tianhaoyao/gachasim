<script>
import { callApi } from '@/callApi';
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
    async login() {
      try {
        const requestInit = {
          method: 'POST',
          body: JSON.stringify({
            username: this.username,
            password: this.password,
          }),
        };
        const response = await callApi({
          endpoint: '/auth/token/',
          requestInit,
        });

        // Save the access token in cookie
        const accessToken = response.access;
        const refreshToken = response.refresh;

        // save access-expiration time cookie set to 5 minutes
        const accessExpiry = new Date(Date.now() + 300 * 1000);
        // save refresh-expiration time cookie set to 1 day
        const refreshExpiry = new Date(Date.now() + 86400 * 1000);

        this.$cookies.set('access-token', accessToken);
        this.$cookies.set('refresh-token', refreshToken);
        this.$cookies.set('access-expiry', accessExpiry.toUTCString());
        this.$cookies.set('refresh-expiry', refreshExpiry.toUTCString());

        this.getUserInfo();
      } catch (error) {
        console.error(error);
      }
    },
    ...mapActions(useUserStore, ['setUser']),
    getUserInfo() {
      callApi({ endpoint: '/auth/user-details/' })
        .then((response) => {
          // Save the user details in local storage or Vuex store
          this.setUser(response);
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
