import cv2
import numpy as np

# Load the images
colored_img = cv2.imread('./selected.jpg')
# green_img = cv2.imread('green_image.jpg')

# Convert the colored image to HSV color space
hsv_img = cv2.cvtColor(colored_img, cv2.COLOR_BGR2HSV)

# Define the lower and upper range for green color in HSV space
lower_green = np.array([35, 100, 100])
upper_green = np.array([85, 255, 255])

# Create a mask where green pixels in the colored image are white and all other pixels are black
mask = cv2.inRange(hsv_img, lower_green, upper_green)

# Apply the mask to the colored image
green_areas = cv2.bitwise_and(colored_img, colored_img, mask=mask)

# Display the resulting image
cv2.imshow('Green Areas', green_areas)
cv2.imwrite('green_areas.jpg', green_areas)
cv2.waitKey(0)
cv2.destroyAllWindows()