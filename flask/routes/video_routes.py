# from flask import Blueprint, request, jsonify
# import cv2
# import os
# from utils.video_processing import extract_skeleton_from_frame,prepare_sequence,normalize_keypoints
# from models.action_recognition import action_model, label_encoder_classes
# import numpy as np

# video_bp = Blueprint("video_bp", __name__)

# @video_bp.route('/upload', methods=['POST'])
# def upload_video():
#     if 'file' not in request.files:
#         return jsonify({"error": "No file provided"}), 400

#     file = request.files['file']
#     input_path = f"uploads/{file.filename}"
#     output_path = f"outputs/{os.path.splitext(file.filename)[0]}_processed.mp4"

#     # Save uploaded file
#     os.makedirs("uploads", exist_ok=True)
#     os.makedirs("outputs", exist_ok=True)
#     file.save(input_path)

#     # Process video
#     cap = cv2.VideoCapture(input_path)
#     frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     fps = int(cap.get(cv2.CAP_PROP_FPS))

#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

#     sequence = []
#     sequence_length = 30
#     predictions = []

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         keypoints = extract_skeleton_from_frame(frame)
#         if keypoints is not None:
#             normalized_keypoints = normalize_keypoints(keypoints)
#             sequence.append(normalized_keypoints.flatten())

#             if len(sequence) == sequence_length:
#                 input_sequence = prepare_sequence(np.array(sequence), sequence_length=sequence_length)
#                 input_sequence = input_sequence.reshape(1, sequence_length, -1)

#                 prediction = action_model.predict(input_sequence)
#                 predicted_label = label_encoder_classes[np.argmax(prediction)]

#                 feedback = f"Detected action: {predicted_label}"
#                 predictions.append({"frame": len(predictions) + 1, "prediction": predicted_label, "feedback": feedback})

#                 cv2.putText(frame, f"Action: {predicted_label}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
#                 sequence.pop(0)

#         out.write(frame)

#     cap.release()
#     out.release()

#     # Send predictions and video as response
#     return jsonify({
#         "predictions": predictions,
#         "video_url": output_path
    # })


    # New one 

    

# from flask import Flask, request, jsonify,Blueprint
# from flask_cors import CORS
# import numpy as np
# import torch
# import cv2
# import mediapipe as mp
# import os


# easy_classes = 3
# medium_classes = 2
# hard_classes = 3

# class ActionRecognitionModel(torch.nn.Module):
#     def __init__(self, input_size, hidden_size, num_classes):
#         super(ActionRecognitionModel, self).__init__()
#         self.lstm1 = torch.nn.LSTM(input_size, hidden_size, batch_first=True, bidirectional=True)
#         self.lstm2 = torch.nn.LSTM(hidden_size * 2, hidden_size // 2, batch_first=True, bidirectional=True)
#         self.fc = torch.nn.Linear(hidden_size, num_classes)
    
#     def forward(self, x):
#         h_lstm1, _ = self.lstm1(x)
#         h_lstm2, _ = self.lstm2(h_lstm1)
#         h_lstm2 = h_lstm2[:, -1, :]
#         out = self.fc(h_lstm2)
#         return out

# easy_model = ActionRecognitionModel(input_size=99, hidden_size=64, num_classes=easy_classes)
# easy_model.load_state_dict(torch.load("models/easy_action_model.pth"))
# easy_model.eval()

# medium_model = ActionRecognitionModel(input_size=99, hidden_size=64, num_classes=medium_classes)
# medium_model.load_state_dict(torch.load("models/medium_action_model.pth"))
# medium_model.eval()

# hard_model = ActionRecognitionModel(input_size=99, hidden_size=64, num_classes=hard_classes)
# hard_model.load_state_dict(torch.load("models/hard_action_model.pth"))
# hard_model.eval()

# mp_pose = mp.solutions.pose

