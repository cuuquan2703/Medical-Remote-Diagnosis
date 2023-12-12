import datetime
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

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None
#         if 'x-access-token' in request.headers:
#             token = request.headers['x-access-token']
#         if not token:
#             return jsonify({'message': 'Token is missing'})
#         data = jwt.decode(token,SECRET_KEY)

#         return f(data,*args,**kwargs)

#     return decorated



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

    def login(self,username,password,method=HASHING_METHOD):
        exist_user = self.find_user(username)
        if len(exist_user) == 0:
            return {"success": False, "message": "Incorrect username"}, 401

        exist_user = exist_user[0]
        salt = exist_user.salt
        password_in_db = exist_user.password
        print(HASHING_METHOD)
        hash_password = "$".join([method,salt,password_in_db])

        check = password
        print(hash_password)
        if check_password_hash(hash_password,check):
            token = jwt.encode({'id':exist_user.id,'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)},SECRET_KEY)
            return {"success": True, "token": token.decode('UTF-8')}, 401
        else:
            return {"success": False, "message": "Incorrect password"}, 401

        
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
        try:
            exist_user = self.find_user(username)
            if len(exist_user) > 0:
                return {"success": False, "message": "User exist"}, 401
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
        try:
            exist_user = self.find_user(username)
            if len(exist_user) == 0:
                return {"success": False, "message": "Incorrect username"}, 401
            
            user = exist_user[0]
            username = user.username

            file_name = secure_filename(f"{username}_login.jpeg")
            upload_folder = os.path.join(os.getcwd(),STATIC,"uploads")
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            img.save(os.path.join(upload_folder,file_name))


            status, faces = faceService.detect_face(os.path.join(upload_folder,file_name))
            if status == False:
                return {"success":False,"message":"There no face detected in Image"},401
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
                    token = jwt.encode({'id':user.id,'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)},SECRET_KEY)
                    return {"success": True,"token":token.decode('UTF-8')}
                else:
                    return {"success": False,"message":"Face not match"}
        except Exception as e:
            return {"success":False,"message":"Something Wrong"},500
        finally:
            os.remove(
                os.path.join(
                    os.path.join(os.getcwd(), STATIC, "uploads"),
                    f"{username}_login.jpeg",
                )
            )
