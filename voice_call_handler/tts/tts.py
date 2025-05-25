import pyttsx3

def speak_text(text: str):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)  # скорость речи
    engine.setProperty("volume", 1.0)  # громкость
    engine.say(text)
    engine.runAndWait()
