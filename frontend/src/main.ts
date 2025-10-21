import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import 'element-plus/dist/index.css'
import ElementPlus from 'element-plus'
import router from './router'


const app=createApp(App)
app.use(router)
app.use(ElementPlus)
app.mount('#app')

