import cv2
import mediapipe as mp
import pyautogui
import time

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)

prev_y = None
last_scroll_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Mirror view
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            # Use tip of index finger (landmark 8)
            finger_tip = hand.landmark[8]
            y_pos = finger_tip.y * frame.shape[0]  # Get Y coordinate

            thumb_tip = hand.landmark[4]
            thumb_x = thumb_tip.x * frame.shape[1]  # Get X coordinate of thumb

            # Scroll detection
            if prev_y is not None:
                dy = y_pos - prev_y
                now = time.time()

                if now - last_scroll_time > 1:  # 1 second delay
                    if dy < -40:  # Moved up fast
                        print("Finger moved UP - Scroll down")
                        pyautogui.press("down")
                        last_scroll_time = now
                    elif dy > 40:  # Moved down fast
                        print("Finger moved DOWN - Scroll up")
                        pyautogui.press("up")
                        last_scroll_time = now

            prev_y = y_pos

    else:
        prev_y = None

    cv2.imshow("Finger Scroll Control", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC key to quit
        break

cap.release()
cv2.destroyAllWindows()
