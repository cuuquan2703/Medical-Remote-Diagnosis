import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import {BrowserRouter, Route, Routes} from 'react-router-dom'
import Login from './components/login.jsx'
import SignUp from './components/Signup/SignUp.jsx';
import LoginByFace from './components/LoginByFace.jsx'
import FaceSignUp from './components/Face/Face_SignUp.jsx';


ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
    <Routes>
      <Route path='/' element={<App/>} >

      </Route>
      <Route path='/login' element={<Login/>}/>
      <Route exact path="/register" element={<SignUp />} /> 
      <Route exact path="/face_register" element={<FaceSignUp />} />

      <Route path='/loginByFace' element={<LoginByFace/>}/>
    </Routes>
    </BrowserRouter>
  </React.StrictMode>,
)
