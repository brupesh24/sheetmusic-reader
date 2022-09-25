import argparse
import math
import cv2
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

dilated = cv2.dilate(image, (2,2), iterations=1)
cv2.imshow('Dilated', dilated)

diff = image.copy()
cv2.absdiff(image, dilated, diff)
cv2.imshow('Diff', diff)

#canny = cv2.Canny(image, 50, 300, None, 3)
canny = diff

#contours = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#contours = contours[0] if len(contours) == 2 else contours[1]

"""
displayImage = np.zeros(image.shape[:2], dtype='uint8')
cv2.drawContours(displayImage, contours, -1, (0,0,255), 2)
cv2.imshow('Contours Drawn', displayImage)

displayImageP = np.zeros(image.shape[:2], dtype='uint8')
cv2.drawContours(displayImageP, contours, -1, (0,0,255), 2)
cv2.imshow('Contours Drawn', displayImageP)
"""

displayImage = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)
displayImageP = np.copy(displayImage)

"""
lines = cv2.HoughLines(canny, 1, np.pi / 180, 150, None, 0, 0)

if lines is not None:
    for line in lines:
        r = line[0][0]
        theta = line[0][1]
        a = math.cos(theta)
        b = math.sin(theta)
        x0 = a * r
        y0 = b * r
        point1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
        point2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))

        cv2.line(displayImage, point1, point2, (0,0,255), 3, cv2.LINE_AA)
"""

linesP = cv2.HoughLinesP(canny, 1, np.pi / 180, 150, None, 20, 10)

blank = np.zeros(image.shape[:2], dtype='uint8')

averageLeftX = 0
averageLeftY = 0
averageRightX = 0
averageRightY = 0

maxX = 0
minX = 500
if linesP is not None:
    for lineP in linesP:
        l = lineP[0]
        if minX > l[0]:
            minX = l[0]
        if maxX < l[2]:
            maxX = l[2]

def checkValid(yCoord, yList):
    for y in yList:
        if abs(yCoord - y) <= 2 and abs(yCoord - y) <= 30:
            return False
    return True

"""
def createValidYList():
    yList = []
    if linesP is not None:
        for drawLine in linesP:
            yCheck = drawLine[0][1]
            yList.append(yCheck)
    for y in yList:
        if (abs(yCheck - y) <= 2) and (abs(yCheck - y) >= 30):
            yList.remove(yCheck)
    return yList
"""

yList = []
count = 0
drawList = []
if linesP is not None:
    for drawLine in linesP:
        l = drawLine[0]
        if checkValid(l[1], yList) == True:
            if (l[2] - l[0] > 100):
                cv2.line(displayImageP, (minX, l[1]), (maxX, l[1]), (0, 0, 255), 1)
                drawList.append(l[1])
        if count%2 == 0:
            color = (0,0,255)
        else: 
            color = (255,0 ,0)
        averageLeftX += l[0]
        averageLeftY += l[1]
        averageRightX += l[2]
        averageRightY += l[3]
        yList.append(l[1])
        #print(l[1])
        count += 1

"""
yList = createValidYList()
for y in yList:
    cv2.line(displayImageP, (minX, y), (maxX, y), (0, 0, 255), 1)
"""

yList.sort()
print(yList)
drawList.sort()
print(drawList)

lineNum = len(linesP)
averageLeftX /= lineNum
averageLeftY /= lineNum
averageRightX /= lineNum
averageRightY /= lineNum

print("Count ", count)
print("drawn Count", len(drawList))

print("Left (%d, %d), Right (%d, %d)" % (averageLeftX, averageLeftY, averageRightX, averageRightY))

cv2.imshow("Image", image)
cv2.imshow("canny", canny)
cv2.imshow("lines", blank)
cv2.imshow("Hough Line Probalistic Detection", displayImageP)

cv2.waitKey(0)

