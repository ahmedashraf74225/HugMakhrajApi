from fastapi import FastAPI, WebSocket
from transformers import pipeline
import torchaudio.transforms as T
import soundfile as sf
import io

app = FastAPI()

pipe = pipeline(model="AsemBadr/whisper-small-final-v3", task="automatic-speech-recognition")
TARGET_SAMPLE_RATE = 16000

@app.get("/hi")
async def root():
    return {"message": "Eid Mubarek"}

def preprocess_audio(audio_data: bytes):
    audio_file = io.BytesIO(audio_data)
    audio, sample_rate = sf.read(audio_file, dtype='float32')

    if sample_rate != TARGET_SAMPLE_RATE:
        resampler = T.Resample(sample_rate, TARGET_SAMPLE_RATE)
        audio = resampler(audio)

    return audio

def transcribe_audio(waveform):
    result = pipe(waveform)
    return result['text']

@app.websocket("/transcribe")
async def transcribe(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_bytes()
        if data:
            waveform = preprocess_audio(data)
            transcription = transcribe_audio(waveform)
            await websocket.send_text(transcription)
        else:
            break

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
