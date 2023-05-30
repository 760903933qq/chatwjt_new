<template>
  <el-descriptions
    title="个人中心"
    direction="horizontal"
    :column="1"
    size="large"
    border
    style="margin: 20px"
  >
    <el-descriptions-item label="昵称">{{ form.username }}</el-descriptions-item>
    <el-descriptions-item label="邀请码">{{ form.invite_code }}</el-descriptions-item>
    <el-descriptions-item label="邀请人数">{{ form.invite_number }}</el-descriptions-item>
  </el-descriptions>
</template>

<script setup lang="ts">
import { homeAPI } from '@/apis/user'
import { ref } from 'vue'

const form = ref({
  username: '',
  invite_code: '',
  invite_number: ''
})

const home = async () => {
  const res = await homeAPI()
  form.value = res.data
}
home()
</script>

<style scoped></style>
