import { useCallback, useRef} from "react"
import { Button } from "react-bootstrap";
import Webcam from "react-webcam";

// eslint-disable-next-line react/prop-types
const Camera = ({imgSrc,setImgSrc}) => {
    // eslint-disable-next-line react/prop-types
    // console.log(props)
    const webcamRef = useRef(null)
    // const [imgSrc, setImgSrc] = useState(null)
    const capture = useCallback(()=>{
        const imageSrc = webcamRef.current.getScreenshot();
        setImgSrc(imageSrc)
    },[webcamRef, setImgSrc])
    const recap = () => {
        setImgSrc(null)
    }
    return (
        <>
            {imgSrc == null ? <Webcam 
                audio={false}
                ref={webcamRef}
                screenshotFormat="image/jpeg"
            /> : <img src={imgSrc}/>}
            {imgSrc == null ? <Button variant="outline-primary" onClick={capture}>Capture</Button> :
                        <Button variant="outline-primary" onClick={recap}>Capture new image</Button>
            }
            

        </>
    )
}

export default Camera