import cv2
import numpy as np

from util import helpers as util
from util.blob_separation import run as blob_separation

def run(img):
    b, g, r = cv2.split(img)
    r_minus_g = cv2.subtract(r, g)
    g_minus_r = cv2.subtract(g, r)

    green_centers = blob_separation(r_minus_g)
    red_centers = blob_separation(g_minus_r)

    for center in green_centers:
        cv2.circle(img, center, 2, (200, 200, 255), -1)
    for center in red_centers:
        cv2.circle(img, center, 2, (0, 255, 0), -1)

    cv2.imshow("Corners and blobs", img)
    cv2.waitKey(0)

# run(cv2.imread('./test627450.jpg'))