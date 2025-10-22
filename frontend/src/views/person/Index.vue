<template>
  <el-descriptions title="个人信息" border>
      <el-descriptions-item
        :rowspan="2"
        :width="140"
        label="Photo"
        align="center"
      >
        <el-image
          style="width: 100px; height: 100px"
          src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"
        />
      </el-descriptions-item>
      <el-descriptions-item label="用户名">{{ userInfo.username }}</el-descriptions-item>
      <el-descriptions-item label="邮箱">{{ userInfo.email }}</el-descriptions-item>
      <el-descriptions-item label="姓名">{{ userInfo.display_name }}</el-descriptions-item>
      <el-descriptions-item label="角色">{{userInfo.role}}</el-descriptions-item>

    </el-descriptions>
  <el-button @click="router.back()">返回</el-button>

</template>
<script setup lang="ts">
import {useUserStore} from "../../store/userStore.ts";
import router from "../../router";

const userStore=useUserStore()
const userInfo=userStore.userInfo

</script>

<style scoped>

</style>