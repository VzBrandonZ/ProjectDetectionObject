from components.yolov7Detector import YOLOv7Detector

if __name__ == "__main__":
    # Ruta del modelo y URL de la cámara ESP32CAM
    model_path = 'path/to/your/yolov7_model.pt'
    video_url = 'http://<IP_CAM>/video'

    # Crear instancia del detector y ejecutar
    detector = YOLOv7Detector(model_path, video_url)
    detector.run()
