from voice_call_handler.stt import transcribe_audio

if __name__ == "__main__":
    path = "voice_call_handler/examples/audio_example.wav"
    text = transcribe_audio(path)
    print("Текст из аудио:", text) 