<template>
  <el-card>
    <el-form :model="loginForm">
      <el-form-item>
        <el-input v-model="loginForm.username" placeholder="请输入用户名"></el-input>
      </el-form-item>
      <el-form-item>
        <el-input v-model="loginForm.password" type="password" placeholder="请输入密码"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleLogin">登录</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>
<script setup lang="ts">
import { login } from '../../api';
import {reactive} from 'vue';
import router from "../../router";

const loginForm=reactive({
  username:'',
  password:''
})
const handleLogin=()=>{
  console.log(loginForm.username,'username')
  login(loginForm).then(data=>{
    console.log('登录成功',data)
    localStorage.setItem('access_token',data.access_token)
    router.push('/')
  })
}
</script>


<style scoped>

</style>