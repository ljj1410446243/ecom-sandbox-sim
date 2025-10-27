<template>
  <el-card>
    <div>
      <el-link type="primary" @click="handleChange">{{formType?'注册账号' : '返回登录'}}</el-link>
    </div>

    <el-form
        :model="loginForm"
        :rules="rules"
        ref="loginFormRef"
    >
      <el-form-item prop="username">
        <el-input v-model="loginForm.username" placeholder="请输入用户名"></el-input>
      </el-form-item>
      <el-form-item prop="password">
        <el-input v-model="loginForm.password" type="password" placeholder="请输入密码"></el-input>
      </el-form-item>

      <el-form-item prop="email" v-if="!formType">
        <el-input v-model="loginForm.email" placeholder="请输入邮箱"></el-input>
      </el-form-item>
      <el-form-item prop="displayName" v-if="!formType">
        <el-input v-model="loginForm.display_name" placeholder="请输入姓名"></el-input>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="handleSubmit">{{formType?'登录' : '注册'}}</el-button>
      </el-form-item>
    </el-form>

  </el-card>
</template>
<script setup lang="ts">
import {login, register} from '../../api';
import {reactive, ref} from 'vue';
import {ElMessage} from "element-plus";
import router from "../../router";


const formType=ref(true); // true 登录 false 注册
const loginForm=reactive({
  username:'',
  password:'',
  email:'',
  display_name:''
})
const loginFormRef=ref();
const rules={
  username:[
    {required:true,message:'请输入用户名!',trigger:'blur'},
    { min: 3, max: 20, message: '用户名长度为3-20个字符', trigger: 'blur' }
  ],
  password:[
    {required:true,message:'请输入密码!',trigger:'blur'},
    { min: 6, max: 30, message: '密码长度为6-30个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
  ],
  displayName: [
    { required: true, message: '请输入姓名', trigger: 'blur' },
    { min: 2, max: 10, message: '姓名长度为2-10个字符', trigger: 'blur' }
  ]
}

const handleChange=()=>{
  formType.value=!formType.value
}
const handleSubmit=()=>{
  if(formType.value){
    loginFormRef.value.validate((valid)=>{
      if(!valid){
        ElMessage.warning('请填写正确的登录信息')
        return
      }
    })
    login(loginForm).then(data=>{
      localStorage.setItem('access_token',data.access_token)
      router.push('/').then(() => {
        ElMessage.success('登录成功')
      })
    })
  }
  else{
    register(loginForm).then(data=>{
      console.log('注册成功',data)
      ElMessage.success('注册成功，请登录')
      formType.value=true
      loginForm.email = '';
      loginForm.display_name = '';
    })
  }

}
</script>


<style scoped>

</style>