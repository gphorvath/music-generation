from transformers import AutoProcessor, MusicgenForConditionalGeneration

PRETRAINED_MODEL_NAME = "facebook/musicgen-small"
MODEL_SAVE_PATH = f"./models/{PRETRAINED_MODEL_NAME}"

processor = AutoProcessor.from_pretrained(PRETRAINED_MODEL_NAME)
processor.save_pretrained(MODEL_SAVE_PATH)

model = MusicgenForConditionalGeneration.from_pretrained(PRETRAINED_MODEL_NAME)
model.save_pretrained(MODEL_SAVE_PATH, use_safetensors=True)
