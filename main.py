import torch
import cv2
from components.model import ModelHandler
from components.video import VideoCapture, URLCapture
from components.prosecution import ObjectDetector
from components.interfaz import UIHandler
from components.voiceOutput import VoiceOutput

def main():
    # Rutas y configuraciones
    ruta_modelo = 'D:/TESIS/ProjectDetectionObject/model/best.pt'
    camara_id = 0  # Cambia esto por la URL si deseas usar una URL
    url = ""  # Deja esto vacío si deseas usar camara_id
    ancho = 640
    alto = 480

    # Parámetros de calibración
    KNOWN_DISTANCE = 50.0  # Distancia conocida en cm
    KNOWN_WIDTH = 8.5      # Ancho conocido del objeto en cm

    # Inicializar componentes
    modelo = ModelHandler(ruta_modelo)
    if url:
        captura = URLCapture(url)
    else:
        captura = VideoCapture(camara_id, ancho, alto)
    detector = ObjectDetector(modelo.detectar_objetos, KNOWN_DISTANCE, KNOWN_WIDTH)
    ui = UIHandler()
    voice_output = VoiceOutput()
    
    esp32_ip = "192.168.0.100"  # Reemplaza con la IP real de tu ESP32-CAM

    while True:
        # Capturar frame
        frame = captura.leer_frame()
        if frame is None:
            break

        # Procesar frame y obtener resultados de detección
        info, frame_renderizado = detector.procesar_frame(frame)
        print(info)

        # Verificar si el DataFrame de detección no está vacío
        if not info.empty:
            voice_output.send_audio_to_esp32("Objeto detectado", esp32_ip)

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
