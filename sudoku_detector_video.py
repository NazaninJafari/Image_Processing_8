import cv2
from imutils.perspective import four_point_transform
#import keyboard


videocap = cv2.VideoCapture(0)

while True:
    ret, frame = videocap.read()
    if ret == False:
        break

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    frame_blurred = cv2.GaussianBlur(frame_gray, (7,7), 3)
    frame_thresh_inv = cv2.adaptiveThreshold(frame_blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    contours = cv2.findContours(frame_thresh_inv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0]

    #sorted bigger to smaller
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    sudoku_contour = None

    for c in contours:
        epsilon = 0.12 * cv2.arcLength(c, True)
        #mokhtasat gushehaye contours
        approx = cv2.approxPolyDP(c, epsilon, True)
        #wich contour has 4 approx?
        if len(approx) == 4:
            sudoku_contour = c
            warped = four_point_transform(frame, approx.reshape(4,2))
            break

    if sudoku_contour is None:
        #writing text on image
        cv2.putText(frame, 'THERE IS NOT Sudoku!', (20,20), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,255,0), 4)

    else:
        
        cv2.drawContours(frame, [sudoku_contour], -1, (0,255,0), 10) 
    
    cv2.imshow('owebcam', frame)
    key = cv2.waitKey(100)

    if key == 27: #Esc
        break
    #save sudoku image    
    elif key == ord('s'): #S
        cv2.imwrite('output_imgs/output.jpg', warped)
