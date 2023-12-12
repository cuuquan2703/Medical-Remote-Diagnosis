from deepface import DeepFace
class Deepface():
    def __init__(self, model="Facenet512"):
        self.model_name = model
        
    def build__model(self):
        ... 
    def extract_feature(self,img):
        ...
    def verify(self,img1,img2,compute_distance='cosine',backend_detector="retinaface"):
        result = DeepFace.verify(img1,img2,model_name=self.model_name, distance_metric=compute_distance,detector_backend=backend_detector)
        return (result['verified'],result['distance'])
    def detect_face(self,img,backend_detector="retinaface"):
        facecial_area = []
        try:
            result = DeepFace.extract_faces(img,detector_backend=backend_detector)
            for face in result:
                facecial_area.append(face['facial_area'])
            return (True, facecial_area)
        except:
            return (False, [])
    def represent(self,img,backend_detector="retinaface"):
        result = DeepFace.represent(img,model_name=self.model_name,detector_backend=backend_detector)
        return result