import cv2
import numpy as np
import mediapipe as mp

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

def extract_skeleton_from_frame(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)
    if results.pose_landmarks:
        keypoints = np.array([[lm.x, lm.y, lm.z] for lm in results.pose_landmarks.landmark])
        return keypoints
    return None

def normalize_keypoints(keypoints):
    reference_point = keypoints[0, :2]
    normalized = keypoints[:, :2] - reference_point
    return normalized

def prepare_sequence(sequence, sequence_length=30):
    if len(sequence) >= sequence_length:
        return sequence[:sequence_length]
    else:
        padding = np.zeros((sequence_length - len(sequence), sequence.shape[1]))
        return np.vstack((sequence, padding))

