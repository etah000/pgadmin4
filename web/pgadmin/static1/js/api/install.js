import request from './request'

// 获取列表数据
export function getInstallConf() {
  return request({
    url: '/install/getInstallConf',
    method: 'get'
  })
}
export function setInstallConf(params) {
  return request({
    url: '/install/setInstallConf',
    method: 'post',
    data: params
  })
}
export function validateConf(params) {
  return request({
    url: '/install/validateConf',
    method: 'post',
    data: params
  })
}
export function validateHost(params) {
  return request({
    url: '/install/validateHost',
    method: 'post',
    data: params
  })
}
export function merge(params) {
  return request({
    url: '/install/merge',
    method: 'post',
    data: params
  })
}
export function list() {
  return request({
    url: '/install/list',
    method: 'post'
  })
}
export function processer() {
  return request({
    url: '/install/processer',
    method: 'post'
  })
}
export function getAllPreferences() {
  return request({
    url: '/preferences/get_all',
    method: 'get'
  })
}
