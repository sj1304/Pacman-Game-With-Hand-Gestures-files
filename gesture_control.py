# gesture_control.py
import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Initialize mediapipe hand solution once
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Start webcam
cap = cv2.VideoCapture(0)

def get_direction():
    """
    Captures one frame from webcam, returns 'left','right','up','down' or None
    depending on thumb tip position.
    """
    ret, frame = cap.read()
    if not ret:
        return None

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    h, w, c = frame.shape
    direction = None

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            # thumb tip = landmark 4
            x = int(handLms.landmark[4].x * w)
            y = int(handLms.landmark[4].y * h)

            

            # Decide direction based on region
            
            if x < w * 0.33:
                direction = 'left'
            elif x > w * 0.66:
                direction = 'right'
            elif y < h * 0.33:
                direction = 'up'
            elif y > h * 0.66:
                direction = 'down'

            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

   
    cv2.imshow("Gesture Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return 'quit'

    return direction

def release():
    cap.release()
    cv2.destroyAllWindows()
