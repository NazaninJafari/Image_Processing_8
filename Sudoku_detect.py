
import cv2
import imutils
import argparse
from imutils.perspective import four_point_transform

parser = argparse.ArgumentParser(description= 'sudoku detector v1.0')

parser.add_argument("--input", type=str, help="path of your input image")
parser.add_argument("--output", type=str, help="path of your output image")
args = parser.parse_args()


image = cv2.imread(args.input)
gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

img_blurred = cv2.GaussianBlur(gray_img, (7,7), 3)


thresh = cv2.adaptiveThreshold(img_blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

thresh_inv = 255-thresh

contours = cv2.findContours(thresh_inv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0]
#sorting contours(big area to smal) 
contours = sorted(contours, key=cv2.contourArea, reverse=True)

sudoku_contour = None

for c in contours:
    epsilon = 0.02 * cv2.arcLength(c, True)
    #mokhtasat gushehaye contours
    approx = cv2.approxPolyDP(c, epsilon, True)
    #kodum contour 4 gushe has?
    if len(approx) == 4:
        sudoku_contour = c
        break
if sudoku_contour is None:
    print('THERE IS NOT')

else:
    result = cv2.drawContours(image, [sudoku_contour], -1, (0,255,0), 20)    


cv2.imwrite(args.output, result)