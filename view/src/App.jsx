import { Link } from 'react-router-dom';
import './App.css'
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {

  return (
    <>
    <Link to="login">Login</Link><br/>
    <Link to="register">Register</Link><br/>
    <Link to="loginByFace">Login By Face</Link><br/>
    </>
  )
}

export default App
