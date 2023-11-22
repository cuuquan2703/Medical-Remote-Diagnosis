import { useState } from 'react';
import { Button } from 'react-bootstrap';
import Form from 'react-bootstrap/Form';
import userApi from '../api/user';

const Login = () => {
  const [formData,setFormData] = useState({
    username:"",
    password:"",
  })

  const [mess, setMess] = useState(<div></div>)
  const _onSubmit = async (e) => {
    e.preventDefault();
    const form = e.target

    const username = form.username.value
    const password = form.password.value

    let formdata = new FormData()
    formdata.append('username',username)
    formdata.append('password',password)

  //   for (var pair of formdata.entries()) {
  //     console.log(pair[0]+ ', ' + pair[1]); 
  // }
    const res = await userApi.login(formdata)
    console.log(res)
    setMess(<div>{res?.message}</div>)
  }


  const _onChange = (e) =>{
    e.preventDefault();
    if (e.target.attributes[0].value == 'username') {
      setFormData({...formData,username:e.target.value})
    }
    if (e.target.attributes[0].value == 'password') {
      setFormData({...formData,password:e.target.value})
    }
    // console.log(formData)
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
    {mess}
    <>
      <Button variant="primary" type="submit">Login</Button>
    </>
  </Form>
</>

)
}

export default Login