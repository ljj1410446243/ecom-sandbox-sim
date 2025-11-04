<template>
  <div>
    <h2>店铺概览 - {{ shopInfo.name }}</h2>
    <el-tag type="success">{{shopInfo.status}}</el-tag>
    <el-button @click="handleExitShop" type="danger">退出店铺</el-button>

    <el-tabs type="border-card" class="demo-tabs">
      <el-tab-pane>
        <template #label>
          <span class="custom-tabs-label">
            <span>我的{{shopInfo.name}}</span>
          </span>
        </template>
        Route
      </el-tab-pane>
      <el-tab-pane label="库存管理"><Inventory/></el-tab-pane>
      <el-tab-pane label="订单">订单</el-tab-pane>
      <el-tab-pane label="平台营销">营销</el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import {useRoute, useRouter} from 'vue-router'
import { useMenuStore } from '../../store/menuStore'
import {onMounted, reactive} from "vue";
import {getShopInfoById} from "../../api";
import Inventory from "../../components/myShop/Inventory.vue";

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
<style lang="less" scoped>
.demo-tabs > .el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}
.demo-tabs .custom-tabs-label .el-icon {
  vertical-align: middle;
}
.demo-tabs .custom-tabs-label span {
  vertical-align: middle;
  margin-left: 4px;
}
</style>