from ..config import STATIC, UPLOAD_FOLDER, MODEL_FOLDER
from ..models.image_model import *
from .logging_service import Logger

import sys
import os
import logging
import cv2
from werkzeug.utils import secure_filename
import numpy as np
from torchvision.models import resnet50
from skimage.transform import resize
import torch
from torchvision import transforms
from skimage import img_as_ubyte

IN_PATH = ""
OUT_PATH = ""

class ImageService():
    def __init__(self,service,name,static=STATIC):
        self.logger = Logger(logging)
        self.service = service
        self.name =  name
        self.static = static
    
    
    def _read(self,img_path):
        pass

    def _save(self,img,out_path=OUT_PATH):
        pass

    def _convert_rgb_to_gray(self,img):
        pass
    
    def _face_dectection(self,img,out_path=OUT_PATH):
        pass

    def read(self,img_path):
        self.logger.log("Reading Image . . .")
        try:
            res = self._read(img_path)
            self._save(res,self.out_path)
            self.logger.log("Success")
            return res
        except:
            self.logger.error(f"Somthing went wrog while loading image using {self.name}")
        finally:
            self.logger.log("Done")        



    def convert_rgb_to_gray(self,img):
        self.logger.log("Converting")
        try:
            res = self._convert_rgb_to_gray(img)
            self.logger.log("Success")
            return res
        except:
            self.logger.error(f"Somthing went wrog while conduct gray converting using {self.name}")
        finally:
            self.logger.log("Done")

    def face_detection(self,img_path):
        try:
            res = self._face_dectection(img_path)
            self.logger.log("Success")
            return res
        except:
            self.logger.error(f"Error in face detection process")
        finally:
            self.logger.log("Done")

class CV2ImageService(ImageService):
    def __init__(self):
        super().__init__(cv2,"cv2")

    def _read(self,img_path):
        image = self.service.imread(img_path)
        return image

    def _save(self,img, out_path):
        self.service.imwrite(out_path,img)

    def _convert_rgb_to_gray(self,img_path):
        img = self._read(img_path)
        gray = self.service.cvtColor(img, self.service.COLOR_BGR2GRAY)
        _,buff = self.service.imencode('.png', gray)
        return buff
    
    def _face_dectection(self, img, out_path):
        gray = self.service.cvtColor(img, self.service.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            self.service.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)

        self._save(img,out_path)
        _, buff = self.service.imencode('.png', img)

        return buff

class UploadImageService():
        
    def upload_image(self, username, file, disease ):
        try:
            folder_name = secure_filename(username)
            folder_path = os.path.join(UPLOAD_FOLDER, folder_name)
            
            if not(os.path.isdir(folder_path)):
                os.makedirs(folder_path)
                
            new_image = ImageModel(username=username, path = folder_path, result= disease)
            print(username,disease)
            image_path = folder_path+"/"+str(datetime.utcnow()).split(".")[0].replace(":","-")+".jpg"
            print("ĐƯờng dẫn: ",image_path)
            cv2.imwrite(folder_path+"/"+str(datetime.utcnow()).split(".")[0].replace(":","-")+".jpg", np.array(file))

            db.session.add(new_image)

            db.session.commit()
            return True
        except Exception as e:
            print(f"Error: {str(e)}")
            return False

    def delete_image(self, id):
        
        image = ImageModel.query.get(id)
        if image:
            db.session.delete(image)
            db.session.commit()
            # Xóa tệp ảnh từ thư mục lưu trữ
            os.remove(os.path.join(UPLOAD_FOLDER, image.path))
            #path_gray = os.path.join(server.config['GRAY_FOLDER'], image.path)
            #path_detect = os.path.join(server.config['DETECT_FOLDER'], image.path)
            # if os.path.exists(path_gray):
            #     os.remove(path_gray)
            #     os.remove(path_detect)
            
class SimilarityImageService():
    def Matching(self, image, threshold):
        try:
            
            
            list_image = os.listdir(MODEL_FOLDER)
            print("Kết quả1: ")
            model = torch.load("../Model/Resnet50.pt")
            print("Kết quả2: ", MODEL_FOLDER,list_image[0])
            image_path = os.path.join(MODEL_FOLDER,list_image[0])
            print("Kết quả3: ")
            data_image = cv2.imread(image_path)
            print("Kết quả4: ")
            result = list_image[0]
            print("Kết quả5: ")
            score = self.Get_image_difference(model,data_image,image)
            print("Kết quả6: ")
            for image_name in list_image:
                image_path = os.path.join(MODEL_FOLDER,image_name)
                data_image = cv2.imread(image_path)
                distance = self.Get_image_difference(model,data_image,image)
                if distance < threshold:
                    result = image_name
                    break
                elif distance < score:
                    result = image_name
                    score = distance
            return result
        except Exception as e:
            print(f"Error: {str(e)}")
            
            
    @staticmethod
    def Get_image_difference(model, image1, image2):
        try:
            image1 = resize(image1, (224, 224))
            image1 = img_as_ubyte(image1)

            image2 = resize(image2, (224, 224))
            image2 = img_as_ubyte(image2)
            
            # Normalize and convert to PyTorch tensor
            transform = transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])
            
            input_image1 = transform(image1).unsqueeze(0)
            input_image2 = transform(image2).unsqueeze(0)
            
            model.eval()
            
            output1 = model(input_image1)
            output2 = model(input_image2)
            
            return torch.norm(output1 - output2, p=2)
        except Exception as e:
            print(f"Error: {str(e)}")