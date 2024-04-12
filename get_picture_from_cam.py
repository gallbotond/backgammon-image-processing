import cv2
import random

# Open the camera
cap = cv2.VideoCapture(1)

# Capture a frame
ret, frame = cap.read()

# Save the frame with a random name
cv2.imwrite('test' + str(random.randint(1, 999999)) + '.jpg', frame)