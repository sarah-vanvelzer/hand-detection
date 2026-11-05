import cv2
import mediapipe as mp
import pyautogui
import math

def hand_gesture_mouse_control():
    cam = cv2.VideoCapture(1)
    mp_hands = mp.solutions.hands.Hands(max_num_hands=1)
    mp_drawing = mp.solutions.drawing_utils

    screen_width, screen_height = pyautogui.size()
    pyautogui.PAUSE = 0
    margin = 5

    clicking = False
    pinch_threshold = 0.06
    prev_x, prev_y = 0, 0
    smoothing = 0.2

    while cam.isOpened():
        success, frame = cam.read()
        if not success:
            continue

        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = mp_hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS
                )

                # Index fingertip:
                index_finger = hand_landmarks.landmark[8]
                x = int(index_finger.x * frame.shape[1])
                y = int(index_finger.y * frame.shape[0])

                screen_x = min(max(screen_width * index_finger.x, margin), screen_width - margin)
                screen_y = min(max(screen_height * index_finger.y, margin), screen_height - margin)
                smooth_x = prev_x + (screen_x - prev_x) * smoothing
                smooth_y = prev_y + (screen_y - prev_y) * smoothing
                pyautogui.moveTo(smooth_x, smooth_y)
                prev_x, prev_y = smooth_x, smooth_y

                # Add decoration to fingertip:
                cv2.circle(frame, (x, y), 10, (182, 85, 242), -1) # Uses BGR

                # Pinch detection:
                thumb_tip = hand_landmarks.landmark[4]
                dx = thumb_tip.x - index_finger.x
                dy = thumb_tip.y - index_finger.y
                distance = math.sqrt(dx*dx + dy*dy)

                if distance < pinch_threshold and not clicking:
                    pyautogui.click()
                    clicking = True
                elif distance >= pinch_threshold and clicking:
                    clicking = False

        cv2.imshow("Hand Gesture Mouse", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"): # Quit with the 'q' key
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    hand_gesture_mouse_control()