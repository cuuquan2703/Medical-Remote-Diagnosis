import { useRef, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export default function CameraApp() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [photoDataUrl, setPhotoDataUrl] = useState(null);
  const [streaming, setStreaming] = useState(false);
  const navigate = useNavigate()
  useEffect(() => {
    navigator.mediaDevices.getUserMedia({ video: true })
      .then((stream) => {
        videoRef.current.srcObject = stream;
        setStreaming(true);
      })
      .catch((error) => console.error('Lỗi truy cập camera: ', error));
  }, []);
  const video = videoRef.current;

  const captureImage = () => {
    
    const canvas = canvasRef.current;
    const context = canvas.getContext('2d');

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataUrl = canvas.toDataURL('image/jpeg');
    setPhotoDataUrl(dataUrl);
    
    
  }

  const sendImage= () =>{
    video.srcObject.getVideoTracks().forEach(track => track.stop());

    navigate(`/register?photo=${encodeURIComponent(photoDataUrl)}`);
  }

  return (
    <div>
      <h1>Ứng dụng Camera </h1>
      <div>
        <video
          ref={videoRef}
          autoPlay
          width="640"
          height="480"
        />
      </div>
      {streaming && (
        <div>
          <canvas
            ref={canvasRef}
            style={{ display: 'none' }}
          />
          {photoDataUrl && (
            <img
              src={photoDataUrl}
              alt="Ảnh chụp"
              width="320"
            />
          )}
          <div>
            <button onClick={captureImage}>Chụp ảnh</button>
            <button onClick={sendImage}>Submit</button>
          </div>
        </div>
      )}
    </div>
  );
}