<script>
import axios from 'axios';

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
          console.log('authorized');
          console.log(accessToken);
          // Redirect or perform other actions after successful login
          // ...
        })
        .catch((error) => {
          // Handle login error
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
