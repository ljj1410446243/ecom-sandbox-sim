<template>
  <div>
    <h2>店铺概览 - {{ shopInfo.name }}</h2>
    <el-tag type="success">{{shopInfo.status}}</el-tag>
    <el-button @click="handleExitShop" type="danger">退出店铺</el-button>
    <p>欢迎来到店铺管理页面</p>
  </div>
</template>

<script setup lang="ts">
import {useRoute, useRouter} from 'vue-router'
import { useMenuStore } from '../../store/menuStore'
import {onMounted, reactive} from "vue";
import {getShopInfoById} from "../../api";

const route = useRoute()
const router = useRouter()
const menuStore = useMenuStore()
const shopInfo=reactive({})

const handleExitShop =  () => {

  menuStore.exitShop()
  console.log('已退出店铺')
  router.push('/myShop')

}
onMounted(()=>{
  console.log('当前店铺ID:',route.params.shopId)
  getShopInfoById(route.params.shopId as string).then((result)=>{
    Object.assign(shopInfo,result)
    console.log('店铺信息:',shopInfo)
  })
})
</script>