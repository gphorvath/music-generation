import torchaudio
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
from datetime import datetime

duration=10
save_directory = "./audio/"
model_id = 'medium'

prompts = ['earthy tones, environmentally conscious, ukulele-infused, harmonic, breezy, easygoing, organic instrumentation, gentle grooves']
    # 'game menu loop', \
    # "fantasy game village"]

model = MusicGen.get_pretrained(model_id)
model.set_generation_params(duration)

wav = model.generate(prompts) 

for idx, one_wav in enumerate(wav):
    # Will save under {idx}.wav, with loudness normalization at -14 db LUFS.
    audio_write(f'{idx}', one_wav.cpu(), model.sample_rate, strategy="loudness")
