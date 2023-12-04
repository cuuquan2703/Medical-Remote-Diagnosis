from ..models.user_model import UserModel
import hashlib
from ..config import STATIC, HASHING_METHOD
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
import os
import cv2
import face_recognition
class AuthService():
    def __init__(self,auth_model) -> None:
        self.auth_model = auth_model
        pass

    def check_password(self,password,salt,password_in_db,method = HASHING_METHOD):
        print(HASHING_METHOD)
        hash_password = "$".join([method,salt,password_in_db])

        check = password
        print(hash_password)
        if check_password_hash(hash_password,check):
            return True
        else:
            return False
        
    def find_user(self, username):
        exist_user = self.auth_model.query.filter_by(username=username).all()
        return exist_user
    
    def create_new_user(self,username,password):
        hash_password = generate_password_hash(password,method=HASHING_METHOD).split("$")
        algo = hash_password[0]
        _salt = hash_password[1]
        new_password = hash_password[2]
        return self.auth_model(username=username, salt=_salt,password=new_password)

    def create_hashing_password(self,password, method=HASHING_METHOD):
        hash_password = generate_password_hash(password,method)
        hash_password = hash_password.split("$")
        algo = hash_password[0]
        salt = hash_password[1]
        new_password = hash_password[2]
        return{
            'full_hash_password': hash_password,
            'part': (new_password,salt,algo)
        }
    
    def register(self,username,password,img):
        file_name = secure_filename(f"{username}.jpeg")
        upload_folder = os.path.join(os.getcwd(),STATIC,"uploads")
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        img.save(os.path.join(upload_folder,file_name))

        (new_password,_salt,algo) = self.create_hashing_password(password)['part']
        new_user = self.auth_model(username=username, salt=_salt,password=new_password)
        return new_user
    
    def find_user(self,username):
        return self.auth_model.query.filter_by(username=username).all()

    def login_by_face(self,username,img):
        file_name = secure_filename(f"{username}_login.jpeg")
        upload_folder = os.path.join(os.getcwd(),STATIC,"uploads")
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        img.save(os.path.join(upload_folder,file_name))

        login_img = cv2.imread(os.path.join(upload_folder,file_name))
        gray_img = cv2.cvtColor(login_img, cv2.COLOR_BGR2GRAY)
        print(os.path.join(os.getcwd(),"haarcascade_frontalface_default.xml"))
        face_cascade = cv2.CascadeClassifier(os.path.join(os.getcwd(),"haarcascade_frontalface_default.xml"))
        faces = face_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces)==0:
            return {"success":False,"message":"No face in camera"}, 401
        
        login_img = face_recognition.load_image_file(os.path.join(upload_folder,file_name))
        login_img_encoding = face_recognition.face_encodings(login_img)

        _user_img = os.path.join(upload_folder,f"{username}.jpeg")
        user_img = face_recognition.load_image_file(_user_img)

        user_img_encoding = face_recognition.face_encodings(user_img)

        if len(login_img_encoding)>0 and len(user_img_encoding)>0:
            matches = face_recognition.compare_faces(user_img_encoding,login_img_encoding[0])
            return matches