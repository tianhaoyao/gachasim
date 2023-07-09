import { createApp, markRaw } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import { router } from './router';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.js';
import ColorInput from 'vue-color-input';
import VueCookies from 'vue-cookies';

const pinia = createPinia();

pinia.use(({ store }) => {
  store.router = markRaw(router);
});

const app = createApp(App);

app.use(router);
app.use(pinia);
app.use(VueCookies);
app.mount('#app');
app.component('ColorInput', ColorInput);
