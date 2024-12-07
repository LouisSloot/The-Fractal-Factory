import math

def getDistance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def findBisectorAngle(prevLineAngle, interimTheta, currentlyMirrored):
    interimSupplement = math.pi - interimTheta
    bisectorAngle = prevLineAngle - interimSupplement/2
    if currentlyMirrored: bisectorAngle += math.pi
    return bisectorAngle

def lawOfCosines(radius, sides):
    centralAngle = math.radians(360 / sides)
    sideLength = math.sqrt(2*(radius**2)*(1-math.cos(centralAngle))) 
    return sideLength

def findPrevLineAngle(x1, y1, q1x, q1y):
    dx = q1x - x1
    dy = y1 - q1y # ugh... up is negative
    prevLineAngle = math.atan2(dy, dx)
    return prevLineAngle