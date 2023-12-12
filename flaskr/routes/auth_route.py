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
from flask import Flask, request, jsonify, make_response

abp = Blueprint("auth", __name__, url_prefix="/auth")
auth_service = AuthService(UserModel)
img_service = CV2ImageService()


@abp.route("/login", methods=["POST"])
@cross_origin()
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        return auth_service.login(username, password)


@abp.route("/register", methods=["POST"])
@cross_origin()
def register():
    print("a")
    if request.method == "POST":
        print(request.form)
        username = request.form["username"]
        password = request.form["password"]
        img = request.files["img"]
        return auth_service.register(username, password, img)


@abp.route("/loginByFace", methods=["POST"])
@cross_origin()
def login_by_face():
    if request.method == "POST":
        username = request.form["username"]
        exist_user = auth_service.find_user(username)
        img = request.files["img"]
        return auth_service.login_by_face(username, img)
           

