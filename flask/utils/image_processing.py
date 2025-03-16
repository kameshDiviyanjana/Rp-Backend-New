import io
import numpy as np
from PIL import Image

def process_image(image):
    img = Image.open(io.BytesIO(image)).convert("RGB")
    img = img.resize((64, 64))
    img_array = np.array(img) / 255.0
    return np.expand_dims(img_array, axis=0)
