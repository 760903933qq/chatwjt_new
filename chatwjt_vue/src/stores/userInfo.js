import { defineStore } from 'pinia'
import { ref } from 'vue'
import { loginAPI } from '@/apis/user'

export const useUserStore = defineStore(
  'user',
  () => {
    // 1. 定义管理用户数据的state
    const userInfo = ref({
      token: '',
      username: '',
      id: ''
    })
    // 2. 定义获取接口数据的action函数
    const getUserInfo = async (data) => {
      const res = await loginAPI(data)
      userInfo.value = res.data
    }
    // 3. logout用户退出登录
    const logout = () => {
      userInfo.value = {
        token: '',
        username: ''
      }
    }

    // 3. 以对象的格式把state和action return
    return {
      userInfo,
      getUserInfo,
      logout
    }
  },
  {
    persist: true
  }
)
