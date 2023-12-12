from flask import Blueprint, request, Response, redirect, url_for, jsonify
import os
from ..config import *
from ..services.image_service import UploadImageService, ImageModel, SimilarityImageService
import base64
from PIL import Image
from io import BytesIO
import cv2
import numpy as np

ibp = Blueprint('img',__name__,url_prefix='/img')



IN_PATH = ""
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

image_upload = UploadImageService()
image_similarity = SimilarityImageService()

@ibp.route('/upload', methods=['POST'])
def upload_img():
    data = request.json
    email = data['email']
    image = data['image']
    print("email: ",email)
    if email == "":
        return jsonify({"message": "Username cannot NULL"})
    elif image is None:
        return jsonify({"message": "Please provide a picture"})
        
    try:
        base64_data = image.split(",")[1]

        image_data = base64.b64decode(base64_data)
        image = Image.open(BytesIO(image_data))
        
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        disease = image_similarity.Matching(image,0.5)

        add_todb = image_upload.upload_image(email, image, disease)
        print(disease)
        if add_todb:
            return jsonify({"message": "Add image successfully","disease":disease})
        return jsonify({"message": "Something wrong"})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"message": "error"})

@ibp.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename))

@ibp.route('/delete/<int:id>')
def delete(id):
    # Xóa ảnh từ cơ sở dữ liệu và thư mục lưu trữ
    UploadImageService.delete_image(id)
    return redirect(url_for('upload_img'))

@ibp.route('/show/<filename>')
def RGB2GRAY(filename):
    # Chuyển đổi ảnh sang ảnh xám và hiển thị giao diện
    gray_image = UploadImageService.convert_to_gray(filename)
    #return render_template('show.html', filename=gray_image)

@ibp.route('/detect/<filename>')
def face_detect(filename):
    # Chuyển đổi ảnh sang ảnh xám và hiển thị giao diện
    detect_image = UploadImageService.face_detect(filename)
    #return render_template('show_detect.html', filename=detect_image)
