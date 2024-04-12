import cv2
import numpy as np

def run(src):

    image = cv2.imread(src)
    # cv2.imshow('Original Image', image)
    cv2.waitKey(0)

    # Convert to Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, th2 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # cv2.imshow('Thresholded Image', th2)
    # cv2.imwrite('sel_rect_thresholded.jpg', th2)

    # Use a copy of your image e.g. edged.copy(), since findContours alters the image
    contours, hierarchy = cv2.findContours(th2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # print(contours)

    # Draw all contours, note this overwrites the input image (inplace operation)
    # Use '-1' as the 3rd parameter to draw all
    cv2.drawContours(image, contours, -1, (0,255,0), thickness = 2)
    # cv2.imshow('Contours', image)
    # cv2.waitKey(0)
    # save the image with contours
    # cv2.imwrite('sel_rect_contours.jpg', image)

    print("Number of Contours found = " + str(len(contours)))

    # Sort contours large to small by area
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
    # print(sorted_contours)

    # loop over the contours
    for cnt in sorted_contours:
        # approximate the contour
        perimeter = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.05 * perimeter, True)
    
        if len(approx) == 4:
            break

    # Our x, y cordinates of the four corners 
    # print("Our 4 corner points are:")
    # print(approx)

    # Order obtained here is top left, bottom left, bottom right, top right
    inputPts = np.float32(approx)
    # print(inputPts)

    # dimensions A3 = 297 x 430 mm
    width, height = 430, 430

    outputPts = np.float32([[0,0],
                        [0,height],
                        [width, height],
                        [width,0]])

    # Get our Transform Matrix, M
    M = cv2.getPerspectiveTransform(inputPts,outputPts)

    # Apply the transform Matrix M using Warp Perspective
    dst = cv2.warpPerspective(image, M, (width, height))

    # cut the edges 
    dst = dst[16:height-16, 14:width-14]

    # cv2.imshow('Warped Image', dst)

    return dst

# run('test650783.jpg')
# cv2.imshow('img', cv2.imread('test650783.jpg'))