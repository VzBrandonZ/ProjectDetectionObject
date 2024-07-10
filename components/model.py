# Archivo: model.py

import torch

class ModelHandler:
    def __init__(self, ruta_modelo):
        self.model = torch.hub.load('VzBrandonZ/Project-YOLOv7', 'custom', path_or_model=ruta_modelo)

    def detectar_objetos(self, frame):
        return self.model(frame)
