import os
import cv2

import util.select_rectangle as select_rectangle
import position_scan

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

img = select_rectangle.run('./test627450.jpg')
position_scan.run(img)

# save the warped image
cv2.imwrite('warped.jpg', img)