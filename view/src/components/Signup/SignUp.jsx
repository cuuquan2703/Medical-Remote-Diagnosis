import { useState, useEffect } from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import {useNavigate, useLocation} from "react-router-dom"
import userApi from '../../api/user';



// TODO remove, this demo shouldn't need to reset the theme.

const defaultTheme = createTheme();

export default function SignUp() {
  const [dataForm, setData] = useState({});
  const [message, setMessage] = useState({});
  const [file, setFile] = useState(null);
  const [selectedImage, setSelectedImage] = useState(null);
  const navigate = useNavigate();
  const location = useLocation();
  const capturedImage  = new URLSearchParams(location.search).get('photo');
  useEffect(() => {
    if (capturedImage) {
      setSelectedImage(decodeURIComponent(capturedImage));
    }
  }, [capturedImage]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const newData = {
      email: data.get('email'),
      password: data.get('password'),
      image: selectedImage
    };
    setData(newData);
  
    
    const response = await userApi.register(newData)
    console.log(response)
    setMessage(response)
  };
  
  if (message['message'] === "Account created successfully")
  {

    navigate("/login")
  }

  

  const handleImageChange = (event) => {
    setFile(event.target.files[0]);
  };

  useEffect(() => {
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setSelectedImage(e.target.result);
      };
      reader.readAsDataURL(file);
    }
  }, [file]);

  const checkpass = (e) => {
    e.preventDefault();
    const password = dataForm.password;
    const confirmPass = dataForm.confirmpassword;
  
    if (password !== confirmPass) {
      setMessage("Mật khẩu và xác nhận mật khẩu không khớp");
    }
  };

  return (
    <ThemeProvider theme={defaultTheme}>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Sign up
          </Typography>
          <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
            <Grid container spacing={2}>
              
              <Grid item xs={12}>
                <TextField
                  required
                  fullWidth
                  id="email"
                  label="Email Address"
                  name="email"
                  autoComplete="email"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  required
                  fullWidth
                  name="password"
                  label="Password"
                  type="password"
                  id="password"
                  autoComplete="new-password"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  required
                  fullWidth
                  name="confirmpassword"
                  label="ComfirmPassword"
                  type="password"
                  id="confirmpassword"
                  autoComplete="new-password"
                  onChange={checkpass}
                />
              </Grid>
              <Grid>
                <h5>Ảnh mặt để đăng nhập</h5>
                <div>
                  <a href='/face_register'>Lấy ảnh bằng camera</a>
                </div>

                <h7>Hoặc upload ảnh</h7>
                <form method="post" action="/" encType="multipart/form-data">
                    <dl>
                        <p>
                            <input type="file" name="file" className="form-control" autoComplete="off" onChange={handleImageChange} required/>
                        </p>
                    </dl>
                    {selectedImage && <img src={selectedImage} alt="Selected" />}
                    
                </form>
                <img src="{{ url_for('static', filename= 'uploads/' + filename) }}" alt=""/>
              </Grid>
            
            </Grid>
            <div><h3 style={{ color: 'red' }}>{message['message']}</h3></div>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Sign Up
            </Button>
            <Grid container justifyContent="flex-end">
              <Grid item>
                <Link href="http://localhost:5173/login" variant="body2">
                  Already have an account? Sign in
                </Link>
              </Grid>
            </Grid>
          </Box>
        </Box>

      </Container>
    </ThemeProvider>
  );
}
