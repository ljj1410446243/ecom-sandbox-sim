<template>
  <div class="common-layout">
    <el-container>
      <Aside/>
      <el-container>
        <el-header><Header/></el-header>
        <el-main>Main</el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import Aside from '../components/Aside.vue';
import Header from '../components/NavHeader.vue';
</script>

<style lang="less" scoped>
.common-layout{
  height: 100%;
  .el-container{
    height: 100%;
  }
}
</style>