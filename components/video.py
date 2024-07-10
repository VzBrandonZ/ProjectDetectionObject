# Archivo: video.py

import cv2

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
