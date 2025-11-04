<template>
  <div class="shop-container">
    <el-button @click="dialogVisible=true" type="primary">创建店铺</el-button>
    <div v-if="shopList.length>0">
      <el-card
        v-for="shop in shopList"
        :key="shop.id"
        border
        class="shop-card"
      >
        <el-row>
          <el-col :span="8" class="left">
            <div class="title">{{shop.name}}</div>
            <el-tag type="success">{{shop.status}}</el-tag>
          </el-col>
          <el-col :span="16">
            <el-button color="#12a6a6" @click="handleEnterShop(shop)">进入店铺</el-button>
            <el-button type="danger" @click="handleDelete(shop.id)">删除</el-button>
          </el-col>
        </el-row>



      </el-card>
    </div>

    <!--  无店铺时提示-->
    <div v-else>
      <el-empty
        description="您还没有店铺，快去创建一个吧！"
        class="margin-top"
      >
      </el-empty>
    </div>
    <!--   创建店铺对话框-->
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
        <el-form-item label="初始资金" prop="initial_balance">
          <el-input-number
              placeholder="请输入店铺初始资金"
              v-model="shopForm.initial_balance"
          >
          </el-input-number>
        </el-form-item>
        <el-button type="primary" @click="handleCreateShop">创建</el-button>
      </el-form>

    </el-dialog>
  </div>
</template>
<script setup lang="ts">
import {createShop, deleteShop, getMyShopInfo} from "../../api";
import {onMounted, reactive, ref} from "vue";
import {ElMessage} from "element-plus";
import {useMenuStore} from "../../store/menuStore.ts";
import router from "../../router";

const dialogVisible=ref(false)
const menuStore=useMenuStore()

// 店铺信息接口定义
interface shopInfo {
  id: number;
  name: string;
  status: string;
  cash_balance: string; // 改为 string 类型
  owner_user_id: number;
  created_at?: string; // 设为可选字段
}

const shopList=ref<shopInfo[]>([])

const shopForm=reactive({
  name:'',
  initial_balance:5000//默认初始资金
})

const formRef=ref()
const rules={
  name:[
    {required:true,message:'店铺名称不可为空',trigger:'blur'},
    {min:2,max:10,message:'店铺名称长度为2-10个字符',trigger: 'blur'}
  ],
  initial_balance:[
    {required:true,message:'初始资金不可为空',trigger:'blur'},
  ]
}

//获取店铺信息
const fetchShopInfo = () => {
  getMyShopInfo().then((res: shopInfo[]) => {
    shopList.value = res
  }).catch(err => {
    console.error('获取店铺信息失败:', err)
    ElMessage.error('获取店铺信息失败')
  })
}


//创建店铺
const handleCreateShop=()=>{
  if(!formRef.value) return
  formRef.value.validate().then(()=>{
    console.log('创建店铺表单验证通过:',shopForm)
    const result=createShop(shopForm)
    result.then((result)=>{
      console.log('创建店铺成功：',result)
      ElMessage.success('创建店铺成功!')
      dialogVisible.value=false
      // 重置表单
      shopForm.name = '';
      shopForm.initial_balance = 5000;
      //刷新店铺信息
      fetchShopInfo()
    })
  })
}
//删除店铺按钮
const handleDelete=(id:string)=>{
  deleteShop(id).then(()=>{
    ElMessage.success('删除店铺成功')
    fetchShopInfo()
  }).catch(err=>{
    console.error('删除店铺失败:',err)
    ElMessage.error('删除店铺失败')
  })
}
//进入店铺
const handleEnterShop=(shop)=>{
  menuStore.setCurrentShop(shop.id,shop.name)
  router.push(`/myShop/${shop.id}`)
}
onMounted(()=>{
  fetchShopInfo()
})
</script>


<style scoped>
.shop-container{
  background-color: #d9dfe7;
  width: 100%;
  height: 100%;
  margin: 20px;
  padding: 20px;
}
.margin-top {
  margin-top: 20px;
}
.left{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.title{
  font-weight: bold;
  font-size: large;
  padding-bottom: 10px;
}
.shop-card{
  padding-top:20px;
  margin: 20px 0;
}
</style>