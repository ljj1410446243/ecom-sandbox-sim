import request from "../utils/request.ts"

//登录
export const login=(data:object)=>{
    return request.post('/auth/login',data)
}

//注册
export const register=(data:object)=>{
    return request.post('/auth/register',data)
}

//获取当前用户信息
export const getUserInfo=()=>{
    return request.get('/auth/me')
}