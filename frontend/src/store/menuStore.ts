import {defineStore} from "pinia";
import {ref} from "vue";

export const useMenuStore=defineStore('menu',()=>{
    const savedShop=JSON.parse(localStorage.getItem('currentShop') || 'null')

    const baseMenus=ref([
        {
            index:'1',
            title:'首页',
            icon:'Location',
            path:'/home',
        },
        {
            index:'2',
            title:'任务',
            icon:'Operation',
            path:'/tasks',
        },
        {
            index:'3',
            title:'采购管理',
            icon:'Document',
            path:'/purchase',
        },
        {
            index:'4',
            title:'店铺运营',
            icon:'Setting',
            children:[
                {
                    index:'4-1',
                    title:'店铺设置',
                    icon:'Setting',
                    path:'/myShop',
                },
            ]
        },
    ])

    const currentShop=ref<{id:string,name:string}|null>(savedShop)

    //完整菜单
    const menus=ref([...baseMenus.value])

    //动态更新菜单
    const updateMenus=()=>{
        const updatedMenus = JSON.parse(JSON.stringify(baseMenus.value))
        const shopOperationMenu=updatedMenus.find(menu=>menu.index==='4')
        if(shopOperationMenu && currentShop.value){
            if(shopOperationMenu.children){
                shopOperationMenu.children=shopOperationMenu.children.filter(
                    child=>!child.index.startsWith('4-2')
                )
            }
            //添加当前店铺菜单
            shopOperationMenu.children.push({
                index:'4-2',
                title:currentShop.value.name,
                icon:'Shop',
                path:`/myShop/${currentShop.value.id}`
            })
        }
        menus.value=updatedMenus
        console.log('当前菜单：',updatedMenus)
    }

    // 设置当前店铺
    const setCurrentShop = (shopId: string, shopName: string) => {
        currentShop.value = { id: shopId, name: shopName }
        // 保存到 localStorage
        localStorage.setItem('currentShop', JSON.stringify(currentShop.value))
        updateMenus()
    }

    // 退出店铺
    const exitShop = () => {
        currentShop.value = null
        localStorage.removeItem('currentShop')
        updateMenus()
    }

    // 初始化时更新菜单
    if (currentShop.value) {
        updateMenus()
    }

    return {menus,currentShop,setCurrentShop,exitShop}
})