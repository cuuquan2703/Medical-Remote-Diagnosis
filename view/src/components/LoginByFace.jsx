import { useState } from "react"
import Camera from "./Camera"
import { Button, Form } from "react-bootstrap"
import toBlob from "./utils"
import userApi from "../api/user"


const LoginByFace = ()=> {
    const [formData,setFormData] = useState({
        img: new Blob()
    })
    const [mess,setMess] = useState(<div></div>)
    const [imgSrc,setImgSrc] = useState(null)
    const _onSubmit = async (e) => {
        e.preventDefault();
        const form = e.target
        // console.log(form)
        const username = form.username.value
        const blob = toBlob(imgSrc)
    
        let formdata = new FormData()
        formdata.append('username', username)
        formdata.append('img',blob)
        // console.log(blob)
      //   for (var pair of formdata.entries()) {
      //     console.log(pair[0]+ ', ' + pair[1]); 
      // }
        const res = await userApi.loginByFace(formdata)
        console.log(res)
        setMess(<div>{res?.message}</div>)
      }

      
  const _onChange = (e) =>{
    e.preventDefault();
    if (e.target.attributes[0].value == 'username') {
      setFormData({...formData,username:e.target.value})
    }
  }
    
    return (
        <>
            <Form encType="multipart/form-data" onSubmit={_onSubmit}>
            <Form.Group className="mb-3" controlId="formGroupUsername">
            <Form.Label>Username</Form.Label>
            <Form.Control controlid='username' name='username' type="text" placeholder="Username" onChange={_onChange} />
            {mess}
            </Form.Group>
                <Camera imgSrc={imgSrc} setImgSrc={setImgSrc} />
                <Button variant="primary" type="submit">Login</Button>
            </Form>

        </>
    )
}

export default LoginByFace