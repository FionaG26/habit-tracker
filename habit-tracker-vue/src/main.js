import { createApp } from 'vue'
import { store } from './store';
import axios from 'axios';
import './style.css'
import App from './App.vue'

const app = createApp(App);
app.use(store);
app.config.globalProperties.$axios = axios;
app.mount('#app');
