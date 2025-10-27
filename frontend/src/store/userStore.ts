import {defineStore} from "pinia";
import {reactive} from 'vue'
import {getUserInfo} from "../api";

export const useUserStore=defineStore('user',()=>{
    //state
    const userInfo=reactive({
        username:'',
        status:'',
        id:'',
        display_name:'',
        email:'',
        role:''
    })

    return {userInfo}
},{
    persist:true
})