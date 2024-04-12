import cv2
import numpy as np

def run(img):
    thresholded = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    dist_map = cv2.distanceTransform(thresholded, cv2.DIST_L2, 3)

    cv2.normalize(dist_map, dist_map, 0, 1.0, cv2.NORM_MINMAX)
    # cv2.imshow('Distance Transform', dist_map)
    # cv2.imwrite(f'dist_map.jpg', (dist_map * 255).astype(np.uint8))  # Convert dist_map to uint8 before saving
    # cv2.waitKey(0)

    # find the ultimate eroded points
    _, sure_fg = cv2.threshold(dist_map, 0.7*dist_map.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)
    # cv2.imshow('Sure Foreground', sure_fg)
    # cv2.imwrite('sure_fg.jpg', sure_fg)
    # cv2.waitKey(0)

    contours, _ = cv2.findContours(sure_fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filtered_contours = [
        contour for contour in contours if cv2.contourArea(contour) > 0 and cv2.contourArea(contour) < 200
    ]

    # draw the contours
    cv2.drawContours(img, filtered_contours, -1, (0, 255, 0), 2)
    # cv2.imshow('Contours', img)
    # cv2.imwrite('contours.jpg', img)
    # cv2.waitKey(0)

    centers = []
    for contour in filtered_contours:
        moments = cv2.moments(contour)
        center = (
            int(moments["m10"] / moments["m00"]),
            int(moments["m01"] / moments["m00"]),
        )
        centers.append(center)

    return centers