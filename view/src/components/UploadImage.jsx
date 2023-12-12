import  { useState, useEffect } from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';





// TODO remove, this demo shouldn't need to reset the theme.

const defaultTheme = createTheme();

export default function SignUp() {
  const [message, setMessage] = useState({});
  const [file, setFile] = useState(null);
  const [selectedImage, setSelectedImage] = useState(null);


  const handleSubmit = async (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const newData = {
      email: data.get('email'),
      image: selectedImage
    };

    try {
      console.log(JSON.stringify(newData))
      const response = await fetch('http://127.0.0.1:5000/img/upload', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newData), // Use newData here instead of dataForm
      });
      const dataFromServer = await response.json();
      console.log(dataFromServer);
      setMessage(dataFromServer);
    } catch (error) {
      console.error('Error:', error);
    }
  };


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
            Upload image
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
              <Grid>
                <form method="post" action="/" encType="multipart/form-data">
                  <dl>
                    <p>
                      <input type="file" name="file" className="form-control" autoComplete="off" onChange={handleImageChange} required />
                    </p>
                  </dl>
                  {selectedImage && <img src={selectedImage} alt="Selected" />}

                </form>
                <img src="{{ url_for('static', filename= 'uploads/' + filename) }}" alt="" />
              </Grid>

            </Grid>
            <div><h3 style={{ color: 'red' }}>{message['message']}</h3></div>
            <div><h3 style={{ color: 'red' }}>{message['disease']}</h3></div>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Submit
            </Button>
            <Grid container justifyContent="flex-end">
            </Grid>
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
}
