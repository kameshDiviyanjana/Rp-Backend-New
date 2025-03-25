from flask import Blueprint, Response
import cv2
import mediapipe as mp
import time
import math
from collections import Counter

finger_counting_bp = Blueprint('finger_counting_bp', __name__)

# Camera setup
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Initialize variables
pTime = 0
tipIds = [4, 8, 12, 16, 20]  # Fingertip landmark IDs
mcpIds = [2, 5, 9, 13, 17]   # MCP joint landmark IDs
pipIds = [3, 6, 10, 14, 18]  # PIP joint landmark IDs

# Global variables
latest_finger_count = 0
latest_confidence = 0.0

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

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
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
    """Adjust brightness and contrast without converting to grayscale."""
    alpha = 1.5  # Contrast control (1.0-3.0)
    beta = 20    # Brightness control (0-100)
    adjusted = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    return adjusted

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

# History for smoothing and confidence
finger_count_history = []
HISTORY_SIZE = 10

def calculate_confidence(history):
    """Calculate confidence based on the frequency of the most common count."""
    if not history:
        return 0.0
    counter = Counter(history)
    most_common_count, frequency = counter.most_common(1)[0]
    confidence = frequency / len(history)  # Proportion of the most frequent count
    return confidence

def generate_finger_counting_frames():
    global pTime, latest_finger_count, latest_confidence, finger_count_history
    while True:
        success, img = cap.read()
        if not success:
            break

        # Preprocess image without grayscale conversion
        img = preprocess_image(img)
        img = detector.findHands(img)

        totalFingers = 0
        debug_text = []
        hand_count = min(2, len(detector.results.multi_hand_landmarks) if detector.results.multi_hand_landmarks else 0)

        for handNo in range(hand_count):
            lmList = detector.findPosition(img, handNo=handNo, draw=False)
            handLabel = detector.getHandLabel(handNo)

            if len(lmList) != 0:
                fingers = []
                # Thumb detection
                thumb_tip = (lmList[tipIds[0]][1], lmList[tipIds[0]][2])
                index_mcp = (lmList[mcpIds[1]][1], lmList[mcpIds[1]][2])
                wrist = (lmList[0][1], lmList[0][2])
                thumb_to_index_mcp = calculate_distance(thumb_tip, index_mcp)
                thumb_to_wrist = calculate_distance(thumb_tip, wrist)
                index_mcp_to_wrist = calculate_distance(index_mcp, wrist)
                normalized_thumb_dist = thumb_to_index_mcp / index_mcp_to_wrist
                if normalized_thumb_dist > 0.5:
                    fingers.append(1)
                else:
                    fingers.append(0)

                # Other fingers
                for id in range(1, 5):
                    mcp = (lmList[mcpIds[id]][1], lmList[mcpIds[id]][2])
                    pip = (lmList[pipIds[id]][1], lmList[pipIds[id]][2])
                    tip = (lmList[tipIds[id]][1], lmList[tipIds[id]][2])
                    angle = calculate_angle(mcp, pip, tip)
                    if angle > 140:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                hand_fingers = fingers.count(1)
                totalFingers += hand_fingers
                finger_names = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
                up_fingers = [finger_names[i] for i in range(5) if fingers[i] == 1]
                debug_text.append(f"Hand {handNo+1} ({handLabel}): {', '.join(up_fingers) if up_fingers else 'None'}")

        # Update history
        finger_count_history.append(totalFingers)
        if len(finger_count_history) > HISTORY_SIZE:
            finger_count_history.pop(0)

        # Smoothed finger count (most frequent) and confidence (frequency-based)
        if finger_count_history:
            smoothed_count = Counter(finger_count_history).most_common(1)[0][0]
            smoothed_confidence = calculate_confidence(finger_count_history)
        else:
            smoothed_count = totalFingers
            smoothed_confidence = 0.0

        # Update global variables
        latest_finger_count = smoothed_count
        latest_confidence = smoothed_confidence

        # Display on frame
        cTime = time.time()
        fps = 1 / (cTime - pTime) if (cTime - pTime) != 0 else 0
        pTime = cTime
        
        cv2.putText(img, f'Fingers: {smoothed_count}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        cv2.putText(img, f'Conf: {smoothed_confidence:.2f}', (20, 110), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)
        cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        for i, text in enumerate(debug_text):
            cv2.putText(img, text, (20, 150 + i*40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)

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