# def extract_keypoints(video_path):
#     pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
#     cap = cv2.VideoCapture(video_path)
#     keypoints_list = []
#     frames_with_keypoints = 0
#     total_frames = 0

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
#         total_frames += 1
#         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         results = pose.process(frame_rgb)
#         if results.pose_landmarks:
#             frames_with_keypoints += 1
#             keypoints = np.array([[lm.x, lm.y, lm.z] for lm in results.pose_landmarks.landmark]).flatten()
#             keypoints_list.append(keypoints)
    
#     cap.release()
#     return np.array(keypoints_list), frames_with_keypoints, total_frames

# def get_message(score, detection_ratio):
#     if detection_ratio < 0.1:
#         return "No human detected in most frames. Please ensure you're in front of the camera."
#     if score == 0:
#         return "Action not recognized. Please try again."
#     elif 1 <= score <= 10:
#         return "It is very hard to find the action."
#     elif 11 <= score <= 40:
#         return "Child is finding it hard to perform the action. Please repeat the action as shown in the video and try again."
#     elif 41 <= score <= 79:
#         return "Child is performing at a medium level. Keep practicing to improve."
#     else:
#         return "Child is performing well! The action is easy for them."

# def get_diff_level(score, detection_ratio):
#     if detection_ratio < 0.1:
#         return "No detection"
#     if score == 0:
#         return "No level"
#     elif 1 <= score <= 40:
#         return "Easy"
#     elif 41 <= score <= 79:
#         return "Medium"
#     else:
#         return "Hard"


# video_bp = Blueprint("video_bp", __name__)

# @video_bp.route('/upload', methods=['POST'])
# def predict():
#     if "file" not in request.files:
#         return jsonify({"error": "No file uploaded"}), 400
    
#     file = request.files["file"]
#     actual_class = request.form.get("actual_class", "").strip()
    
#     if not actual_class:
#         return jsonify({"error": "No actual class provided"}), 400
    
#     video_path = "temp_video.mp4"
#     file.save(video_path)
    
#     keypoints, frames_with_keypoints, total_frames = extract_keypoints(video_path)
#     detection_ratio = frames_with_keypoints / total_frames if total_frames > 0 else 0
    
#     if detection_ratio < 0.1:
#         return jsonify({
#             "predictions": [],
#             "percentage": "0",
#             "message": get_message(0, detection_ratio),
#             "level": get_diff_level(0, detection_ratio),
#             "predicted_action": "none",
#             "actual_class": actual_class,
#             "receivedPredictions": {},
#             "detection_ratio": f"{detection_ratio:.2f}"
#         })
    
#     if len(keypoints) == 0:
#         return jsonify({"error": "No keypoints detected"}), 400
    
#     keypoints = torch.tensor(np.expand_dims(keypoints, axis=0), dtype=torch.float32)
    
#     easy_actions = {"catch": 0, "stand": 1, "walk": 2}
#     medium_actions = {"run": 0, "throw": 1}
#     hard_actions = {"dribble": 0, "handstand": 1, "kick-ball": 2}
    
#     if actual_class in easy_actions:
#         model = easy_model
#         label_to_int = easy_actions
#         endpoint = "easy"
#     elif actual_class in medium_actions:
#         model = medium_model
#         label_to_int = medium_actions
#         endpoint = "medium"
#     elif actual_class in hard_actions:
#         model = hard_model
#         label_to_int = hard_actions
#         endpoint = "hard"
#     else:
#         return jsonify({"error": "Invalid action class"}), 400
    
#     with torch.no_grad():
#         prediction = model(keypoints)
#         probabilities = torch.softmax(prediction, dim=1)
#         predicted_label = torch.argmax(prediction, dim=1).item()
    
#     int_to_label = {v: k for k, v in label_to_int.items()}
#     predicted_action = int_to_label[predicted_label]
    
#     if predicted_action != actual_class:
#         score = 1 
#     else:
#         score = probabilities[0][predicted_label].item() * 100
    
#     message = get_message(int(round(score)), detection_ratio)
#     level = get_diff_level(int(round(score)), detection_ratio)
#     class_probabilities = {int_to_label[i]: float(probabilities[0][i].item()) for i in range(probabilities.size(1))}
    
