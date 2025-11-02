<template>
  <div>
    <h2>店铺概览 - {{ $route.params.shopId }}</h2>
    <el-button @click="handleExitShop">退出店铺</el-button>
    <p>欢迎来到店铺管理页面</p>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useMenuStore } from '../../store/menuStore'

const router = useRouter()
const menuStore = useMenuStore()

const handleExitShop =  () => {

  menuStore.exitShop()
  console.log('已退出店铺')
  router.push('/myShop')

}
</script>