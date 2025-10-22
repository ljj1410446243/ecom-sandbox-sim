import request from "../utils/request.ts"

//登录
export const login=(data:object)=>{
    return request.post('/auth/login',data)
}

//获取当前用户信息
export const getUserInfo=()=>{
    return request.get('/auth/me')
}

//创建店铺
export const createShop=(data:object)=>{
    return request.post('/shops',data)
}

//查询我的店铺信息
export const getMyShopInfo=()=>{
    return request.get('/shops/mine')
}

//按ID查询店铺
export const getShopInfoById=(id:string)=>{
    return request.get(`/shops/${id}`)
}