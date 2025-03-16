import sys
import librosa
import numpy as np
from tensorflow.keras.models import load_model

model = load_model("lstm_model.h5")

def analyze_audio(audio_path):
    y, sr = librosa.load(audio_path, sr=22050)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
    features = np.mean(mfccs.T, axis=0)

    input_features = features.reshape(1, 1, -1)
    prediction = model.predict(input_features)

    return "Correct pronunciation" if prediction[0][0] > 0.5 else "Needs improvement"

if __name__ == "__main__":
    audio_path = sys.argv[1]
    print(analyze_audio(audio_path))
