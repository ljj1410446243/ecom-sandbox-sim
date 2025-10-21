import {createRouter,createWebHashHistory} from 'vue-router'

const routes=[
    {
        path:"/",
        component:()=>import('../views/Main.vue')
    },
    {
        path:'/auth',
        component:()=>import('../views/auth/Index.vue')
    }
]

const router=createRouter({
    routes,
    history:createWebHashHistory()
})

export default router