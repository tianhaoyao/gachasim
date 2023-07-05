<script lang="ts">
import { defineComponent } from 'vue';
import axios from '@/axios-instance';
import { RegisterPageContainer } from './styles';

export default defineComponent({
  name: 'RegisterPage',
  components: {
    RegisterPageContainer,
  },
  data() {
    return {
      form: {
        userName: '',
        password: '',
        email: '',
      },
    };
  },
  methods: {
    onSubmit() {
      if (this.form.userName && this.form.password && this.form.email) {
        const payload = {
          username: this.form.userName,
          password: this.form.password,
          email: this.form.email,
        };

        axios
          .post('/auth/register/', payload)
          .then((response) => {
            console.log(response);
            // Redirect or perform other actions after successful registration
            // ...
          })
          .catch((error) => {
            // Handle registration error
            console.error(error);
          });
      }
    },
  },
});
</script>

<template>
  <RegisterPageContainer>
    <form @submit.prevent="onSubmit">
      <label>Username</label>
      <input v-model="form.userName" placeholder="Username" required />
      <label>Password</label>
      <input v-model="form.password" placeholder="Password" type="password" required />
      <label>Email</label>
      <input v-model="form.email" placeholder="Email" type="email" required />
      <button>Register</button>
    </form>
  </RegisterPageContainer>
</template>
