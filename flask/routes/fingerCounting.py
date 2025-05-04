
from flask import Blueprint, Response
import cv2  
import mediapipe as mp  
import time  
import math 
import numpy as np
from collections import Counter  

finger_counting_bp = Blueprint('finger_counting_bp', __name__)  

# Camera setup
wCam, hCam = 640, 480  
cap = cv2.VideoCapture(0) 
cap.set(3, wCam)
cap.set(4, hCam) 

# Initialize variables
pTime = 0 
tipIds = [4, 8, 12, 16, 20]  # Fingertips
mcpIds = [2, 5, 9, 13, 17]   # MCP joints
pipIds = [3, 6, 10, 14, 18]  # PIP joints

# Global variables
latest_finger_count = 0  
latest_confidence = 0.0 
current_state = 0  # FSM initial state: 0 fingers
HISTORY_SIZE = 10  # Frame buffer size
finger_count_history = []

# Hand Detector Class
class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.75, trackCon=0.5):
        self.mode = mode 
        self.maxHands = maxHands  
        self.detectionCon = detectionCon  
        self.trackCon = trackCon  
        self.mpHands = mp.solutions.hands 
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,  
            max_num_hands=self.maxHands, 
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils 
        self.results = None  

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks and draw: 
            for handLms in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img  

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results and self.results.multi_hand_landmarks and handNo < len(self.results.multi_hand_landmarks):
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return lmList

    def getHandLabel(self, handNo=0):
        if self.results and self.results.multi_handedness and handNo < len(self.results.multi_handedness):
            return self.results.multi_handedness[handNo].classification[0].label  
        return None  

# Initialize detector
detector = handDetector(detectionCon=0.75, maxHands=2)    

