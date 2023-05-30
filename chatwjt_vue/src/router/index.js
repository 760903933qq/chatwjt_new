import { createRouter, createWebHistory } from 'vue-router'
import Index from '@/views/Index/IndexIndex.vue'
import ForgetPassword from '@/views/ForgetPassword/ForgetPasswordIndex.vue'
import Login from '@/views/Login/LoginIndex.vue'
import Register from '@/views/Register/RegisterIndex.vue'
import Home from '@/views/Home/HomeIndex.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index
    },
    {
      path: '/user',
      name: 'user',
      children: [
        {
          path: '',
          name: 'home',
          component: Home
        },
        {
          path: 'login',
          name: 'login',
          component: Login
        },
        {
          path: 'register',
          name: 'register',
          component: Register
        },
        {
          path: 'forgetPassword',
          name: 'forgetPassword',
          component: ForgetPassword
        }
      ]
    }
  ]
})

export default router
