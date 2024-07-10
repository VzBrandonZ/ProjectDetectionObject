# Importamos librerias
import torch
import cv2
import numpy as np

# Leemos el modelo
model = torch.hub.load('VzBrandonZ/Project-YOLOv7', 'custom',
                       path_or_model = 'D:/TESIS/ProjectDetectionObject/model/best.pt')

# Realizo Videocaptura
cap = cv2.VideoCapture(0)

# Empezamos
while True:
    # Realizamos lectura de frames
    ret, frame = cap.read()

    # Correccion de color
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Realizamos las detecciones
    detect = model(frame)

    info = detect.pandas().xyxy[0]  # im1 predictions
    print(info)

    # Mostramos FPS
    cv2.imshow('Detector de objetos', np.squeeze(detect.render()))

    # Leemos el teclado
    t = cv2.waitKey(5)
    if t == 27:
        break

cap.release()
cv2.destroyAllWindows()