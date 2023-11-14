from flask import Blueprint, request, Response
import os

from services import CV2ImageService


ibp = Blueprint('img',__name__,url_prefix='img')

service = CV2ImageService()
IN_PATH = ""

@ibp.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    img_path=IN_PATH
    file.save(img_path)

    buff = service.face_detection(img_path)
    return Response(buff.tobytes(), content_type='image/png')


