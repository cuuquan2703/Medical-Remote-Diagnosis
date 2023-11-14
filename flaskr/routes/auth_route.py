from flask import Blueprint, request
from werkzeug.utils import secure_filename
from ..models.user_model import db, UserModel
from flask_cors import cross_origin
import json
import cv2
import face_recognition
from ..config import STATIC, HASHING_METHOD

import os
from ..services.auth_service import AuthService
from ..services.image_service import CV2ImageService


abp = Blueprint('auth',__name__, url_prefix='/auth')
auth_service = AuthService(UserModel)
img_service = CV2ImageService()

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
                print(_hash_password)
                is_valid = auth_service.check_password(password,_salt,_hash_password)
                if (is_valid):
                    return {"success": True, "message":"Login Success"}, 200
                else:
                    return {"success": False, "message":"Incorrect password"},401
            except:
                return {"success":False,"message":"Something went wrong"},500 

    
@abp.route('/register', methods = ['POST'])
@cross_origin()
def register():
     if request.method == 'POST':
        print(request.form)                         
        username = request.form['username']
        password = request.form['password']
        img= request.files['img']
        print(request.files)
        # data = img.read()
        # mime = img.content_type
        # print(data)
        # print(mime)
        file_name = secure_filename(f"{username}.jpeg")
        upload_folder = os.path.join(os.getcwd(),STATIC,"uploads")
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        img.save(os.path.join(upload_folder,file_name))
        # exist_user = UserModel.query.filter_by(username=username).all()
        exist_user = auth_service.find_user(username)
        if (len(exist_user) > 0):
            return {"success": False, "message":"User exist"},401
        else:       
            try:   
            # hash_password = generate_password_hash(password,method=HASHING_METHOD).split("$")
            # algo = hash_password[0]
            # _salt = hash_password[1]
            # new_password = hash_password[2]
                (new_password,_salt,algo) = auth_service.create_hashing_password(password)['part']
                print(f"{algo},{_salt},{new_password}")
                new_user = UserModel(username=username, salt=_salt,password=new_password)
                db.session.add(new_user)
                db.session.commit()
                return {"success": True, "message":"Successfully Register"}
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
