import tensorflow as tf

# Load hand gesture model
MODEL_PATH = "./model/hand_gesture_model.h5"
gesture_model = tf.keras.models.load_model(MODEL_PATH)
