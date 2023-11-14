import { useState } from 'react';
import { Button } from 'react-bootstrap';
import Form from 'react-bootstrap/Form';
import userApi from '../api/user';
import Camera from './Camera';
import toBlob from './utils';

const Register = () => {
  const [formData,setFormData] = useState({
    username:"",
    password:"",
    img:new Blob()
  })

  const [imgSrc, setImgSrc] = useState(null)
  const _onSubmit = async (e) => {
    e.preventDefault();
    // console.log(formData)
    // const data = {...formData, img:toBlob(imgSrc)}
    // console.log("Data submit: ",data.img)
    // console.log("Blob: ",toBlob(data.img))

    const form = e.target
    // console.log(form)
    const username = form.username.value
    const password = form.password.value
    const blob = toBlob(imgSrc)

    let formdata = new FormData()

    formdata.append('username',username)
    formdata.append('password',password)
    formdata.append('img',blob)
    // console.log(blob)
  //   for (var pair of formdata.entries()) {
  //     console.log(pair[0]+ ', ' + pair[1]); 
  // }
    const res = await userApi.register(formdata)
    console.log(res)
  }

  const _onChange = (e) =>{
    e.preventDefault();
    if (e.target.attributes[0].value == 'username') {
      setFormData({...formData,username:e.target.value})
    }
    if (e.target.attributes[0].value == 'password') {
      setFormData({...formData,password:e.target.value})
    }

  }


    return (<>
        <Form encType='multipart/form-data' onSubmit={_onSubmit}>
        <Form.Group className="mb-3" controlId="formGroupUsername">
          <Form.Label>Username</Form.Label>
          <Form.Control controlid='username' name='username' type="text" placeholder="Username" onChange={_onChange} />
        </Form.Group>
        <Form.Group className="mb-3" controlId="formGroupPassword"> 
          <Form.Label>Password</Form.Label>
          <Form.Control controlid='password' name='password' type="password" placeholder="Password" onChange={_onChange}/>
        </Form.Group>
        <Form.Group className="mb-3" controlId="formGroupConfirmPassword">
          <Form.Label>Confirm Password</Form.Label>
          <Form.Control controlid='confirm' type="password" placeholder="Confirm Password" />
        </Form.Group>
        <>
          <Button variant="primary" type="submit">Register</Button>
        </>
        <Camera imgSrc={imgSrc} setImgSrc={setImgSrc}/>
      </Form>
    </>

    )
  }
  
  export default Register