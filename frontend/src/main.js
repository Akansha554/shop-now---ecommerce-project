import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './assets/main.css'
import { formatPrice, formatDate, truncate } from './utils/helpers'

const app = createApp(App)

app.config.globalProperties.$formatPrice = formatPrice
app.config.globalProperties.$formatDate  = formatDate
app.config.globalProperties.$truncate    = truncate

app.use(router).use(store).mount('#app')