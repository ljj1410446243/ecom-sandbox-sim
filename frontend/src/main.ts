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
router.beforeEach((to,from,next)=>{
  const token = localStorage.getItem('access_token')

  // 认证逻辑
  if (!token && to.path !== '/auth') {
    next('/auth')
    return
  } else if (token && to.path === '/auth') {
    next('/')
    return
  }

  // 店铺页面检查逻辑
  if (token && to.path.startsWith('/shop/')) {
    const menuStore = useMenuStore()

    // 如果访问店铺页面但没有当前店铺信息
    if (!menuStore.currentShop) {
      // 重定向到店铺列表
      next('/myShop')
      return
    }

    // 如果访问的店铺ID与当前店铺不匹配
    const shopIdInPath = to.params.shopId as string
    if (menuStore.currentShop.id !== shopIdInPath) {
      // 重定向到当前店铺的对应页面
      const redirectPath = to.path.replace(`/myShop/${shopIdInPath}`, `/myShop/${menuStore.currentShop.id}`)
      next(redirectPath)
      return
    }
  }

  // 所有检查通过，继续导航
  next()
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
