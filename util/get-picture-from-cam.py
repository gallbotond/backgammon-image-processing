import cv2

# Open the camera
cap = cv2.VideoCapture(1)

# Capture a frame
ret, frame = cap.read()

# Save the frame
cv2.imwrite('test.jpg', frame)