import pyttsx3

class VoiceOutput:
    def __init__(self):
        self.engine = pyttsx3.init()

    def speak(self, text):
        """
        Convertir texto a voz.
        """
        self.engine.say(text)
        self.engine.runAndWait()
