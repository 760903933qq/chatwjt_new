import httpInstance from '@/utils/http'

export function registerAPI(data) {
  return httpInstance({
    url: 'user/register',
    method: 'post',
    data: data
  })
}

export function captchaAPI(email) {
  return httpInstance({
    url: 'user/register/captcha?email=' + email,
    method: 'get'
  })
}

export function loginAPI(data) {
  return httpInstance({
    url: 'user/login',
    method: 'post',
    data: data
  })
}

export function forgetAPI(data) {
  return httpInstance({
    url: 'user/forget',
    method: 'post',
    data: data
  })
}
export function homeAPI() {
  return httpInstance({
    url: 'user/home',
    method: 'get'
  })
}
