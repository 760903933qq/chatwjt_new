<template>
  <el-menu
    :default-active="activeIndex"
    class="el-menu-demo"
    mode="horizontal"
    :ellipsis="false"
    :router="true"
  >
    <el-menu-item index="0" class="Logo" route="/">ChatWjt</el-menu-item>
    <div class="flex-grow" />
    <el-sub-menu index="1" :hide-timeout="200">
      <template #title>个人中心</template>
      <template v-if="isLoggedIn">
        <el-menu-item index="1-1" route="/user">{{ username }}</el-menu-item>
        <el-menu-item index="1-2" @click="logout" route="/user/login">退出登录</el-menu-item>
      </template>
      <template v-else>
        <el-menu-item index="1-3" route="/user/login">登录</el-menu-item>
        <el-menu-item index="1-4" route="/user/register">注册</el-menu-item>
      </template>
    </el-sub-menu>
  </el-menu>
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue'
import { useUserStore } from '@/stores/userInfo'

const activeIndex = ref('0')
// 判断登陆状态
const userStore = useUserStore()
const isLoggedIn = ref(userStore.userInfo.token ? true : false)
const username = ref(userStore.userInfo.username)

watch(
  () => userStore.userInfo,
  (newUserInfo) => {
    if (!newUserInfo) return
    isLoggedIn.value = newUserInfo.token ? true : false
    username.value = newUserInfo.username
  }
)
const logout = () => {
  userStore.logout()
  isLoggedIn.value = false
}
</script>

<style>
.flex-grow {
  flex-grow: 1;
}

.Logo {
  font-size: 20px;
  font-weight: bold;
}
</style>
