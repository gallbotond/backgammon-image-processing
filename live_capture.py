import cv2

# Open the camera
cap = cv2.VideoCapture(1)
# cap = cv2.VideoCapture('http://192.168.0.138:4747/video')

# cv2.imshow('frame', cv2.imread('./img/im1.jpeg'))
# cv2.waitKey(0)

while True:
    # Capture a frame
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break