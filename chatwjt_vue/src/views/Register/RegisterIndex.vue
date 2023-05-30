<template>
  <el-row justify="center" style="margin: 20px">
    <el-col :span="20">
      <el-card class="box-card">
        <template #header>
          <div class="card-header">
            <span>注册</span>
          </div>
        </template>
        <el-form :model="form" label-width="100px" :rules="rules" label-position="top">
          <el-form-item label="用户名" prop="username">
            <el-input v-model="form.username" />
          </el-form-item>
          <el-form-item label="电子邮箱" prop="email">
            <el-input v-model="form.email" />
          </el-form-item>
          <el-form-item label="密码" prop="password1">
            <el-input v-model="form.password1" type="password" show-password />
          </el-form-item>
          <el-form-item label="确认密码" prop="password2">
            <el-input v-model="form.password2" type="password" show-password />
          </el-form-item>
          <el-form-item label="邀请码(可不填)" prop="invitation">
            <el-input v-model="form.invitation" />
          </el-form-item>
          <el-form-item label="验证码" prop="captcha">
            <el-row :gutter="20">
              <el-col :span="12">
                <el-input v-model="form.captcha" />
              </el-col>
              <el-col :span="3">
                <el-button @click="captcha">获取验证码</el-button>
              </el-col>
            </el-row>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="register">注册</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </el-col>
  </el-row>
</template>

<script setup>
import { reactive } from 'vue'
import { registerAPI } from '@/apis/user'
import { captchaAPI } from '@/apis/user'
import { useRouter } from 'vue-router'

// 表单验证
const form = reactive({
  username: '',
  email: '',
  password1: '',
  password2: '',
  invitation: '',
  captcha: ''
})

const validateConfirmPassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== form.password1) {
    callback(new Error('两次输入密码不一致!'))
  } else {
    callback()
  }
}
const rules = reactive({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 20, message: '用户名请控制在2-20字符之间', trigger: ['blur', 'change'] }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: ['blur'] }
  ],
  password1: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 32, message: '密码长度在 6 到 32 个字符', trigger: ['blur', 'change'] }
  ],
  password2: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: ['blur'] }
  ],
  invitation: [{ required: false, message: '', trigger: 'blur' }],
  captcha: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { min: 4, max: 4, message: '验证码长度为4个字符', trigger: ['blur', 'change'] }
  ]
})

const router = useRouter()
const register = async () => {
  await registerAPI(form)
  router.push('/user/login')
}

const captcha = () => {
  const email = form.email

  const res = captchaAPI(email)
  console.log(res)
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
