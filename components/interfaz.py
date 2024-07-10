# Archivo: interfaz.py

import cv2

class UIHandler:
    def mostrar_frame(self, nombre_ventana, frame):
        cv2.imshow(nombre_ventana, frame)

    def leer_teclado(self, delay=5):
        return cv2.waitKey(delay)

    def cerrar_ventanas(self):
        cv2.destroyAllWindows()
