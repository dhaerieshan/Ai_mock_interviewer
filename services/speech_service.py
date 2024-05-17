import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import os

load_dotenv()

class SpeechService:
    def __init__(self, speech_key, service_region):
        self.speech_key = speech_key
        self.service_region = service_region
        self.initialize_speech_components()

    def initialize_speech_components(self):
        self.speech_config = speechsdk.SpeechConfig(subscription=self.speech_key, region=self.service_region)

    def listen_once(self, audio_file_path):
        audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_config)
        result = speech_recognizer.recognize_once()
        return self.handle_result(result)

    def handle_result(self, result):
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return result.text
        elif result.reason == speechsdk.ResultReason.NoMatch:
            return "No speech could be recognized."
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            return f"Speech recognition canceled: {cancellation_details.reason}"
        return None

    def speak(self, text):
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config)
        speech_synthesizer.speak_text(text)