#     os.remove(video_path)
#     return jsonify({
#         "predictions": [{"prediction": predicted_action, "confidence": class_probabilities.get(predicted_action, 0)}],
#         "percentage": f"{score:.0f}",
#         "message": message,
#         "level": level,
#         "predicted_action": predicted_action,
#         "actual_class": actual_class,
#         "receivedPredictions": class_probabilities,
#         "detection_ratio": f"{detection_ratio:.2f}",
#         "endpoint": endpoint
#     })

# def upload_video():
#     if 'file' not in request.files:
#         return jsonify({"error": "No file provided"}), 400

#     file = request.files['file']
#     input_path = f"uploads/{file.filename}"
#     os.makedirs("uploads", exist_ok=True)
#     file.save(input_path)

#     cap = cv2.VideoCapture(input_path)
#     predictions = []

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         keypoints = extract_skeleton_from_frame(frame)
#         if keypoints is not None:
#             input_data = keypoints.flatten().reshape(1, -1)
#             prediction = action_model.predict(input_data)
#             predicted_label = label_encoder_classes[np.argmax(prediction)]
#             predictions.append(predicted_label)

#     cap.release()

#     return jsonify({"predictions": predictions})

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import numpy as np
# import torch
# import cv2
# import mediapipe as mp
# import os

# easy_classes = 3
# medium_classes = 2
# hard_classes = 3

# class ActionRecognitionModel(torch.nn.Module):
#     def __init__(self, input_size, hidden_size, num_classes):
#         super(ActionRecognitionModel, self).__init__()
#         self.lstm1 = torch.nn.LSTM(input_size, hidden_size, batch_first=True, bidirectional=True)
#         self.lstm2 = torch.nn.LSTM(hidden_size * 2, hidden_size // 2, batch_first=True, bidirectional=True)
#         self.fc = torch.nn.Linear(hidden_size, num_classes)
    
#     def forward(self, x):
#         h_lstm1, _ = self.lstm1(x)
#         h_lstm2, _ = self.lstm2(h_lstm1)
#         h_lstm2 = h_lstm2[:, -1, :]
#         out = self.fc(h_lstm2)
#         return out

# easy_model = ActionRecognitionModel(input_size=99, hidden_size=64, num_classes=easy_classes)
# easy_model.load_state_dict(torch.load("models/easy_action_model.pth"))
# easy_model.eval()

# medium_model = ActionRecognitionModel(input_size=99, hidden_size=64, num_classes=medium_classes)
# medium_model.load_state_dict(torch.load("models/medium_action_model.pth"))
# medium_model.eval()

# hard_model = ActionRecognitionModel(input_size=99, hidden_size=64, num_classes=hard_classes)
# hard_model.load_state_dict(torch.load("models/hard_action_model.pth"))
# hard_model.eval()

# mp_pose = mp.solutions.pose

# def extract_keypoints(video_path):
#     pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
#     cap = cv2.VideoCapture(video_path)
#     keypoints_list = []
#     frames_with_keypoints = 0
#     total_frames = 0

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
#         total_frames += 1
#         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         results = pose.process(frame_rgb)
#         if results.pose_landmarks:
#             frames_with_keypoints += 1
#             keypoints = np.array([[lm.x, lm.y, lm.z] for lm in results.pose_landmarks.landmark]).flatten()
#             keypoints_list.append(keypoints)
    
#     cap.release()
#     return np.array(keypoints_list), frames_with_keypoints, total_frames

# def get_message(score, detection_ratio):
#     if detection_ratio < 0.1:
#         return "No human detected in most frames. Please ensure you're in front of the camera."
#     if score == 0:
#         return "Action not recognized. Please try again."
#     elif 1 <= score <= 10:
#         return "It is very hard to find the action."
#     elif 11 <= score <= 40:
#         return "Child is finding it hard to perform the action. Please repeat the action as shown in the video and try again."
#     elif 41 <= score <= 79:
#         return "Child is performing at a medium level. Keep practicing to improve."
#     else:
#         return "Child is performing well! The action is easy for them."

# def get_diff_level(score, detection_ratio):
#     if detection_ratio < 0.1:
#         return "No detection"
#     if score == 0:
#         return "No level"
#     elif 1 <= score <= 40:
#         return "Easy"
#     elif 41 <= score <= 79:
#         return "Medium"
#     else:
#         return "Hard"



