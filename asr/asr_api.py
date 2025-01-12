from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from speech_to_text import SpeechToTextService
import uvicorn

app = FastAPI()

class TranscriptionResponse(BaseModel):
    transcription: str
    duration: str


@app.get("/ping")
async def ping():
    """
    A ping endpoint to return a response of "pong" to check if the service is working
    """
    return {"message": "pong"}


@app.post("/asr", response_model=TranscriptionResponse)
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Endpoint to transcribe uploaded audio file and return transcription and duration.
    """
    try:
        # Read the binary content of the uploaded file
        audio_binary = await file.read()

        # Transcribe audio from binary
        transcription, duration = stt.transcribe(audio_binary)

        # Note: No deletion done after processing as no temporary file was saved

    except Exception as e:
        return {"error": str(e)}

    return {"transcription": transcription, "duration": f"{duration:.1f}"}


if __name__ == "__main__":

    # Load speech to text object
    stt = SpeechToTextService()

    # Start the service
    uvicorn.run(app, host="0.0.0.0", port=8001)
