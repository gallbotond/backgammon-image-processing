import cv2

# Open the camera
cap = cv2.VideoCapture(2)

while True:
    # Capture a frame
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break   