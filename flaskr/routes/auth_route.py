from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from ..models.user_model import db, UserModel
from flask_cors import cross_origin
import json
import cv2
import face_recognition
from ..config import STATIC, HASHING_METHOD
import base64
from PIL import Image
from io import BytesIO
import numpy as np
import os


from ..services.auth_service import AuthService
from ..services.image_service import CV2ImageService
from ..services.sign_up_service import *


abp = Blueprint('auth',__name__, url_prefix='/auth')
auth_service = AuthService(UserModel)
img_service = CV2ImageService()
account_controller = SignUpController()

@abp.route('/login', methods = ['POST'])
@cross_origin()
def login():
     if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # exist_user = UserModel.query.filter_by(username=username).all()
        exist_user = auth_service.find_user(username)
        if (len(exist_user) == 0):
            return {"success": False, "message":"Incorrect username"},401
        else:
            try:
                user = exist_user[0]
                _username = user.username
                _hash_password = user.password
                _salt = user.salt
                print("Hash_password: ",_hash_password)
                is_valid = auth_service.check_password(password,_salt,_hash_password)
                if (is_valid):
                    return {"success": True, "message":"Login Success"}, 200
                else:
                    return {"success": False, "message":"Incorrect password"},401
            except:
                return {"success":False,"message":"Something went wrong"},500 

    
@abp.route('/register', methods = ['OPTIONS','POST'])
@cross_origin()
def register():
        print("Kết nối thành công")
        try:
            data = request.json
            email = data['email']
            password = data['password']
            image = data['image']
            if email == "":
                return jsonify({"message": "Username cannot NULL"})
            elif password == "":
                return jsonify({"message": "Password cannot NULL"})
            elif image is None:
                return jsonify({"message": "Please provide a picture of your face"})
                
                
            base64_data = image.split(",")[1]
            image_data = base64.b64decode(base64_data)
            image = Image.open(BytesIO(image_data))
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            
            #print("password trước khi hash: ", password)
            add_todb = account_controller.upload_account(email, password, image)
            
            if add_todb:
                return jsonify({"message": "Account created successfully",
                                "success": True})
            return jsonify({"message": "Face could not be detected" })
        except:
            return {"success":False,"message":"Something went wrong"},500
    
@abp.route('/loginByFace',methods=['POST'])
@cross_origin()
def login_by_face():
     if request.method == 'POST':
        username = request.form['username']
        exist_user = UserModel.query.filter_by(username=username).all()
        if (len(exist_user) == 0):
            return {"success": False, "message":"Incorrect username"},401
        else:
            try:
                user = exist_user[0]
                _username = user.username
                img= request.files['img']
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
                    if any(matches):
                        print(matches)
                        return {"success":True,"message":"Success"}, 200
                
                return {"success":False,"message":"False"},401
            except:
                return {"success":False,"message":"Something went wrong"},500
            finally:
                os.remove(os.path.join(os.path.join(os.getcwd(),STATIC,"uploads"),f"{username}_login.jpeg"))
