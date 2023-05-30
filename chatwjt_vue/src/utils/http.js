// axios基础的封装
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/userInfo'
import axios from 'axios'
const httpInstance = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
  timeout: 5000
})

// 拦截器

// axios请求拦截器
httpInstance.interceptors.request.use(
  (config) => {
    // 1. 从pinia获取token数据
    const userStore = useUserStore()
    // 2. 按照后端的要求拼接token数据
    const token = userStore.userInfo.token
    if (token) {
      config.headers.Authorization = `Token ${token}`
    }
    return config
  },
  (e) => Promise.reject(e)
)

// axios响应式拦截器
httpInstance.interceptors.response.use(
  (res) => {
    if (res.data.code === 200) {
      return res.data
    } else {
      // 统一错误提示
      ElMessage({
        type: 'error',
        message: res.data.msg,
        duration: 2000,
        center: true,
        showClose: true
      })
      return res.data
    }
  },
  (e) => {
    // 统一错误提示
    ElMessage({
      type: 'error',
      message: e.response.data.message,
      duration: 2000,
      center: true,
      showClose: true
    })
  }
)

export default httpInstance
