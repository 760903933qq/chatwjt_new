<template>
  <el-row justify="center" style="margin: 20px">
    <el-col :span="20">
      <el-card class="box-card">
        <template #header>
          <div class="card-header">
            <span>忘记密码</span>
          </div>
        </template>
        <el-form :model="form" label-width="100px" :rules="rules" label-position="top">
          <el-form-item label="电子邮箱" prop="email">
            <el-input v-model="form.email" />
          </el-form-item>
          <el-form-item label="密码" prop="password1">
            <el-input v-model="form.password1" type="password" show-password />
          </el-form-item>
          <el-form-item label="确认密码" prop="password2">
            <el-input v-model="form.password2" type="password" show-password />
          </el-form-item>
          <el-form-item label="验证码" prop="captcha">
            <el-row :gutter="20">
              <el-col :span="21">
                <el-input v-model="form.captcha" />
              </el-col>
              <el-col :span="3">
                <el-button @click="captcha">获取验证码</el-button>
              </el-col>
            </el-row>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="forget">修改密码</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </el-col>
  </el-row>
</template>

<script setup>
import { reactive } from 'vue'
import { forgetAPI } from '@/apis/user'
import { captchaAPI } from '@/apis/user'
// import { useRouter } from 'vue-router'

// 表单验证
const form = reactive({
  email: '',
  password1: '',
  password2: '',
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
  captcha: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { min: 4, max: 4, message: '验证码长度为4个字符', trigger: ['blur', 'change'] }
  ]
})

const forget = async () => {
  await forgetAPI(form)
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
