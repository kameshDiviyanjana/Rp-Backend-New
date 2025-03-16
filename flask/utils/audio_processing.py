import io
import numpy as np
import librosa
from sklearn.preprocessing import MinMaxScaler

def preprocess_audio(file, sr=16000, n_mfcc=13, max_timesteps=100):
    try:
        audio, _ = librosa.load(io.BytesIO(file.read()), sr=sr)
        mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc).T

        if len(mfccs) < max_timesteps:
            pad_width = max_timesteps - len(mfccs)
            mfccs = np.pad(mfccs, ((0, pad_width), (0, 0)), mode='constant')
        else:
            mfccs = mfccs[:max_timesteps]

        scaler = MinMaxScaler()
        return np.expand_dims(scaler.fit_transform(mfccs), axis=0)
    except Exception as e:
        print(f"Error processing audio file: {e}")
        return None