# @app.route("/action/predict", methods=["POST"])
# def predict():
#     if "file" not in request.files:
#         return jsonify({"error": "No file uploaded"}), 400
    
#     file = request.files["file"]
#     actual_class = request.form.get("actual_class", "").strip()
    
#     if not actual_class:
#         return jsonify({"error": "No actual class provided"}), 400
    
#     video_path = "temp_video.mp4"
#     file.save(video_path)
    
#     keypoints, frames_with_keypoints, total_frames = extract_keypoints(video_path)
#     detection_ratio = frames_with_keypoints / total_frames if total_frames > 0 else 0
    
#     if detection_ratio < 0.1:
#         return jsonify({
#             "predictions": [],
#             "percentage": "0",
#             "message": get_message(0, detection_ratio),
#             "level": get_diff_level(0, detection_ratio),
#             "predicted_action": "none",
#             "actual_class": actual_class,
#             "receivedPredictions": {},
#             "detection_ratio": f"{detection_ratio:.2f}"
#         })
    
#     if len(keypoints) == 0:
#         return jsonify({"error": "No keypoints detected"}), 400
    
#     keypoints = torch.tensor(np.expand_dims(keypoints, axis=0), dtype=torch.float32)
    
#     easy_actions = {"catch": 0, "stand": 1, "walk": 2}
#     medium_actions = {"run": 0, "throw": 1}
#     hard_actions = {"dribble": 0, "handstand": 1, "kick-ball": 2}
    
#     if actual_class in easy_actions:
#         model = easy_model
#         label_to_int = easy_actions
#         endpoint = "easy"
#     elif actual_class in medium_actions:
#         model = medium_model
#         label_to_int = medium_actions
#         endpoint = "medium"
#     elif actual_class in hard_actions:
#         model = hard_model
#         label_to_int = hard_actions
#         endpoint = "hard"
#     else:
#         return jsonify({"error": "Invalid action class"}), 400
    
#     with torch.no_grad():
#         prediction = model(keypoints)
#         probabilities = torch.softmax(prediction, dim=1)
#         predicted_label = torch.argmax(prediction, dim=1).item()
    
#     int_to_label = {v: k for k, v in label_to_int.items()}
#     predicted_action = int_to_label[predicted_label]
    
#     if predicted_action != actual_class:
#         score = 1 
#     else:
#         score = probabilities[0][predicted_label].item() * 100
    
#     message = get_message(int(round(score)), detection_ratio)
#     level = get_diff_level(int(round(score)), detection_ratio)
#     class_probabilities = {int_to_label[i]: float(probabilities[0][i].item()) for i in range(probabilities.size(1))}
    
#     os.remove(video_path)
#     return jsonify({
#         "predictions": [{"prediction": predicted_action, "confidence": class_probabilities.get(predicted_action, 0)}],
#         "percentage": f"{score:.0f}",
#         "message": message,
#         "level": level,
#         "predicted_action": predicted_action,
#         "actual_class": actual_class,
#         "receivedPredictions": class_probabilities,
#         "detection_ratio": f"{detection_ratio:.2f}",
#         "endpoint": endpoint
#     })


from flask import Blueprint, request, jsonify
import numpy as np
import torch
import os
import cv2
import mediapipe as mp

video_bp = Blueprint('video_bp', __name__)


# easy_classes = 3
# medium_classes = 2
# hard_classes = 3

# # LSTM Model Definition
# class ActionRecognitionModel(torch.nn.Module):
#     def __init__(self, input_size, hidden_size, num_classes):
#         super(ActionRecognitionModel, self).__init__()
#         self.lstm1 = torch.nn.LSTM(input_size, hidden_size, batch_first=True, bidirectional=True)
#         self.lstm2 = torch.nn.LSTM(hidden_size * 2, hidden_size // 2, batch_first=True, bidirectional=True)
#         self.fc = torch.nn.Linear(hidden_size, num_classes)
    
