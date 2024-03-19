import cv2
import numpy as np

def run(img, debug, invert=False, thresh_low=30):
    thresholded = cv2.threshold(img, thresh_low, 255, cv2.THRESH_BINARY)[1]
    if debug:
        cv2.imshow('Thresholded Image', thresholded)
        cv2.waitKey(0)
    gray = cv2.cvtColor(thresholded, cv2.COLOR_BGR2GRAY)
    
    if invert: inverted = cv2.bitwise_not(gray)
    else: inverted = gray

    if debug:
        cv2.imshow('Inverted Image', inverted)
        cv2.waitKey(0)

    # calculate the eucledian distance map
    ret, thresh = cv2.threshold(invert, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    dist_map = cv2.distanceTransform(thresh, cv2.DIST_L2, 3)
    cv2.normalize(dist_map, dist_map, 0, 1.0, cv2.NORM_MINMAX)

    if debug:
        cv2.imshow('Distance Map', dist_map)
        cv2.waitKey(0)

    # find the ultimate eroded points
    _, sure_fg = cv2.threshold(dist_map, 0.7*dist_map.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)
    if debug: cv2.imshow('Sure FG', sure_fg)

    contours, _ = cv2.findContours(sure_fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if debug: 
        for contour in contours:
             print(cv2.contourArea(contour))
    filtered_contours = [
        contour for contour in contours if cv2.contourArea(contour) > 0 and cv2.contourArea(contour) < 200
    ]
    centers = []
    for contour in filtered_contours:
        moments = cv2.moments(contour)
        center = (
            int(moments["m10"] / moments["m00"]),
            int(moments["m01"] / moments["m00"]),
        )
        centers.append(center)

    if debug:
        for center in centers:
            cv2.circle(img, center, 5, (0, 255, 0), -1)

        cv2.imshow('Detected Points', img)
        cv2.waitKey(0)
        # save the result
        cv2.imwrite('sure_fg.jpg', sure_fg)
        cv2.destroyAllWindows()

    return centers