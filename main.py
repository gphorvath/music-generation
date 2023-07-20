from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import torchaudio
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
import os
from datetime import datetime

app = FastAPI()

# Ensure the audio directory exists
os.makedirs('audio', exist_ok=True)

@app.post("/generate")
async def generate(prompt: str, duration: float):
    save_directory = "./audio/"
    model_id = 'medium'

    model = MusicGen.get_pretrained(model_id)
    model.set_generation_params(duration)

    wav = model.generate(prompt) 

    # Will save under {idx}.wav, with loudness normalization at -14 db LUFS.
    # ct stores current time
    ct = datetime.datetime.now()
    print("current time:-", ct)
    #filename = f'{idx}.wav'
    filename = '{ct}.wav'
    audio_write(filename, wav.cpu(), model.sample_rate, strategy="loudness")
    
    # return the path to the first file generated
    return FileResponse(f'./audio/{filename}', media_type='audio/wav')

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
