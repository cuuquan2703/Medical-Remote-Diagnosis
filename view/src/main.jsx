import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import {BrowserRouter, Route, Routes} from 'react-router-dom'
import Login from './components/login.jsx'
import Register from './components/register.jsx'
import LoginByFace from './components/LoginByFace.jsx'
import UploadImage from './components/UploadImage.jsx'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
    <Routes>
      <Route path='/' element={<App/>} >

      </Route>
      <Route path='/login' element={<Login/>}/>
      <Route path='/register' element={<Register/>}/>
      <Route path='/loginByFace' element={<LoginByFace/>}/>
      <Route path='/Upload' element={<UploadImage />}/>
    </Routes>
    </BrowserRouter>
  </React.StrictMode>,
)
