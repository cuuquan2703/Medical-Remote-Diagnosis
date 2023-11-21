import './App.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import Button from '@mui/material/Button';
import { useNavigate } from 'react-router-dom';
function App() {

  const navigate = useNavigate()
  const signin = () =>{
      navigate("/login")
  }
  const signup = () =>{
      navigate("/register")
  }
  const face_signin = () =>{
      navigate("/loginByFace")
  }
  return(
      <div>
          <div>
              <Button type="submit"
              onClick={signin}
            variant="contained"
            sx={{ mt: 3, mb: 2 }}>Đăng nhập</Button>
          </div>
          <div>
              <Button type="submit"
            onClick={signup}
            variant="contained"
            sx={{ mt: 3, mb: 2 }}>Đăng Ký</Button>
          </div>
          <div>
              <Button type="submit"
              onClick={face_signin}
            variant="contained"
            sx={{ mt: 3, mb: 2 }}>Đăng nhập bẳng khuôn mặt</Button>
          </div>
      </div>
  )
}

export default App
