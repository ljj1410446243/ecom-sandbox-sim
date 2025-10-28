<template>
  <div class="header-container">
    <div class="header-left flex-box">
      CEMO Simulation
    </div>
    <div class="header-right flex-box">
        <el-dropdown>
          <div>
            <el-avatar> {{ userStore.userInfo.username }} </el-avatar>
          </div>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="GoToPerson">个人中心</el-dropdown-item>
              <el-dropdown-item @click="handleLogout">登出</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
    </div>
  </div>
</template>

<script setup lang="ts">
import router from "../router";
import {onMounted, reactive} from "vue";
import {getUserInfo} from "../api";
import {useUserStore} from "../store/userStore.ts";

const userStore=useUserStore()

onMounted(()=>{
  getUserInfo().then(data=>{
    Object.assign(userStore.userInfo, data)
  }).catch(err=>{
    console.error('获取用户信息失败:', err)
  })
})
const handleLogout=()=>{
  localStorage.removeItem('access_token')
  router.push('/auth').then(() => {
    console.log('登出成功!')
  })
}
const GoToPerson=()=>{
  router.push('/person')
}
</script>

<style lang="less" scoped>
.flex-box{
  display: flex;
  align-items:center;
  height: 100%;
}
.header-container{
  display: flex;
  justify-content: space-between;
  height:100%;
}
.header-left{
  font-size: 20px;
  font-weight: bold;
  margin-left: 20px;
}
</style>