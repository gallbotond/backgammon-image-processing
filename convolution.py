import cv2
import numpy as np

im = cv2.imread('./selected.jpg')
cv2.imshow('image', im)
cv2.waitKey(0)

# Create a 20x20 pixel image with 3 color channels (BGR), filled with green color
green_img = np.full((25, 25, 3), (0, 255, 0), dtype=np.uint8)

# Save the image
# cv2.imwrite('green_img.jpg', green_img)
cv2.imshow('green_img', green_img)
cv2.waitKey(0)

# convert the image to grayscale
im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
green_img = cv2.cvtColor(green_img, cv2.COLOR_BGR2GRAY)

# go through the image in 10px increments and multiply the pixel values using convolution
for i in range(0, im.shape[0], 5):
    for j in range(0, im.shape[1], 5):
        patch = im[i:i+25, j:j+25]  # Extract the image patch
        if patch.shape == green_img.shape:  # Check if patch size matches green_img size
            im[i:i+25, j:j+25] = cv2.multiply(patch, green_img)  # Perform multiplication
            # normalize the value from a range of 0-65025 to 0-255
            im[i:i+25, j:j+25] = cv2.normalize(im[i:i+25, j:j+25], None, 0, 255, cv2.NORM_MINMAX)
        else:
            print("Patch size does not match green_img size.")

cv2.imshow('image', im)
cv2.imwrite('green_img_conv.jpg', im)
cv2.waitKey(0)

cv2.destroyAllWindows()