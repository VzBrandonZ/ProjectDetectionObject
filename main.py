# Archivo: main.py

import torch
import cv2
from components.model import ModelHandler
from components.video import VideoCapture, URLCapture
from components.prosecution import ObjectDetector
from components.interfaz import UIHandler


def main():
    # Rutas y configuraciones
    ruta_modelo = 'D:/TESIS/ProjectDetectionObject/model/best.pt'
    camara_id = 0  # Cambia esto por la URL si deseas usar una URL
    url = ""  # Deja esto vacío si deseas usar camara_id
    ancho = 640
    alto = 480

    # Inicializar componentes
    modelo = ModelHandler(ruta_modelo)
    if url:
        captura = URLCapture(url)
    else:
        captura = VideoCapture(camara_id, ancho, alto)
    detector = ObjectDetector(modelo.detectar_objetos)
    ui = UIHandler()

    while True:
        # Capturar frame
        frame = captura.leer_frame()
        if frame is None:
            break

        # Procesar frame y obtener resultados de detección
        info, frame_renderizado = detector.procesar_frame(frame)
        print(info)

        # Mostrar frame con detecciones
        ui.mostrar_frame('Detector de objetos', frame_renderizado)

        # Leer teclado
        tecla = ui.leer_teclado()
        if tecla == 27:  # Presionar ESC para salir
            break

    # Liberar recursos
    captura.liberar()
    ui.cerrar_ventanas()

if __name__ == "__main__":
    main()