import axios from "axios";
import {ElMessage} from "element-plus";

const http=axios.create({
    baseURL:'http://127.0.0.1:8000/api/v1',
    timeout:1000,
})

//请求拦截器
http.interceptors.request.use(config=>{
    console.log( config)
    const token=localStorage.getItem('access_token')
    const whiteUrl=['/auth/login','/auth/register']
    if(!whiteUrl.includes(config.url)){
        config.headers.Authorization=`Bearer ${token}`
    }
    return config
},err=>{
    console.error('请求拦截器错误:',err)
    return Promise.reject(err)
})

//响应拦截器
http.interceptors.response.use(res=>{
    console.log(res,'res')
    return res.data
},err=>{
    if(err.response.status===401){
        ElMessage.error('登录已过期，请重新登录')
        localStorage.removeItem('access_token')
        localStorage.removeItem('currentShop')
        window.location.reload()
    }
    return Promise.reject(err)
})

export default http