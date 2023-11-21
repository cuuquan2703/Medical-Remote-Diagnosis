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
            const response = await fetch(`${url}/register`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify(formData),
            });
            return await response.json();

          } catch (error) {
            console.error('Error:', error);
            throw error;
          }
        
    }
}

export default userApi;