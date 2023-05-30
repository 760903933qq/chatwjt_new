import httpInstance from '@/utils/http'

export function rightAPI() {
  return httpInstance({
    url: 'chat/right'
  })
}
