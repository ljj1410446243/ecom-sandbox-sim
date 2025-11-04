<template>
  <el-table :data="tableData" style="width: 100%">
    <el-table-column fixed prop="id" label="库存id" width="120" />
    <el-table-column prop="product_code" label="商品编码" width="120" />
    <el-table-column prop="product_name" label="商品名称" width="120" />
    <el-table-column prop="category" label="商品类别" width="120" />
    <el-table-column prop="on_hand_qty" label="库存量" width="120" />
    <el-table-column fixed="right" label=操作 min-width="120">
      <template #default>
        <el-button link type="primary" size="small" @click="handleClick">
          Detail
        </el-button>
        <el-button link type="primary" size="small">Edit</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>
<script setup lang="ts">
import {computed, onMounted} from "vue";
import {ref} from "vue";
import {getInventory, getProductInfoById} from "../../api";
// 库存项接口
interface InventoryInfo {
  id: number
  product_id: number
  on_hand_qty: number
}

// 商品信息接口
interface ProductInfo {
  id: number
  name: string
  product_code: string
  category: string
  base_cost: string
  // 根据实际API返回字段添加
}

const inventoryList=ref<InventoryInfo>([])
const productList=ref<ProductInfo>([])

//获取库存信息
const fetchInventory=()=>{
  getInventory().then(res=>{
    inventoryList.value=res
    tableData.value.push(inventoryList.value)
    console.log('获取库存信息成功:', res)
    console.log('inventoryList:', inventoryList.value)
    fetchProductInfo()
  })
}
//获取详细商品信息
const fetchProductInfo= async ()=>{
  try {
    const productPromises=inventoryList.value.map(item=>{
      return getProductInfoById(item.product_id.toString())
    })
    const products=await Promise.all(productPromises)
    productList.value=products.flat()
    console.log('获取商品信息成功:', productList.value)
  }catch (err){
    console.error('获取商品信息失败:', err)
  }
}

//整合信息
const tableData=computed(()=>{
  return inventoryList.value.map(inventory=>{
    const product=productList.value.find(p=>p.id===inventory.product_id)
    return {
      ...inventory,
      product_name:product?.name||'未知商品',
      product_code:product?.product_code||'未知编码',
      category:product?.category||'未知类别',

    }
  })
})
const handleClick=()=>{
  console.log('点击了详情按钮')
}

onMounted(()=>{
  fetchInventory()
})
</script>


<style scoped>

</style>