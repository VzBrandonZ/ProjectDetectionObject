# Archivo: procesamiento.py

import cv2
import numpy as np

from components.voiceOutput import VoiceOutput  # Importar la clase VoiceOutput


class ObjectDetector:
    def __init__(self, modelo):
        self.modelo = modelo
        self.voz = VoiceOutput()

    def procesar_frame(self, frame):
        # Convertir el frame a formato que acepte el modelo (BGR a RGB)
        #frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb = frame
        # Realizar la detección
        detect = self.modelo(frame_rgb)

        # Obtener información de detección
        info = detect.pandas().xyxy[0]

        # Renderizar la detección en el frame original
        renderizado = np.squeeze(detect.render())

        # Si se detectan objetos, decirlo por salida por voz
        if len(info) > 0:
            objetos_detectados = ', '.join(info['name'].values)
            self.voz.speak(f"{objetos_detectados} detectado")

        return info, renderizado