def preprocess_image(img):
    """Enhance image for dark environments and edge detection."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    alpha = 2.0
    beta = 30
    adjusted = cv2.convertScaleAbs(enhanced, alpha=alpha, beta=beta)
    blurred = cv2.GaussianBlur(adjusted, (5, 5), 0)
    return blurred, img

def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def calculate_angle(point1, point2, point3):
    vector1 = [point1[0] - point2[0], point1[1] - point2[1]]  
    vector2 = [point3[0] - point2[0], point3[1] - point2[1]]  
    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
    mag1 = math.sqrt(vector1[0]**2 + vector1[1]**2)
    mag2 = math.sqrt(vector2[0]**2 + vector2[1]**2)  
    if mag1 == 0 or mag2 == 0: 
        return 0
    cos_angle = dot_product / (mag1 * mag2) 
    cos_angle = max(min(cos_angle, 1), -1)  
    return math.degrees(math.acos(cos_angle)) 

def calculate_confidence(history):
    if not history: 
        return 0.0
    counter = Counter(history)  
    most_common_count, frequency = counter.most_common(1)[0]  
    return frequency / len(history)

def edge_based_finger_count(img_gray, lmList):
    """Count fingers using edge detection and contour analysis."""
    edges = cv2.Canny(img_gray, 50, 150)
    
    if len(lmList) == 0:
        # No landmarks: Check for hand-like structure
        edge_density = np.sum(edges) / (edges.shape[0] * edges.shape[1])
        if edge_density < 10:  # Low edge density = no hand
            return 0
        
        # Find contours in full image
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        finger_count = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 100:  # Filter small noise
                x, y, w, h = cv2.boundingRect(cnt)
                aspect_ratio = w / h if h > 0 else 0
                if 0.2 < aspect_ratio < 1.0 and h > 20:  # Finger-like shape
                    finger_count += 1
        return finger_count
    
    # Landmarks present: Focus on hand region
    min_x = max(0, min([lm[1] for lm in lmList]) - 30)
    max_x = min(img_gray.shape[1], max([lm[1] for lm in lmList]) + 30)
    min_y = max(0, min([lm[2] for lm in lmList]) - 30)
    max_y = min(img_gray.shape[0], max([lm[2] for lm in lmList]) + 30)
    
    roi = edges[min_y:max_y, min_x:max_x]
    if roi.size == 0:
        return 0
    
    # Find contours in hand region
    contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    finger_count = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 50:  # Minimum area for a finger
            x, y, w, h = cv2.boundingRect(cnt)
            aspect_ratio = w / h if h > 0 else 0
            if 0.2 < aspect_ratio < 1.0 and h > 15:  # Finger-like shape
                finger_count += 1
    
    return finger_count
    

def generate_finger_counting_frames():
    global pTime, latest_finger_count, latest_confidence, finger_count_history, current_state
    while True:
        success, img = cap.read()  
        if not success: 
            break

        img_gray, img = preprocess_image(img)  
        img = detector.findHands(img)  
        totalFingers = 0
        edge_fingers = 0
        debug_text = [] 
        hand_count = min(2, len(detector.results.multi_hand_landmarks) if detector.results.multi_hand_landmarks else 0) 

        if hand_count > 0:  
            for handNo in range(hand_count):  
                lmList = detector.findPosition(img, handNo=handNo, draw=False)  
                handLabel = detector.getHandLabel(handNo)

                if len(lmList) != 0: 
                    fingers = [0] * 5  
                    wrist = (lmList[0][1], lmList[0][2])
                    index_mcp = (lmList[mcpIds[1]][1], lmList[mcpIds[1]][2])
                    hand_size = calculate_distance(wrist, index_mcp)

                    # Thumb detection
                    thumb_tip = (lmList[tipIds[0]][1], lmList[tipIds[0]][2])
                    thumb_to_index_mcp = calculate_distance(thumb_tip, index_mcp)
                    thumb_to_wrist = calculate_distance(thumb_tip, wrist)
                    normalized_thumb_dist = thumb_to_index_mcp / hand_size
                    thumb_threshold = 0.4 + (hand_size / 200) * 0.2
                    if normalized_thumb_dist > thumb_threshold and thumb_to_wrist > hand_size * 0.6:
                        fingers[0] = 1

                    # Other fingers
                    orientation_angle = math.degrees(math.atan2(index_mcp[1] - wrist[1], index_mcp[0] - wrist[0]))
                    is_vertical = abs(orientation_angle) > 45 and abs(orientation_angle) < 135
                    for id in range(1, 5):
                        mcp = (lmList[mcpIds[id]][1], lmList[mcpIds[id]][2])  
                        pip = (lmList[pipIds[id]][1], lmList[pipIds[id]][2]) 
                        tip = (lmList[tipIds[id]][1], lmList[tipIds[id]][2])  
                        angle = calculate_angle(mcp, pip, tip)
                        tip_to_mcp_dist = calculate_distance(tip, mcp)
                        angle_threshold = 130 if is_vertical else 150
                        dist_threshold = hand_size * 0.5
                        if angle > angle_threshold and tip_to_mcp_dist > dist_threshold:
                            fingers[id] = 1

                    # Gesture rejection
                    palm_open = all([calculate_distance(wrist, (lmList[tipIds[i]][1], lmList[tipIds[i]][2])) > hand_size * 0.7 for i in range(1, 5)])
                    if palm_open and sum(fingers) == 0:
                        continue 

                    hand_fingers = sum(fingers)
                    totalFingers += hand_fingers 
                    finger_names = ["Thumb", "Index", "Middle", "Ring", "Pinky"] 
                    up_fingers = [finger_names[i] for i in range(5) if fingers[i] == 1]  
                    debug_text.append(f"Hand {handNo+1} ({handLabel}): Landmark: {hand_fingers}")  

                    # Edge-based counting per hand
                    edge_fingers += edge_based_finger_count(img_gray, lmList)
                    debug_text.append(f"Edge: {edge_fingers}")

            # Combine counts
            final_count = totalFingers
            if abs(totalFingers - edge_fingers) > 2:  # Larger discrepancy threshold
                final_count = edge_fingers if latest_confidence < 0.5 else totalFingers

            finger_count_history.append(final_count)
            if len(finger_count_history) > HISTORY_SIZE:
                finger_count_history.pop(0)

            base_confidence = calculate_confidence(finger_count_history)
            edge_agreement = 1.0 if abs(totalFingers - edge_fingers) <= 2 else 0.5
            smoothed_confidence = base_confidence * 0.6 + edge_agreement * 0.4

            proposed_count = final_count
            count_change = abs(proposed_count - current_state)
            if count_change <= 2 or smoothed_confidence > 0.9:
                current_state = proposed_count

            latest_finger_count = current_state
            latest_confidence = smoothed_confidence

        else:  # No hands detected
            edge_fingers = edge_based_finger_count(img_gray, [])
            if edge_fingers == 0:  # No significant edges = no hand
                totalFingers = 0
                finger_count_history.clear()  
                current_state = 0
                latest_finger_count = 0
                latest_confidence = 0.0
            else:
                totalFingers = edge_fingers
                finger_count_history.append(totalFingers)
                if len(finger_count_history) > HISTORY_SIZE:
                    finger_count_history.pop(0)
                base_confidence = calculate_confidence(finger_count_history)
                latest_finger_count = totalFingers
                latest_confidence = base_confidence * 0.5  # Lower confidence without landmarks
            debug_text.append(f"Edge (No Landmarks): {edge_fingers}")

        cTime = time.time()
        fps = 1 / (cTime - pTime) if (cTime - pTime) != 0 else 0  
        pTime = cTime
        cv2.putText(img, f'Conf: {latest_confidence:.2f}', (20, 110), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)
        cv2.putText(img, f'Fingers: {latest_finger_count}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        cv2.putText(img, f'State: {current_state}', (20, 150), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
        for i, text in enumerate(debug_text):
            cv2.putText(img, text, (20, 190 + i*40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)

        ret, buffer = cv2.imencode('.jpg', img) 
        frame = buffer.tobytes() 
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@finger_counting_bp.route('/feed')
def finger_counting_feed():
    return Response(generate_finger_counting_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@finger_counting_bp.route('/count')
def get_finger_count():
    global latest_finger_count, latest_confidence
    return {"finger_count": latest_finger_count, "confidence": round(latest_confidence, 2)}

def cleanup():
    cap.release()