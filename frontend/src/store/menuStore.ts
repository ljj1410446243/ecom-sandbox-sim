import {defineStore} from "pinia";
import {reactive} from "vue";

export interface MenuItem {
    index: string
    title: string
    icon?: string
    path?: string
    children?: MenuItem[]
    disabled?: boolean
    component?:string
}

export const useMenuStore=defineStore('menu',()=>{
    const menus=reactive<MenuItem[]>([
        {
            index:'1',
            title:'首页',
            icon:'Location',
            path:'/home',
            component:'home'
        },
        {
            index:'2',
            title:'任务',
            icon:'Operation',
            path:'/tasks',
            component:'tasks'
        },
        {
            index:'3',
            title:'采购管理',
            icon:'Document',
            path:'/purchase',
            component:'purchase'
        },
        {
            index:'4',
            title:'店铺运营',
            icon:'Setting',
            children:[
                {index:'4-1',title:'我的店铺',path:'/myShop',component:'myShop'},
                {index:'4-2',title:'店铺设置',path:'/setShop',component:'setShop'},
            ],
        },
    ])


    return {menus}
})