import tensorflow as tf

# Load action recognition model
model_path = "./model/action_recognition_model.keras"
action_model = tf.keras.models.load_model(model_path)

# Define action labels
label_encoder_classes = [
    "catch", "dribble", "handstand", "jump", "kick_ball",
    "run", "somersault", "throw", "walk"
]