#     def forward(self, x):
#         h_lstm1, _ = self.lstm1(x)
#         h_lstm2, _ = self.lstm2(h_lstm1)
#         h_lstm2 = h_lstm2[:, -1, :]
#         out = self.fc(h_lstm2)
#         return out

# # Load models safely
# easy_model = ActionRecognitionModel(input_size=99, hidden_size=64, num_classes=easy_classes)
# medium_model = ActionRecognitionModel(input_size=99, hidden_size=64, num_classes=medium_classes)
# hard_model = ActionRecognitionModel(input_size=99, hidden_size=64, num_classes=hard_classes)

# # Load models from correct path
# model_folder = os.path.join(os.path.dirname(__file__), '..', 'models')
# easy_model_path = os.path.join(model_folder, 'easy_action_model.pth')
# medium_model_path = os.path.join(model_folder, 'medium_action_model.pth')
# hard_model_path = os.path.join(model_folder, 'hard_action_model.pth')

# try:
#     easy_model.load_state_dict(torch.load(easy_model_path, map_location=torch.device('cpu')))
#     easy_model.eval()
# except FileNotFoundError:
#     print(f"Model file not found: {easy_model_path}")

# try:
#     medium_model.load_state_dict(torch.load(medium_model_path, map_location=torch.device('cpu')))
#     medium_model.eval()
# except FileNotFoundError:
#     print(f"Model file not found: {medium_model_path}")

# try:
#     hard_model.load_state_dict(torch.load(hard_model_path, map_location=torch.device('cpu')))
#     hard_model.eval()
# except FileNotFoundError:
#     print(f"Model file not found: {hard_model_path}")

# # Mediapipe
# mp_pose = mp.solutions.pose

# def extract_keypoints(video_path):
#     pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
#     cap = cv2.VideoCapture(video_path)
#     keypoints_list = []
#     frames_with_keypoints = 0
#     total_frames = 0

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
#         total_frames += 1
#         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         results = pose.process(frame_rgb)
#         if results.pose_landmarks:
#             frames_with_keypoints += 1
#             keypoints = np.array([[lm.x, lm.y, lm.z] for lm in results.pose_landmarks.landmark]).flatten()
#             keypoints_list.append(keypoints)
    
#     cap.release()
#     return np.array(keypoints_list), frames_with_keypoints, total_frames

# def get_message(score, detection_ratio):
#     if detection_ratio < 0.1:
#         return "No human detected in most frames. Please ensure you're in front of the camera."
#     if score == 0:
#         return "Action not recognized. Please try again."
#     elif 1 <= score <= 10:
#         return "It is very hard to find the action."
#     elif 11 <= score <= 40:
#         return "Child is finding it hard to perform the action. Please repeat the action as shown in the video and try again."
#     elif 41 <= score <= 79:
#         return "Child is performing at a medium level. Keep practicing to improve."
#     else:
#         return "Child is performing well! The action is easy for them."

# def get_diff_level(score, detection_ratio):
#     if detection_ratio < 0.1:
#         return "No detection"
#     if score == 0:
#         return "No level"
#     elif 1 <= score <= 40:
#         return "Easy"
#     elif 41 <= score <= 79:
#         return "Medium"
#     else:
#         return "Hard"

# @video_bp.route("/action/predict", methods=["POST"])
# def predict():
#     if "file" not in request.files:
#         return jsonify({"error": "No file uploaded"}), 400
    
#     file = request.files["file"]
#     actual_class = request.form.get("actual_class", "").strip()
    
#     if not actual_class:
#         return jsonify({"error": "No actual class provided"}), 400
    
#     video_path = "temp_video.mp4"
#     file.save(video_path)
    
#     keypoints, frames_with_keypoints, total_frames = extract_keypoints(video_path)
#     detection_ratio = frames_with_keypoints / total_frames if total_frames > 0 else 0

#     if detection_ratio < 0.1 or len(keypoints) == 0:
#         os.remove(video_path)
#         return jsonify({
#             "predictions": [],
#             "percentage": "0",
#             "message": get_message(0, detection_ratio),
#             "level": get_diff_level(0, detection_ratio),
#             "predicted_action": "none",
#             "actual_class": actual_class,
#             "receivedPredictions": {},
#             "detection_ratio": f"{detection_ratio:.2f}"
#         })

