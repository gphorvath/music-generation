from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import torchaudio
import torch
import time
from transformers import (
    AutoConfig,
    AutoProcessor,
    MusicgenForConditionalGeneration,
)
import transformers.utils.logging
import scipy
from sigfig import round
import os
from datetime import datetime
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)

transformers.utils.logging.enable_progress_bar()

# Setup audiofile save directory
save_directory = "./audio/"
os.makedirs(save_directory, exist_ok=True)

# Setup Audio Models
PRETRAINED_MODEL_NAME = "facebook/musicgen-small"
MODEL_SAVE_PATH = f"./models/{PRETRAINED_MODEL_NAME}"
config = AutoConfig.from_pretrained(
    MODEL_SAVE_PATH, local_files_only=True, trust_remote_code=True
)
logging.info(f'Serving Model: {PRETRAINED_MODEL_NAME}')

device = "cuda:0" if torch.cuda.is_available() else "cpu"

logging.info(f"Running on: {device}")
processor = AutoProcessor.from_pretrained(MODEL_SAVE_PATH)
model = MusicgenForConditionalGeneration.from_pretrained(MODEL_SAVE_PATH).to(device)


app.mount("/audio", StaticFiles(directory="audio"), name="audio")
@app.get("/audio")
def audios():
    out = []
    for filename in os.listdir(save_directory):
        out.append({
            "name": filename.split(".")[0],
            "path": save_directory + filename
        })
    return out

@app.get("/generate")
async def generate(prompt: str, tokens: int):
    inputs = processor(
        text=prompt,
        padding=True,
        return_tensors="pt"
    ).to(device)
    filename = f'{datetime.now().timestamp()}.wav'
    filename = save_directory+filename
    logging.info(f'Save file: {filename}')
    logging.info(f'Prompt: {prompt}')
    logging.info(f'Tokens: {tokens}')
    logging.info(f'Begin Generation on: ')
    logging.info(torch.cuda.get_device_properties("cuda:0") if torch.cuda.is_available() else "cpu" )

    tic = time.time()

    audio_values = model.generate(**inputs, max_new_tokens=tokens).to(device)

    toc = time.time()

    logging.info(f'Generation complete in {round(toc-tic, sigfigs=4)} seconds!')
    

    sampling_rate = model.config.audio_encoder.sampling_rate
    data = audio_values[0, 0].cpu().numpy()

    logging.info(f"Writing to: {filename}")

    scipy.io.wavfile.write(filename, rate=sampling_rate, data=data)
    
    # return the path to the first file generated
    return FileResponse(filename, media_type='audio/wav')

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
