import request from "../utils/request.ts"

//登录
export const login=(data:object)=>{
    return request.post('/auth/login',data)
}

//获取当前用户信息
export const getUserInfo=()=>{
    return request.get('/auth/me')
}