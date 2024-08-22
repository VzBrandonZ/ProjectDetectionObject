import pyttsx3
import requests
from io import BytesIO

class VoiceOutput:
    def __init__(self):
        self.engine = pyttsx3.init()

    def speak(self, text):
        """
        Convertir texto a voz y reproducirlo localmente.
        """
        self.engine.say(text)
        self.engine.runAndWait()

    def send_audio_to_esp32(self, text, esp32_ip):
        """
        Convertir texto a voz y enviar el audio al ESP32-CAM para su transmisión por Bluetooth.
        """
        # Generar el audio en un buffer de memoria
        audio_buffer = BytesIO()
        self.engine.save_to_file(text, audio_buffer)
        self.engine.runAndWait()

        # Moverse al inicio del buffer
        audio_buffer.seek(0)

        # Enviar el audio al ESP32-CAM
        url = f'http://{esp32_ip}/audio'
        files = {'file': ('detected.wav', audio_buffer, 'audio/wav')}
        response = requests.post(url, files=files)

        if response.status_code == 200:
            print('Audio enviado con éxito al ESP32-CAM')
        else:
            print('Error al enviar el audio')
