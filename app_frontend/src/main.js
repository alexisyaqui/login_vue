import "./assets/main.css";

import { createApp } from "vue";
import { createPinia } from "pinia";
import { plugin, defaultConfig } from "@formkit/vue"; //libreria instalada de formkit


import {toast} from 'vue3-toastify'
import 'vue3-toastify/dist/index.css';

import config from "../formkit.config"; // la configuracion viene de la configuracion creada

import App from "./App.vue";
import router from "./router";



const app = createApp(App);
app.use(createPinia());
app.use(router);
app.use(plugin, defaultConfig(config));
app.use(Vue3Toastify);

app.mount("#app");
