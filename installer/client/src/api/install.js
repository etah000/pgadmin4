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
    data: params,
    timeout:  30*24*60*60*1000 //30day
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
    data: params,
    timeout:  1*60*1000 //1m
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
export function processer(params) {
  return request({
    url: '/install/processer',
    method: 'post',
    data: params,
    timeout:  3*1000 //3s
  })
}
export function getAllPreferences() {
  return request({
    url: '/preferences/get_all',
    method: 'get'
  })
}
