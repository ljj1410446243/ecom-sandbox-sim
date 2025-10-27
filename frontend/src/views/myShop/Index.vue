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
        {{myShopInfo.name||'暂无店铺'}}
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
        <el-tag size="small">{{myShopInfo.status||'未创建'}}</el-tag>

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
        {{ myShopInfo.cash_balance ? `￥${myShopInfo.cash_balance}`:'--' }}
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
      :rules="rules"
    >
      <el-form-item label="店铺名称" prop="name">
        <el-input
            placeholder="请输入店铺名称"
            v-model="shopForm.name"
        >
        </el-input>
      </el-form-item>
      <el-form-item label="初始资金" prop="cash_balance">
        <el-input
            placeholder="请输入店铺初始资金"
            v-model="shopForm.cash_balance"
        >
        </el-input>
      </el-form-item>
      <el-button type="primary" @click="handleCreateShop">创建</el-button>
    </el-form>

  </el-dialog>
</template>
<script setup lang="ts">
import {createShop, getMyShopInfo} from "../../api";
import {onMounted, reactive, ref} from "vue";
import {ElMessage} from "element-plus";

const dialogVisible=ref(false)
const myShopInfo=reactive({})

const shopForm=reactive({
  name:'',
  cash_balance:5000//默认初始资金
})

const formRef=ref()
const rules={
  name:[
    {required:true,message:'店铺名称不可为空',trigger:'blur'},
    {min:2,max:10,message:'店铺名称长度为2-10个字符',trigger: 'blur'}
  ],
  cash_balance:[
    {required:true,message:'初始资金不可为空',trigger:'blur'},
  ]
}

//获取店铺信息
const fetchShopInfo=()=>{
  getMyShopInfo().then(data=>{
    Object.assign(myShopInfo,data)
    console.log('获取店铺信息成功:', data)
  }).catch(err=>{
    console.error('获取店铺信息失败:', err)
    ElMessage.error('获取店铺信息失败')
  })
}

//创建店铺
const handleCreateShop=()=>{
  if(!formRef.value) return
  formRef.value.validate().then(()=>{
    const result=createShop(shopForm)
    result.then((result)=>{
      console.log('创建店铺成功：',result)
      ElMessage.success('创建店铺成功!')
      dialogVisible.value=false
      fetchShopInfo()//刷新店铺信息
    })
  })
}
onMounted(()=>{
  fetchShopInfo()
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