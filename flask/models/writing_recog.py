import tensorflow as tf

# Load hand gesture model
MODEL_PATH = "./model/final_sinhala_letter_model.h5"
gesture_model = tf.keras.models.load_model(MODEL_PATH)
