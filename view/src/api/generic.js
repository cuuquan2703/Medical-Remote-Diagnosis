import axios from 'axios';
import _config from "../../config"

const SERVER_PORT = _config.SERVER_PORT || 5000
const SERVER_URL = _config.SERVER_URL || `http://localhost:${SERVER_PORT}`
export const baseURI =  SERVER_URL

export const config = ()=>{
    return {
        headers: {
            'content-type': 'application/json'
        }
    }
}

export const fileConfig = () => {
    return {
        headers: {
            'content-type': 'multipart/form-data'
        }
    }
}

export const get = (url,config) => {
    return new Promise((resolve, reject) => {
        axios.get(url,config)
        .then((res)=>{
            return resolve({data:res})
        })
        .catch((err)=>{
            return reject(err)
        })
    })
}

export const post = (url,data,config) => {
    return new Promise((resolve, reject) => {
        axios.post(url,data,config)
        .then((res)=> {
            return resolve({data:res})
        })
        .catch((err)=>{
            return reject(err)
        })
    })
}