#     keypoints = torch.tensor(np.expand_dims(keypoints, axis=0), dtype=torch.float32)
    
#     easy_actions = {"catch": 0, "stand": 1, "walk": 2}
#     medium_actions = {"run": 0, "throw": 1}
#     hard_actions = {"dribble": 0, "handstand": 1, "kick-ball": 2}
    
#     if actual_class in easy_actions:
#         model = easy_model
#         label_to_int = easy_actions
#         endpoint = "easy"
#     elif actual_class in medium_actions:
#         model = medium_model
#         label_to_int = medium_actions
#         endpoint = "medium"
#     elif actual_class in hard_actions:
#         model = hard_model
#         label_to_int = hard_actions
#         endpoint = "hard"
#     else:
#         os.remove(video_path)
#         return jsonify({"error": "Invalid action class"}), 400

#     with torch.no_grad():
#         prediction = model(keypoints)
#         probabilities = torch.softmax(prediction, dim=1)
#         predicted_label = torch.argmax(prediction, dim=1).item()
    
#     int_to_label = {v: k for k, v in label_to_int.items()}
#     predicted_action = int_to_label[predicted_label]

#     if predicted_action != actual_class:
#         score = 1
#     else:
#         score = probabilities[0][predicted_label].item() * 100
    
#     message = get_message(int(round(score)), detection_ratio)
#     level = get_diff_level(int(round(score)), detection_ratio)
#     class_probabilities = {int_to_label[i]: float(probabilities[0][i].item()) for i in range(probabilities.size(1))}

#     os.remove(video_path)

#     return jsonify({
#         "predictions": [{"prediction": predicted_action, "confidence": class_probabilities.get(predicted_action, 0)}],
#         "percentage": f"{score:.0f}",
#         "message": message,
#         "level": level,
#         "predicted_action": predicted_action,
#         "actual_class": actual_class,
#         "receivedPredictions": class_probabilities,
#         "detection_ratio": f"{detection_ratio:.2f}",
#         "endpoint": endpoint
#     })

easy_classes = 3
medium_classes = 2
hard_classes = 3

