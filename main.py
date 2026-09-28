import cv2
import mediapipe as mp
import math 
import pyautogui 

cap=cv2.VideoCapture(0)
frame_width=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

button_name = "JUMP"
button_x = 50
button_y = 50
button_width = 140
button_height = 70

def draw_button(frame):
    top_left = (button_x, button_y)
    bottom_right = (button_x + button_width, button_y + button_height)

    cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), -1)
    cv2.putText(frame,button_name,(button_x+25,button_y+45),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)

# Mediapipe Hands 
mp_hands=mp.solutions.hands
mp_drawing_tool=mp.solutions.drawing_utils 

hands=mp_hands.Hands(max_num_hands=1)

# Pinch detection
pinch_pressed=False 

def detect_pinch(frame,hand_landmarks):
    global pinch_pressed

    "Index finger tip and thumb finger tip"
    # Index finger top
    index_tip=hand_landmarks.landmark[8]
    # Thumb tip
    thumb_tip=hand_landmarks.landmark[4]

    "Coords to pixels" 
    index_x=int(index_tip.x * frame_width)
    index_y=int(index_tip.y * frame_height)

    thumb_tip_x=int(thumb_tip.x * frame_width)
    thumb_tip_y=int(thumb_tip.y * frame_height)

    "Distance formula (distance from index to thumb calculation)"
    distance=math.sqrt(
        (index_x-thumb_tip_x) ** 2 +
        (index_y - thumb_tip_y) ** 2 
    )

    inside_button=False 
    if button_x <= index_x <= button_x+button_width:
        if button_y <=index_y <=button_y+button_height:
            inside_button=True 

    pinch_threshold=40

    "Trigger the jump"
    if distance < pinch_threshold and inside_button:
        if not pinch_pressed:
            pyautogui.press("space") # Trigger space  - reasearched how to trigger
            pinch_pressed=True
    else:
        pinch_pressed=False 

while True:
    ret,frame=cap.read()

    if not ret:
        break 

    # Flip the camera - mirror
    frame=cv2.flip(frame,1)

    # BGR To RGB 
    rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    # Detect hands
    results=hands.process(rgb) # Process the rgb frame 
    if results.multi_hand_landmarks:
        hand_landmarks=results.multi_hand_landmarks[0] #get first hand detected

        "Draw the hand"
        mp_drawing_tool.draw_landmarks(frame,hand_landmarks,mp_hands.HAND_CONNECTIONS)

        detect_pinch(frame,hand_landmarks) # Detect the pinch

    # Draw JUMP button
    draw_button(frame)

    # Display the window
    cv2.imshow("T-Rex Gesture Controller",frame)

    # Exit by pressing esc
    key = cv2.waitKey(1) & 0xff 
    if key==27:
        break 

cap.release()
hands.close()
cv2.destroyAllWindows()



