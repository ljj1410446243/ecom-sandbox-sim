import {createRouter, createWebHashHistory} from 'vue-router'


const routes=[
    {
        path:"/",
        redirect:'/home',
        component:()=>import('../views/Main.vue'),
        children:[
            {path:'/home',component:()=>import('../views/home/Index.vue')},
            {path:'/tasks',component:()=>import('../views/tasks/Index.vue')},
            {path:'/purchase',component:()=>import('../views/purchase/Index.vue')},
            {path:'/myShop',component:()=>import('../views/myShop/Shops.vue')},
            {path:'/myShop/:shopId',component:()=>import('../views/myShop/Index.vue')}
        ]
    },
    {
        path:'/auth',
        component:()=>import('../views/auth/Index.vue')
    },
    {
        path:'/person',
        component:()=>import('../views/person/Index.vue')
    }
]

const router=createRouter({
    routes,
    history:createWebHashHistory()
})


export default router