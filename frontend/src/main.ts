import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import 'element-plus/dist/index.css'
import ElementPlus from 'element-plus'
import router from './router'
import {createPinia} from "pinia";
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import {useMenuStore} from "./store/menuStore.ts";
//路由守卫
router.beforeEach((to)=>{
    const token=localStorage.getItem('access_token')
    if(!token&&to.path!=='/auth'){
        return '/auth'
    }
    else if(token&&to.path==='/auth'){
        return '/'
    }
    else {
        return true
    }
})

const app=createApp(App)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

const pinia=createPinia()
pinia.use(piniaPluginPersistedstate)

app.use(pinia)
app.use(router)
app.use(ElementPlus)
app.mount('#app')

const menuStore=useMenuStore()
menuStore.initDynamicRoutes()