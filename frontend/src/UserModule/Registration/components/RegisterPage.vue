<script lang="ts">
import { defineComponent } from 'vue';
import { callApi } from '@/callApi';
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
        const requestInit = {
          method: 'POST',
          body: JSON.stringify({
            username: this.form.userName,
            password: this.form.password,
            email: this.form.email,
          }),
        };

        callApi({
          endpoint: '/auth/register/',
          requestInit: requestInit,
        })
          .then((response) => {
            console.log(response);
          })
          .catch((error) => {
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
