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

//删除店铺
export const deleteShop=(id:string)=>{
    return request.delete(`/shops/${id}`)
}

//修改店铺信息
export const updateShop=(id:string,data:object)=>{
    return request.patch(`/shops/${id}`,data)
}