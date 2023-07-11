<script setup lang="ts">
import { login } from '@/UserModule/api/login';
import { ref } from 'vue';

defineOptions({
  name: 'LoginPage',
});

const userName = ref('');
const password = ref('');

const handleLogin = async () => {
  login({
    userName: userName.value,
    password: password.value,
  });
};
</script>

<template>
  <div>
    <input v-model="userName" placeholder="Username" />
    <input v-model="password" placeholder="Password" type="password" />
    <button @click="handleLogin">Login</button>
  </div>
</template>
