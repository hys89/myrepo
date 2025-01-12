from io import BytesIO
import soundfile as sf
import librosa
import torch
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC

class SpeechToTextService:

    """
    A class for transcribing speech from audio files.
    """

    def __init__(self, model_name: str = "facebook/wav2vec2-large-960h"):
        """
        Initialize the SpeechToTextService with a specified model.

        Args:
            model_name (str): The name of the pre-trained model to load.
        """
        self.processor = Wav2Vec2Processor.from_pretrained(model_name)
        self.model = Wav2Vec2ForCTC.from_pretrained(model_name)


    def transcribe(self, audio_binary: bytes) -> dict:
        """
        Transcribe the provided audio file (binary) into text.

        Args:
            audio_binary (bytes): The binary content of an audio file.

        Returns:
            dict: A dictionary containing the transcription and duration.
        """

        # Load audio from binary
        with BytesIO(audio_binary) as audio_buffer:
            audio, rate = sf.read(audio_buffer, dtype="float32")
        
        # Ensure mono audio
        if len(audio.shape) > 1:  # If stereo, take mean to convert to mono
            audio = audio.mean(axis=1)
        
        # Resample to 16kHz
        if rate != 16000:
            audio = librosa.resample(audio, orig_sr=rate, target_sr=16000)
            rate = 16000
        
        # Calculate duration
        duration = librosa.get_duration(y=audio, sr=rate)
        
        # Preprocess audio for Wav2Vec2
        input_values = self.processor(audio, sampling_rate=rate, return_tensors="pt", padding=True).input_values
        
        # Perform inference
        with torch.no_grad():
            logits = self.model(input_values).logits

        # Decode the predicted logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.batch_decode(predicted_ids)[0]

        return transcription, duration
