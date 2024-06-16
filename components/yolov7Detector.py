import cv2
import torch
#from torchvision import transforms
from utils import Utils
from voiceOutput import VoiceOutput

class YOLOv7Detector:
    def __init__(self, model_path, video_url):
        # Cargar el modelo YOLOv7
        self.model = torch.hub.load('WongKinYiu/yolov7', 'custom', path=model_path)
        self.model.eval()

        # Dirección URL de la transmisión de video de ESP32CAM
        self.video_url = video_url

        # Capturar video de la ESP32CAM
        self.cap = cv2.VideoCapture(self.video_url)

        # Instancia la clase Utils
        self.utils = Utils()

        # Instancia la clase VoiceOutput
        self.voiceOutput = VoiceOutput()

    def detect_objects(self, frame):
        """
        Realizar la detección de objetos en el frame.
        """
        img = self.utils.preprocess(frame)

        # Realizar la detección
        with torch.no_grad():
            results = self.model(img)

        return results

    def run(self):
        """
        Ejecutar el bucle principal para capturar video y realizar detección de objetos.
        """
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("No se puede recibir frame (stream end?). Saliendo ...")
                break

            # Detectar objetos
            results = self.detect_objects(frame)

            # Dibujar las cajas delimitadoras y obtener objetos detectados
            frame, detected_objects = self.utils.draw_boxes(frame, results)

            # Mostrar la imagen con las detecciones
            cv2.imshow('Detecciones', frame)

            # Salida por voz para los objetos detectados
            if detected_objects:
                detected_objects_str = ', '.join(detected_objects)
                self.voiceOutput.speak(f"Se detectaron {detected_objects_str}")

            # Cerrar el programa con la tecla 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Liberar los recursos
        self.cap.release()
        cv2.destroyAllWindows()
