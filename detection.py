import cv2
import mediapipe as mp
import controller

mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands
hands = mp_hand.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5, max_num_hands=1)
video = cv2.VideoCapture(0)

FRAME_CENTER_X = int(video.get(3) / 2)
FRAME_CENTER_Y = int(video.get(4) / 2)

# Servo mappings
SERVO_LATERAL = 1  # Z-axis rotation (1st Servo)
SERVO_VERTICAL_1 = 2  # X-axis rotation (2nd Servo)
SERVO_VERTICAL_2 = 3  # X-axis rotation (3rd Servo)
SERVO_VERTICAL_3 = 5  # X-axis rotation (5th Servo, with camera)

# Initial servo positions
servo_angles = {
    SERVO_LATERAL: 90,
    SERVO_VERTICAL_1: 90,
    SERVO_VERTICAL_2: 90,
    4: 90,
    SERVO_VERTICAL_3: 90,
    6: 90,
    7: 90
}

# Sensitivity controls
sensitivity = 250  # Higher = slower movement

while True:
    ret, image = video.read()
    if not ret:
        break
    
    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)
    
    # Draw center point
    cv2.circle(image, (FRAME_CENTER_X, FRAME_CENTER_Y), 5, (0, 0, 255), -1)

    if results.multi_hand_landmarks:
        hand_landmark = results.multi_hand_landmarks[0]
        lmList = [[id, int(lm.x * image.shape[1]), int(lm.y * image.shape[0])] for id, lm in enumerate(hand_landmark.landmark)]
        
        mp_draw.draw_landmarks(image, hand_landmark, mp_hand.HAND_CONNECTIONS)
        
        if lmList:
            hand_x, hand_y = lmList[9][1], lmList[9][2]  # Landmark 9 (MCP of index finger)

            # Calculate offsets
            lateral_offset = (FRAME_CENTER_X - hand_x) / sensitivity  # Reversed direction
            vertical_offset = (hand_y - FRAME_CENTER_Y) / sensitivity

            # Adjust servos dynamically
            servo_angles[SERVO_LATERAL] -= lateral_offset
            servo_angles[SERVO_VERTICAL_1] -= vertical_offset
            servo_angles[SERVO_VERTICAL_2] -= vertical_offset
            servo_angles[SERVO_VERTICAL_3] -= vertical_offset

            # Clamp angles between 0 and 180
            for servo in servo_angles:
                servo_angles[servo] = max(0, min(180, servo_angles[servo]))

            # Send updated angles to servos
            for servo, angle in servo_angles.items():
                controller.set_servo_angle(servo, angle)

            # Display debug info
            cv2.putText(image, f"Lateral: {servo_angles[SERVO_LATERAL]:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            cv2.putText(image, f"Vertical: {servo_angles[SERVO_VERTICAL_1]:.1f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    cv2.imshow("Frame", image)
    if cv2.waitKey(1) == 27:  # Press 'Esc' to exit
        break
    
video.release()
cv2.destroyAllWindows()
controller.cleanup()
