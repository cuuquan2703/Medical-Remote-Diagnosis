import os
from flask import render_template, request, redirect, url_for
from datetime import datetime
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import os
from deepface.detectors import FaceDetector

from ..models.user_model import UserModel, db
from ..config import *
from ..services.auth_service import AuthService

authservice = AuthService(UserModel)
class SignUpController:
    def upload_account(self, username, password, image):
        try:
            
            detector = FaceDetector.build_model("opencv")
            
            
            file_name = secure_filename(f"{username}.jpeg")
            path_image = os.path.join(os.getcwd(),STATIC,"uploads")
            if not os.path.exists(path_image):
                os.makedirs(path_image)

            
            #cv2.imwrite(path_image, np.array(image))

            face_cascade = cv2.CascadeClassifier(os.path.join(os.getcwd(),"haarcascade_frontalface_default.xml"))
            image = face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            print(image, "----------------")
            cv2.imwrite(os.path.join(path_image,file_name), np.array(image))
            (new_password,_salt,algo) = authservice.create_hashing_password(password)['part']
            print(f"{algo},{_salt},{new_password}")
            new_account = UserModel(username=username, salt=_salt,password=new_password, img_path=path_image)
            db.session.add(new_account)
            db.session.commit()
            return True
        except Exception as e:
            print(f"Error: {str(e)}")
            return False
    

    # def get_all_account(self):
    #     account = UserModel.query.order_by(UserModel.date_created).all()
    #     return account

    # def delete_account(self, id):
    #     account = account.query.get(id)
    #     if account:
    #         db.session.delete(account)
    #         db.session.commit()
