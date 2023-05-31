<template>
  <el-row justify="center" style="margin: 20px">
    <el-col :span="20">
      <el-card class="box-card">
        <template #header>
          <div class="card-header">
            <span>登陆</span>
          </div>
        </template>
        <el-form :model="form" label-width="100px" :rules="rules" label-position="top">
          <el-form-item label="用户名" prop="username">
            <el-input v-model="form.username" />
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input v-model="form.password" type="password" show-password />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="onSubmit">登陆</el-button>
            <el-button @click="handleClick">忘记密码</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </el-col>
  </el-row>
</template>

<script lang="ts" setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userInfo'

// 表单验证
const form = reactive({
  username: '',
  password: ''
})

const rules = reactive({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 20, message: '用户名请控制在2-20字符之间', trigger: ['blur', 'change'] }
  ],

  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6 到 32 个字符', trigger: ['blur', 'change'] }
  ]
})

const userStore = useUserStore()
const router = useRouter()
const onSubmit = async () => {
  const res = await userStore.getUserInfo(form)
  if (res === 200) {
    router.push('/')
  }
}

const handleClick = () => {
  router.push('/user/forgetPassword')
}
</script>

<style>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
}
</style>
