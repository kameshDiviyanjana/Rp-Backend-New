from flask import Blueprint, request, jsonify
import cv2
import os
from utils.video_processing import extract_skeleton_from_frame,prepare_sequence,normalize_keypoints
from models.action_recognition import action_model, label_encoder_classes
import numpy as np

video_bp = Blueprint("video_bp", __name__)

@video_bp.route('/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    input_path = f"uploads/{file.filename}"
    output_path = f"outputs/{os.path.splitext(file.filename)[0]}_processed.mp4"

    # Save uploaded file
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)
    file.save(input_path)

    # Process video
    cap = cv2.VideoCapture(input_path)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    sequence = []
    sequence_length = 30
    predictions = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        keypoints = extract_skeleton_from_frame(frame)
        if keypoints is not None:
            normalized_keypoints = normalize_keypoints(keypoints)
            sequence.append(normalized_keypoints.flatten())

            if len(sequence) == sequence_length:
                input_sequence = prepare_sequence(np.array(sequence), sequence_length=sequence_length)
                input_sequence = input_sequence.reshape(1, sequence_length, -1)

                prediction = action_model.predict(input_sequence)
                predicted_label = label_encoder_classes[np.argmax(prediction)]

                feedback = f"Detected action: {predicted_label}"
                predictions.append({"frame": len(predictions) + 1, "prediction": predicted_label, "feedback": feedback})

                cv2.putText(frame, f"Action: {predicted_label}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                sequence.pop(0)

        out.write(frame)

    cap.release()
    out.release()

    # Send predictions and video as response
    return jsonify({
        "predictions": predictions,
        "video_url": output_path
    })
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
