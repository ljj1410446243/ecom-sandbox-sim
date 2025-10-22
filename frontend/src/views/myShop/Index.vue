<template>
    <el-descriptions
      class="margin-top"
      title="With border"
      :column="3"
      border
    >
      <template #extra>
        <el-button type="primary" @click="dialogVisible=true">创建店铺</el-button>
      </template>
      <el-descriptions-item>
        <template #label>
          <div class="cell-item">
            <el-icon >
              <user />
            </el-icon>
            店铺名称
          </div>
        </template>
        {{myShopInfo.name}}
      </el-descriptions-item>
      <el-descriptions-item>
        <template #label>
          <div class="cell-item">
            <el-icon >
              <iphone />
            </el-icon>
            店铺状态
          </div>
        </template>
        <el-tag size="small">{{myShopInfo.status}}</el-tag>

      </el-descriptions-item>
      <el-descriptions-item>
        <template #label>
          <div class="cell-item">
            <el-icon>
              <location />
            </el-icon>
            现金余额
          </div>
        </template>
        {{ myShopInfo.cash_balance }}
      </el-descriptions-item>
      <el-descriptions-item>
        <template #label>
          <div class="cell-item">
            <el-icon >
              <tickets />
            </el-icon>
            Remarks
          </div>
        </template>
        <el-tag size="small">School</el-tag>
      </el-descriptions-item>
      <el-descriptions-item>
        <template #label>
          <div class="cell-item">
            <el-icon >
              <office-building />
            </el-icon>
            Address
          </div>
        </template>
        No.1188, Wuzhong Avenue, Wuzhong District, Suzhou, Jiangsu Province
      </el-descriptions-item>
  </el-descriptions>
  <el-dialog
    v-model="dialogVisible"
    title="开设店铺"
    width="500px"
  >
    <el-form
      ref="formRef"
      label-position="left"
      label-width="100"
      :model="shopForm"
    >
      <el-form-item label="店铺名称">
        <el-input placeholder="请输入店铺名称">
        </el-input>
      </el-form-item>
      <el-form-item label="店铺初始资金">
        <el-input placeholder="请输入店铺初始资金">
        </el-input>
      </el-form-item>
      <el-button type="primary">创建</el-button>
    </el-form>

  </el-dialog>
</template>
<script setup lang="ts">
import {createShop, getMyShopInfo} from "../../api";
import {onMounted, reactive, ref} from "vue";

const dialogVisible=ref(false)
const myShopInfo=reactive({})



onMounted(()=>{
  getMyShopInfo().then(data=>{
    Object.assign(myShopInfo, data)
    console.log('获取店铺信息成功:', data)
    console.log('注入店铺信息成功:', myShopInfo)
  })
})
</script>


<style scoped>
.cell-item {
  display: flex;
  align-items: center;
}
.margin-top {
  margin-top: 20px;
}
</style>