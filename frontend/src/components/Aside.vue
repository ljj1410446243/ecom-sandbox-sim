<template>
      <el-menu
        active-text-color="#ffd04b"
        background-color="#545c64"
        class="el-menu-vertical-demo"
        :default-active="activeIndex"
        router
        text-color="#fff"
        :key="menuKey"
        @open="handleOpen"
        @close="handleClose"
      >
        <p>电商沙盘</p>
        <template v-for="menu in menuStore.menus" :key="menu.index">
          <!--有子菜单-->
          <el-sub-menu v-if="menu.children" :index="menu.index">
            <template #title>
              <el-icon>
                <component :is="menu.icon"></component>
              </el-icon>
              <span>{{menu.title}}</span>
            </template>
            <el-menu-item
              v-for="child in menu.children"
              :key="child.index"
              :index="child.path"
              :route="child.path"
            >
              {{child.title}}
            </el-menu-item>
          </el-sub-menu>

          <!--无子菜单-->
          <el-menu-item
            v-else
            :index="menu.path"
            :route="menu.path"
          >
            <el-icon>
              <component :is="menu.icon"></component>
            </el-icon>
            <span>{{menu.title}}</span>

          </el-menu-item>

        </template>
      </el-menu>

</template>
<script setup lang="ts">
import {useMenuStore} from "../store/menuStore.ts";
import {useRoute} from "vue-router";
import {computed, ref, watch} from "vue";

const route=useRoute()
const menuStore=useMenuStore()
const menuKey = ref(0) // 用于强制重新渲染的 key


// 使用计算属性获取当前激活的菜单项
const activeIndex = computed(() => {
  console.log('当前路由路径:', route.path)
  console.log('当前路由参数:', route.params)
  return route.path
});

const handleOpen = () => {

};
const handleClose = () => {

};
</script>
<style lang="less" scoped>

</style>