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

//创建商品
export const createProduct=(data:object)=>{
    return request.post('/products',data)
}

//删除商品
export const deleteProduct=(id:string)=>{
    return request.delete(`/products/${id}`)
}

//获取所有商品
export const getProducts=()=>{
    return request.get('/products')
}

//按照ID获取商品信息
export const getProductInfoById=(id:string)=>{
    return request.get(`/products/${id}`)
}

//更新商品
export const updateProduct=(id:string,data:object)=>{
    return request.patch(`/products/${id}`,data)
}

//上架商品
export const putProductOnSale=(data:object)=>{
    return request.post(`/listings`,data)
}

//按ID查询上架商品
export const getProductOnSaleById=(id:string)=>{
    return request.get(`/listings/${id}`)
}

//更新上架商品
export const updateProductOnSale=(id:string,data:object)=>{
    return request.patch(`/listings/${id}`,data)
}

//删除上架商品
export const deleteProductOnSale=(id:string)=>{
    return request.delete(`/listings/${id}`)
}