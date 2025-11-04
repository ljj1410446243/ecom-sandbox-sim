<template>
  <div class="shop-page">
    <!-- 搜索框 -->
    <div class="search-container flex-box">
      <el-input
        v-model="searchQuery"
        placeholder="搜索商品"
        suffix-icon="el-icon-search"
        @keyup.enter="handleSearch"
        class="search-input"
      />
      <el-button type="primary" @click="handleSearch">搜索</el-button>
    </div>

    <!-- 商品列表 -->
    <div class="product-list">
      <el-row :gutter="20">
        <el-col :span="8" v-for="product in productList" :key="product.id" >
          <ProductCard :product="product" />
        </el-col>
      </el-row>
    </div>

    <!-- 没有商品时显示空状态 -->
    <div v-if="!total">
      <el-empty description="没有商品数据" />
    </div>

    <!-- 分页 -->
    <div class="pagination-container">
      <el-pagination
        :current-page="currentPage"
        :page-size="pageSize"
        :total="total"
        layout="prev, pager, next, total"
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>
<script setup lang="ts">
import {onMounted, ref} from "vue";
  import {getProducts} from "../../api";
  import {ElMessage} from "element-plus";
  import ProductCard from "../../components/ProductCard.vue";

  export interface ProductInfo{
    id:string
    name:string
    product_code:string
    category:string
    base_cost:string
  }

  const productList=ref<ProductInfo[]>()

  //获取商品信息
  const fetchProductInfo=()=>{
    getProducts().then((res:ProductInfo[])=>{
      console.log('获取商品信息成功:', res)
      // 搜索过滤
      let filteredData = res
      if (searchQuery.value) {
        filteredData = res.filter(product =>
          product.name.includes(searchQuery.value) ||
          product.product_code.includes(searchQuery.value)
        )
      }

      // 分页处理
      const start = (currentPage.value - 1) * pageSize.value
      const end = start + pageSize.value
      productList.value = filteredData.slice(start, end)
      total.value = filteredData.length

      console.log('商品列表:', productList.value)
    }).catch(err=>{
      console.error('获取商品信息失败:', err)
      ElMessage.error('获取商品信息失败')
    })
  }

  const searchQuery = ref('')
  const currentPage = ref(1)
  const pageSize = ref(10)
  const total = ref(0)

  //处理搜索
  const handleSearch = () => {
    // 在这里实现搜索逻辑
    console.log('搜索查询:', searchQuery.value)
    // 你可以根据 searchQuery.value 过滤 productList
    currentPage.value = 1  // 搜索时返回第一页
    fetchProductInfo()
  }

  //处理页码变化
  const handlePageChange = (newPage: number) => {
    currentPage.value = newPage
    fetchProductInfo()
  }

  onMounted(()=>{
    fetchProductInfo()
  })
</script>


<style scoped>

</style>