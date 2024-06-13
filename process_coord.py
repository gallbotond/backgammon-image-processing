import cv2
import numpy as np
import matplotlib.pyplot as plt

def run(im, points):
    # get the image shape
    h, w, _ = im.shape

    # initialize an array of 24 to 0
    positions = [0] * 24

    for position in points:
        # get the x and y coordinates
        x, y = position

        # point = {'x':23, 'y':45}
        # cv2.circle(im, (point['x'], point['y']), 5, (0, 255, 255), -1)

        xfrac = w / 12
        yfrac = h / 2

        xmax = 0
        ymax = 0

        imcopy = im.copy()


        for i in range(2):
            ymin = ymax
            ymax = ymin + yfrac 
            xmax = 0

            for j in range(12):
                xmin = xmax
                xmax = xmin + xfrac 
                # print(xmin, ymin, xmax, ymax)
                # draw squares on the image with changing colors
                if x >= xmin and x <= xmax and y >= ymin and y <= ymax:
                    cv2.rectangle(imcopy, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 2)
                    positions[i*12 + j] += 1
                # else:
                #     cv2.rectangle(imcopy, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (255, 0, 0), 2)

        # cv2.rectangle(imcopy, (0, 0), (33, 199), (255, 0, 0), 2)
        # cv2.rectangle(imcopy, (33, 199), (66, 398), (255, 0, 0), 2)

        cv2.imshow("positions", imcopy)
        cv2.waitKey(0)
        cv2.imwrite('positions.jpg', imcopy)
        # positions = np.array(positions)
    return positions