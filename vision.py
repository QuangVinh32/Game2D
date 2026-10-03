import cv2
import mediapipe as mp
import pydirectinput


def play():
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands

    # Webcam input:
    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(
        model_complexity = 0,
        min_detection_confidence = 0.5,
        min_tracking_confidence = 0.5) as hands:
      while cap.isOpened():
        success, image = cap.read()
        if not success:
          print("Ignoring empty camera frame.")
          # If loading a video, use 'break' instead of 'continue'.
          continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
          for hand_landmarks in results.multi_hand_landmarks:
            print(hand_landmarks.landmark[9].x, hand_landmarks.landmark[9].y)
            pydirectinput.moveTo(int((0.5 - hand_landmarks.landmark[9].x) * 3200),
                                 int(hand_landmarks.landmark[9].y * 2000))

            if hand_landmarks.landmark[8].y > hand_landmarks.landmark[7].y and hand_landmarks.landmark[12].y > \
                    hand_landmarks.landmark[11].y and hand_landmarks.landmark[16].y > hand_landmarks.landmark[15].y \
                    and hand_landmarks.landmark[20].y > hand_landmarks.landmark[19].y:
                pydirectinput.mouseDown()
            elif hand_landmarks.landmark[8].y < hand_landmarks.landmark[7].y and hand_landmarks.landmark[12].y > \
                    hand_landmarks.landmark[11].y and hand_landmarks.landmark[16].y > hand_landmarks.landmark[15].y \
                    and hand_landmarks.landmark[20].y > hand_landmarks.landmark[19].y:
                pydirectinput.press('left')
            elif hand_landmarks.landmark[8].y > hand_landmarks.landmark[7].y and hand_landmarks.landmark[12].y < \
                    hand_landmarks.landmark[11].y and hand_landmarks.landmark[16].y > hand_landmarks.landmark[15].y \
                    and hand_landmarks.landmark[20].y > hand_landmarks.landmark[19].y:
                pydirectinput.press('space')
            elif hand_landmarks.landmark[8].y > hand_landmarks.landmark[7].y and hand_landmarks.landmark[12].y > \
                    hand_landmarks.landmark[11].y and hand_landmarks.landmark[16].y > hand_landmarks.landmark[15].y \
                    and hand_landmarks.landmark[20].y < hand_landmarks.landmark[19].y:
                pydirectinput.press('right')
            else:
                pydirectinput.mouseUp()

            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('Demo MediaPipe Hands', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
          break
    cap.release()

if __name__ == '__main__':
    play()