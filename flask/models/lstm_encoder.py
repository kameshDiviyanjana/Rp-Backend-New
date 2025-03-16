import numpy as np
from tensorflow.keras.models import load_model
from sklearn.cluster import KMeans

# Load the pre-trained LSTM encoder model
encoder_model = load_model("lstm_encoder_model.keras")

# Load clustering model
clusters = np.load("clusters1.npy")  
num_clusters = len(np.unique(clusters))
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
latent_features = np.load("latent_features1.npy")
kmeans.fit(latent_features)
