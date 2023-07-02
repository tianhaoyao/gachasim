import { createApp } from 'vue';
import App from './App.vue';
import { router } from './router';
import axios from 'axios';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.js';
import ColorInput from 'vue-color-input';

axios.defaults.baseURL = 'http://127.0.0.1:8000/';

const app = createApp(App);
app.use(router);
app.mount('#app');
app.component('ColorInput', ColorInput);
