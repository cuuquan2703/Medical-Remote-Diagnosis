from ..models.user_model import UserModel,db
import hashlib
from ..config import STATIC, HASHING_METHOD, SECRET_KEY
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
import os
import cv2
import face_recognition
from .vision_service import Deepface
import jwt
from functools import wraps
faceService = Deepface()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing'})
        data = jwt.decode(token,SECRET_KEY)

        return f(data,*args,**kwargs)

    return decorated



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

    def login(self,username,password):

        exist_user = self.find_user(username)
        if len(exist_user) == 0:
            return {"success": False, "message": "Incorrect username"}, 401

        print(HASHING_METHOD)
        hash_password = "$".join([method,salt,password_in_db])

        check = password
        print(hash_password)
        if check_password_hash(hash_password,check):
            token = jwt.encode({'id':exist_user[0].})
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
        exist_user = self.find_user(username)
        if len(exist_user) > 0:
            return {"success": False, "message": "User exist"}, 401
        try:
            file_name = secure_filename(f"{username}.jpeg")
            upload_folder = os.path.join(os.getcwd(),STATIC,"uploads")
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            img.save(os.path.join(upload_folder,file_name))

            (new_password,_salt,algo) = self.create_hashing_password(password)['part']
            new_user = self.auth_model(username=username, salt=_salt,password=new_password)

            db.session.add(new_user)
            db.session.commit()
            return {"success": True, "message": "Successfully Register"},201
        except:
            return {"success": False, "message": "Something went wrong"}, 500
    
    def find_user(self,username):
        return self.auth_model.query.filter_by(username=username).all()

    def login_by_face(self,username,img):
        file_name = secure_filename(f"{username}_login.jpeg")
        upload_folder = os.path.join(os.getcwd(),STATIC,"uploads")
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        img.save(os.path.join(upload_folder,file_name))

        status, faces = faceService.detect_face(os.path.join(upload_folder,file_name))
        if status == False:
            return 0
        else:
            login_img = os.path.join(upload_folder,file_name)
            user_img = os.path.join(upload_folder,f"{username}.jpeg")
            thresh_hold = {
                "cosine":0.25,
                "euclidean": 13,
                "euclidean_l2": 0.6
            }

            compute_distance = "euclidean_l2"
            verify = faceService.verify(login_img,user_img,compute_distance=compute_distance)
            if (verify[1] <= thresh_hold[compute_distance]):
                return 1
            else:
                return -1


    # def login_by_face(self,username,img):
    #     file_name = secure_filename(f"{username}_login.jpeg")
    #     upload_folder = os.path.join(os.getcwd(),STATIC,"uploads")
    #     if not os.path.exists(upload_folder):
    #         os.makedirs(upload_folder)
    #     img.save(os.path.join(upload_folder,file_name))

    #     login_img = cv2.imread(os.path.join(upload_folder,file_name))
    #     gray_img = cv2.cvtColor(login_img, cv2.COLOR_BGR2GRAY)
    #     print(os.path.join(os.getcwd(),"haarcascade_frontalface_default.xml"))
    #     face_cascade = cv2.CascadeClassifier(os.path.join(os.getcwd(),"haarcascade_frontalface_default.xml"))
    #     faces = face_cascade.detectMultiScale(gray_img, scaleFactor=1.05, minNeighbors=3, minSize=(0, 0))

        
    #     if len(faces)>0:
    #         print(file_name,f"{username}.jpeg" )
    #         login_img = face_recognition.load_image_file(os.path.join(upload_folder,file_name))
    #         login_img_encoding = face_recognition.face_encodings(login_img)

    #         _user_img = os.path.join(upload_folder,f"{username}.jpeg")
    #         user_img = face_recognition.load_image_file(_user_img)

    #         user_img_encoding = face_recognition.face_encodings(user_img)

    #         if len(login_img_encoding)>0 and len(user_img_encoding)>0:
    #             matches = face_recognition.compare_faces(user_img_encoding,login_img_encoding[0])
    #             print(matches)
    #             return matches,len(faces)
    #     return [False],0