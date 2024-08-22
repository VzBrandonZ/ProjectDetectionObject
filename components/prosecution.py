# Archivo: procesamiento.py

import cv2
import numpy as np

from components.voiceOutput import VoiceOutput

class ObjectDetector:
    def __init__(self, modelo, known_distance, known_width):
        self.modelo = modelo
        self.voz = VoiceOutput()
        self.known_distance = known_distance
        self.known_width = known_width
        self.focal_length = None

    def find_focal_length(self, pixel_width):
        """Calcular la distancia focal usando un objeto de tamaño conocido."""
        return (pixel_width * self.known_distance) / self.known_width

    def calculate_distance(self, pixel_width):
        """Calcular la distancia al objeto."""
        return (self.known_width * self.focal_length) / pixel_width

    def procesar_frame(self, frame):
        frame_rgb = frame
        detect = self.modelo(frame_rgb)

        info = detect.pandas().xyxy[0]
        renderizado = np.squeeze(detect.render())

        if len(info) > 0:
            objetos_detectados = ', '.join(info['name'].values)
            self.voz.speak(f"{objetos_detectados} detectado")

            # Supongamos que detectamos un solo objeto y calculamos su distancia
            object_width_pixels = info.iloc[0]['xmax'] - info.iloc[0]['xmin']
            if self.focal_length is None:
                # Calcular la distancia focal la primera vez
                self.focal_length = self.find_focal_length(object_width_pixels)

            # Calcular la distancia al objeto detectado
            distancia = self.calculate_distance(object_width_pixels)
            print(f"Distancia al objeto detectado: {distancia:.2f} cm")
            
            # Agregar la distancia al renderizado
            cv2.putText(renderizado, f"Distancia: {distancia:.2f} cm", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        return info, renderizado
