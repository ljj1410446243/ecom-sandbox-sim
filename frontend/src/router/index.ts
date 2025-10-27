import {createRouter, createWebHashHistory} from 'vue-router'


const routes=[
    {
        path:"/",
        component:()=>import('../views/Main.vue'),
        children:[
            {
                path:'/home',
                component:()=>import('../views/home/Index.vue'),
                meta:{title:'首页'}
            },
            {
                path:'/tasks',
                component:()=>import('../views/tasks/Index.vue'),
                meta:{title:'任务'}
            },
            {
                path:'/purchase',
                component:()=>import('../views/purchase/Index.vue'),
                meta:{title:'采购管理'}
            },
            {
                path:'/myShop',
                component:()=>import('../views/myShop/Index.vue'),
                meta:{title:'我的店铺'}
            },
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