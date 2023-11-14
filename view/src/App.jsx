import { Link } from 'react-router-dom';
import './App.css'
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {

  return (
    <>
    <Link to="login">Login</Link>
    <Link to="register">Register</Link>
    <Link to="loginByFace">Login By Face</Link>
    </>
  )
}

export default App
