import cv2
from torchvision import transforms

class Utils:
    def preprocess(self, frame):
        """
        Preprocesar la imagen para que sea compatible con el modelo YOLOv7.
        """
        transform = transforms.Compose([
            transforms.ToTensor()
        ])
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = transform(img).unsqueeze(0)
        return img

    def draw_boxes(self, frame, results):
        """
        Dibujar las cajas delimitadoras en la imagen.
        """
        detected_objects = set()
        for i, (xmin, ymin, xmax, ymax, confidence, class_id) in enumerate(results.xyxy[0].cpu().numpy()):
            label = self.model.names[int(class_id)]
            cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 2)
            cv2.putText(frame, f'{label} {confidence:.2f}', 
                        (int(xmin), int(ymin)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            detected_objects.add(label)

        return frame, detected_objects
