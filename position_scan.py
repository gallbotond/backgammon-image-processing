import cv2
import numpy as np

from util import helpers as util
from util.blob_separation import run as blob_separation

def run(img):
    # src = './data/2024-03-17 17_14_00/frame_9340.jpg'
    # img = cv2.imread(src)
    # downscale_by = 8
    # img = cv2.resize(img, (img.shape[1] // downscale_by, img.shape[0] // downscale_by))
    clear = img.copy()

    # detect corners
    # corners = util.detect_rectangle(img).reshape(4, 2)
    # rect = np.zeros((4, 2), dtype = "float32")
    # s = corners.sum(axis = 1)
    # rect[0] = corners[np.argmin(s)]
    # rect[2] = corners[np.argmax(s)]
    # diff = np.diff(corners, axis = 1)
    # rect[1] = corners[np.argmin(diff)]
    # rect[3] = corners[np.argmax(diff)]
    # print(rect)
    # (tl, tr, br, bl) = rect / 1.4
    # img_with_corners = util.draw_points(img, tl, tr, br, bl)

    # Get the dimensions of the image
    height, width, channels = img.shape
    img_with_corners = util.draw_points(img, (0, 0), (width, 0), (width, height), (0, height))

    # cv2.imshow("Corners", img)
    # cv2.waitKey(0)

    # detect blobs
    min_area = 0
    max_area = 200
    b, g, r = cv2.split(clear)
    r_minus_g = util.overflow_subtract(r, g)
    g_minus_r = util.overflow_subtract(g, r)
    cv2.imshow("Red", r_minus_g)
    cv2.imshow("Green", g_minus_r)
    # green_centers = util.blob_detect_center(r_minus_g, min_area, max_area, 6)
    # red_centers = util.blob_detect_center(g_minus_r, min_area, max_area, 6)
    green_centers = blob_separation(r_minus_g, True, False, 20)
    red_centers = blob_separation(g_minus_r, True, True)
    for center in red_centers:
        cv2.circle(img_with_corners, center, 2, (0, 0, 255), -1)
    for center in green_centers:
        cv2.circle(img_with_corners, center, 2, (0, 255, 0), -1)

    cv2.imshow("Corners and blobs", img_with_corners)
    cv2.waitKey(0)