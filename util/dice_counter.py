import cv2

def run(image):
    # image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, threshed = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # show the thresholded image but make it bigger
    cv2.imshow('threshed', cv2.resize(threshed, (0,0), fx=2, fy=2))
    cv2.waitKey(0)
    
    ## findcontours
    cnts = cv2.findContours(threshed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]

    ## filter by area
    s1= 1
    s2 = 20
    xcnts = []
    for cnt in cnts:
        if s1<cv2.contourArea(cnt) <s2:
            xcnts.append(cnt)

    return len(xcnts)

print(run(cv2.imread('circle_0.jpg')))