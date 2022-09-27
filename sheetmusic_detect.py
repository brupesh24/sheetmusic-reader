import argparse
#import math
import cv2
import numpy as np

def getArgs():
    #Purpose: Gets arguments
    #Parameters: none
    #Return: argument
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required = True, help = "Path to the image")
    args = vars(ap.parse_args())
    return args

def processImage(imageName):
    #Purpose: Processes the image for line detection (methods of canny or diff)
    #Parameters: none
    #Return: processed image
    print(imageName["image"])
    image = cv2.imread(imageName["image"])
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    dilated = cv2.dilate(image, (2,2), iterations=1)
    cv2.imshow('Dilated', dilated)

    diff = image.copy()
    cv2.absdiff(image, dilated, diff)
    cv2.imshow('Diff', diff)

    #canny = cv2.Canny(image, 50, 300, None, 3)
    #canny = image

    #contours = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #contours = contours[0] if len(contours) == 2 else contours[1]
    return diff

def findX(linesP):
    #Purpose: finds min and max x values
    #Parameters: list of lines detected
    #Return: minimum x value and maximum x value
    maxX = 0
    minX = 500
    if linesP is not None:
        for lineP in linesP:
            l = lineP[0]
            if minX > l[0]:
                minX = l[0]
            if maxX < l[2]:
                maxX = l[2]
    return minX, maxX

def checkValid(yCoord, yList):
    #Purpose: checks if it is a double line
    #Parameters: y coordinate to check, y list to check against
    #Return: whether the line is not double (valid)
    for y in yList:
        if abs(yCoord - y) <= 2:
            return False
    return True

def findLines(minX, maxX, count, drawList):
    #Purpose: finds non-double lines to draw and their coordinates
    #Parameters: min and max X, count variable,
    #list of drawn y-coords
    #Return: count, list of drawn y-coords, lines with their coordinates
    linesToDraw = []
    if linesP is not None:
        for drawLine in linesP:
            l = drawLine[0]
            if checkValid(l[1], yList) == True:
                if (l[2] - l[0] > 100):
                    linesToDraw.append([(minX, l[1]), (maxX, l[1])])
                    drawList.append(l[1])
            yList.append(l[1])
            #print(l[1])
            count += 1
    return count, drawList, linesToDraw

def drawLines(displayImageP, linesToDraw, drawList):
    #Purpose: draws lines, removes extraneous (non-staff) lines
    #Parameters: image to display to, lines with coords, list of drawn y-coords
    #Return: None
    for lineToDraw in linesToDraw:
        if checkStaff(lineToDraw[0][1], drawList):
            cv2.line(displayImageP, lineToDraw[0], lineToDraw[1], (0, 0, 255), 1)
        else:
            drawList.remove(lineToDraw[0][1])
    return

def checkStaff(yCoord, drawList):
    #Purpose: checks if it is an extraneous line
    #Parameters: y coordinate to check, to draw list to check against
    #Return: whether the line is not extraneous (valid)
    for y in drawList:
        if abs(yCoord - y) <= 13 and y != yCoord:
            return True
    return False

if __name__ == "__main__":
    argImage = getArgs()
    processedImage = processImage(argImage)
    linesP = cv2.HoughLinesP(processedImage, 1, np.pi / 180, 150, None, 20, 10)

    displayImageP = cv2.cvtColor(processedImage, cv2.COLOR_GRAY2BGR)
    minX, maxX = findX(linesP)

    yList = []
    count = 0
    drawList = []

    count, drawList, linesToDraw = findLines(minX, maxX, count, drawList)

    drawLines(displayImageP, linesToDraw, drawList)

    #print("Count ", count)
    print("drawn Count", len(drawList))

    ogImage = cv2.imread(argImage["image"])
    cv2.imshow("Image", ogImage)
    cv2.imshow("processed", processedImage)
    cv2.imshow("Hough Line Probalistic Detection", displayImageP)

    cv2.waitKey(0)










"""
yList.sort()
print(yList)
drawList.sort()
print(drawList)
"""

"""
yList = createValidYList()
for y in yList:
    cv2.line(displayImageP, (minX, y), (maxX, y), (0, 0, 255), 1)
"""

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

"""
displayImage = np.zeros(image.shape[:2], dtype='uint8')
cv2.drawContours(displayImage, contours, -1, (0,0,255), 2)
cv2.imshow('Contours Drawn', displayImage)

displayImageP = np.zeros(image.shape[:2], dtype='uint8')
cv2.drawContours(displayImageP, contours, -1, (0,0,255), 2)
cv2.imshow('Contours Drawn', displayImageP)
"""

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