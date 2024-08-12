# Archivo: video.py

import cv2
import urllib.request
import numpy as np

class VideoCapture:
    def __init__(self, camara_id=0, ancho=640, alto=480):
        self.cap = cv2.VideoCapture(camara_id)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, ancho)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, alto)

    def leer_frame(self):
        ret, frame = self.cap.read()
        if ret:
            return frame
        else:
            return None

    def liberar(self):
        self.cap.release()

class URLCapture:
    def __init__(self, url):
        self.url = url

    def leer_frame(self):
        with urllib.request.urlopen(self.url) as resp:
            arr = np.asarray(bytearray(resp.read()), dtype=np.uint8)
            frame = cv2.imdecode(arr, -1)
            return frame

    def liberar(self):
        pass  # No se necesita liberar nada para la captura de URL