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
        exist_user = auth_service.find_user(username)
        if (len(exist_user) > 0):
            return {"success": False, "message":"User exist"},401
        else:       
            try:   
                new_user = auth_service.register(username,password,img)
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
        exist_user = auth_service.find_user(username)
        if (len(exist_user) == 0):
            return {"success": False, "message":"Incorrect username"},401
        else:
            try:
                user = exist_user[0]
                _username = user.username
                img= request.files['img']

                matches = auth_service.login_by_face(username,img)
                if any(matches):
                    return {"success":True,"message":"Success"}, 200
                
                return {"success":False,"message":"False"},401
            except:
                return {"success":False,"message":"Something went wrong"},500
            finally:
                os.remove(os.path.join(os.path.join(os.getcwd(),STATIC,"uploads"),f"{username}_login.jpeg"))
