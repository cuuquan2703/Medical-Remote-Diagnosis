import sys
from os.path import dirname,abspath, join
from .logging_service import Logger
import logging
import cv2
from ..config import STATIC, HASHING_METHOD

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

