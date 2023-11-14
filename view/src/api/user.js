import { baseURI } from "./generic";

const url = `${baseURI}/auth`

const userApi = {
    login: async (formData)=>{
        try {
            return fetch(`${url}/login`,{
                method:'POST',
                body: formData,
                }).then(resolve=>{
                    return resolve.json()
                })
                .catch(err => {
                    console.log(err)
                })
            
        } catch (error) {
            console.log(error)
        }

   
    },
    loginByFace: (formData) => {
        try {
            return fetch(`${url}/loginByFace`,{
                method:'POST',
                body: formData,
                }).then(resolve=>{
                    return resolve.json()
                })
                .catch(err => {
                    console.log(err)
                })
        } catch (error) {
            console.log(error)
        }
    },
    register: async (formData)=>{
        try {
            return fetch(`${url}/register`,{
                method:'POST',
                body: formData,
                }).then(resolve=>{
                    return resolve.json()
                })
                .catch(err => {
                    console.log(err)
                })
        } catch (error) {
            console.log(error)
        }
    }
}

export default userApi;