import { createApp, markRaw } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import { router } from './router';
import axios from 'axios';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.js';
import ColorInput from 'vue-color-input';

axios.defaults.baseURL = 'http://127.0.0.1:8000/';

const pinia = createPinia();

pinia.use(({ store }) => {
  store.router = markRaw(router);
});

const app = createApp(App);

app.use(router);
app.use(pinia); // make sure this line is the one right above app.mount() for pinia to work properly in devtools
app.mount('#app');
app.component('ColorInput', ColorInput);