class ActionRecognitionModel(torch.nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(ActionRecognitionModel, self).__init__()
        self.lstm1 = torch.nn.LSTM(input_size, hidden_size, batch_first=True, bidirectional=True)
        self.lstm2 = torch.nn.LSTM(hidden_size * 2, hidden_size // 2, batch_first=True, bidirectional=True)
        self.fc = torch.nn.Linear(hidden_size, num_classes)
    
    def forward(self, x):
        h_lstm1, _ = self.lstm1(x)
        h_lstm2, _ = self.lstm2(h_lstm1)
        h_lstm2 = h_lstm2[:, -1, :]
        out = self.fc(h_lstm2)
        return out

easy_model = ActionRecognitionModel(input_size=99, hidden_size=64, num_classes=easy_classes)
easy_model.load_state_dict(torch.load("models/easy_model.pth"))
easy_model.eval()

medium_model = ActionRecognitionModel(input_size=99, hidden_size=64, num_classes=medium_classes)
medium_model.load_state_dict(torch.load("models/med_model.pth"))
medium_model.eval()

hard_model = ActionRecognitionModel(input_size=99, hidden_size=64, num_classes=hard_classes)
hard_model.load_state_dict(torch.load("models/hard_action_model.pth"))
hard_model.eval()

mp_pose = mp.solutions.pose

def extract_keypoints(video_path):
    pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
    cap = cv2.VideoCapture(video_path)
    keypoints_list = []
    frames_with_keypoints = 0
    total_frames = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        total_frames += 1
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)
        if results.pose_landmarks:
            frames_with_keypoints += 1
            keypoints = np.array([[lm.x, lm.y, lm.z] for lm in results.pose_landmarks.landmark]).flatten()
            keypoints_list.append(keypoints)
    
    cap.release()
    return np.array(keypoints_list), frames_with_keypoints, total_frames

def get_message(score, detection_ratio):
    if detection_ratio < 0.1:
        return "No human detected in most frames. Please ensure you're in front of the camera."
    if score == 0:
        return "Action not recognized. Please try again."
    elif 1 <= score <= 10:
        return "It is very hard to find the action."
    elif 11 <= score <= 40:
        return "Child is finding it hard to perform the action. Please repeat the action as shown in the video and try again."
    elif 41 <= score <= 79:
        return "Child is performing at a medium level. Keep practicing to improve."
    else:
        return "Child is performing well! The action is easy for them."

# def get_diff_level(score, detection_ratio):
#     if detection_ratio < 0.1:
#         return "No detection"
#     if score == 0:
#         return "No level"
#     elif 1 <= score <= 40:
#         return "Easy"
#     elif 41 <= score <= 79:
#         return "Medium"
#     else:
#         return "Hard"
def get_diff_level(score, detection_ratio):
    if detection_ratio < 0.1:
        return "No detection"
    if score == 0:
        return "No level"
    elif 1 <= score <= 40:
        return "Easy"
    elif 41 <= score <= 79:
        return "Medium"
    else:
        return "Hard"


# @app.route("/action/predict", methods=["POST"])
@video_bp.route("/action/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    actual_class = request.form.get("actual_class", "").strip()
    
    if not actual_class:
        return jsonify({"error": "No actual class provided"}), 400
    
    video_path = "temp_video.mp4"
    file.save(video_path)
    
    keypoints, frames_with_keypoints, total_frames = extract_keypoints(video_path)
    detection_ratio = frames_with_keypoints / total_frames if total_frames > 0 else 0
    
    if detection_ratio < 0.1:
        return jsonify({
            "predictions": [],
            "percentage": "0",
            "message": get_message(0, detection_ratio),
            "level": get_diff_level(0, detection_ratio),
            "predicted_action": "none",
            "actual_class": actual_class,
            "receivedPredictions": {},
            "detection_ratio": f"{detection_ratio:.2f}"
        })
    
    if len(keypoints) == 0:
        return jsonify({"error": "No keypoints detected"}), 400
    
    keypoints = torch.tensor(np.expand_dims(keypoints, axis=0), dtype=torch.float32)
    
    easy_actions = {"catch": 0, "stand": 1, "walk": 2}
    medium_actions = {"run": 0, "throw": 1}
    hard_actions = {"dribble": 0, "handstand": 1, "kick-ball": 2}
    
    if actual_class in easy_actions:
        model = easy_model
        label_to_int = easy_actions
        endpoint = "easy"
    elif actual_class in medium_actions:
        model = medium_model
        label_to_int = medium_actions
        endpoint = "medium"
    elif actual_class in hard_actions:
        model = hard_model
        label_to_int = hard_actions
        endpoint = "hard"
    else:
        return jsonify({"error": "Invalid action class"}), 400
    
    with torch.no_grad():
        prediction = model(keypoints)
        probabilities = torch.softmax(prediction, dim=1)
        predicted_label = torch.argmax(prediction, dim=1).item()
    
    int_to_label = {v: k for k, v in label_to_int.items()}
    predicted_action = int_to_label[predicted_label]
    
    if predicted_action != actual_class:
        score = 1 
    else:
        score = probabilities[0][predicted_label].item() * 100
    
    message = get_message(int(round(score)), detection_ratio)
    level = get_diff_level(int(round(score)), detection_ratio)
    class_probabilities = {int_to_label[i]: float(probabilities[0][i].item()) for i in range(probabilities.size(1))}
    
    os.remove(video_path)
    print(class_probabilities)
    return jsonify({
        "predictions": [{"prediction": predicted_action, "confidence": class_probabilities.get(predicted_action, 0)}],
        "percentage": f"{score:.0f}",
        "message": message,
        "level": level,
        "predicted_action": predicted_action,
        "actual_class": actual_class,
        "receivedPredictions": class_probabilities,
        "detection_ratio": f"{detection_ratio:.2f}",
        "endpoint": endpoint
    })
