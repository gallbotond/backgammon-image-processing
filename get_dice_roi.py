import cv2
import numpy as np

def run(im):
    # find circles in the image
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=30, maxRadius=50)

    imcopy = im.copy()

    # draw circles
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            radius = i[2]
            cv2.circle(imcopy, center, radius, (0, 255, 0), 3)
            print(center, radius)

    cv2.imshow("circles", imcopy)
    cv2.imwrite('circles.jpg', imcopy)
    cv2.waitKey(0)

    # create a mask for the circles
    mask = np.zeros(im.shape[:2], dtype=np.uint8)
    for i in circles[0, :]:
        center = (i[0], i[1])
        radius = i[2]
        cv2.circle(mask, center, radius, (255), -1)

    cv2.imshow("Mask", mask)
    cv2.imwrite('mask.jpg', mask)
    cv2.waitKey(0)

    # apply the mask to the image
    masked = cv2.bitwise_and(im, im, mask=mask)
    cv2.imshow("Masked", masked)
    cv2.imwrite('masked.jpg', masked)
    cv2.waitKey(0)

    rois = []
    # save the circles to separate images
    for i, circle in enumerate(circles[0, :]):
        center = (circle[0], circle[1])
        radius = circle[2]
        x, y = center
        r = radius
        roi = im[y-r:y+r, x-r:x+r]
        rois.append(roi)
        # cv2.imshow(f"ROI {i}", roi)
        # cv2.waitKey(0)

    return rois

# run(cv2.imread('./selected.jpg'))