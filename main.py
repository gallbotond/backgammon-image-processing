import os
import cv2

import util.select_rectangle as select_rectangle
import position_scan
import get_dice_roi
import util.dice_counter as dice_counter

# select the last folder
folder = os.listdir('./data')[-1]

# get the full paths of the files
files = [os.path.join(f'./data/{folder}', file) for file in os.listdir(f'./data/{folder}')]

# sort the files by date created
files = sorted(files, key=os.path.getctime)

images = [file for file in files if file.endswith('.jpg')]

# for image in images:
#     img = select_rectangle.run(image)
#     # position_scan.run(img)
#     cv2.imshow("Corners and blobs", img)
#     cv2.waitKey(0)

img = select_rectangle.run('test650783.jpg')
original = img.copy()

# cv2.imwrite('selected.jpg', img)
cv2.imshow('selected', img)
cv2.waitKey(0)
green_centers, red_centers = position_scan.run(img)

for center in green_centers:
    cv2.circle(img, center, 2, (200, 200, 255), -1)
for center in red_centers:
    cv2.circle(img, center, 2, (0, 255, 0), -1)

cv2.imshow("positions", img)
cv2.waitKey(0)

rois = get_dice_roi.run(original)

for roi in rois:
    cv2.imshow('roi', roi)
    cv2.waitKey(0)

    # count the dice
    c = dice_counter.run(roi)
    print(c)

# # save the warped image
# cv2.imwrite('warped.jpg', img)