from fastapi import FastAPI, File, UploadFile
import shutil
import tempfile
from services.speech_service import SpeechService
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv('SPEECH_API_KEY')
region = os.getenv('SPEECH_SERVICE_REGION')

if not api_key or not region:
    raise ValueError("Missing Azure credentials. Please set `SPEECH_API_KEY` and `SPEECH_SERVICE_REGION`.")

# Initialize SpeechService
speech_service = SpeechService(api_key, region)

# FastAPI instance
app = FastAPI()

@app.post("/upload_audio")
async def upload_audio(file: UploadFile = File(...)):
    temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    with open(temp_audio_file.name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    transcription = speech_service.listen_once(temp_audio_file.name)
    return {"transcription": transcription}
