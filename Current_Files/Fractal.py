from cmu_graphics import *
import math
from Knob import *
from Clone_App_Object import *
from collections import deque
from Horizontal_Slider import *
from Line_Tools import *
import random
    
def setupDefaultFractalApp(app):
    app.trailsOn = False
    app.isCurrentlyAnimated = False
    app.autoSlider = False
    app.autoKnob = False
    app.mirrorFractal = False
    app.bisectorsOn = False
    app.dashes = False
    app.recursionDepth = 0
    app.motifStage = 1
    app.baseStructureSides = 1
    app.startingSideLength = 400 # fits image best
    app.sideLength = 400
    app.fractalClones = deque()
    app.maxClones = 15
    app.defaultScalableAngle = 60
    app.scalableAngle = app.defaultScalableAngle
    motifSides = assignSides(app.motifStage)
    app.maxScalableAngle = getMaxScalableAngle(motifSides)
    app.fractalFill = 'white'
    app.lineWidth = 1
    app.fractalOpacity = 100
    app.fractalRotation = 0

def setupFractalApp(app):
    setupDefaultFractalApp(app)
    app.justRandomized = False # used by Customization to update dashboard
    app.justReset = False # ^^^
    app.fractalCenter = (app.width//2, app.height//2-5) # fitting BG img
    app.setMaxShapeCount(50000)
    app.stepsPerSecond = 30
    app.stepCount = 0

def drawFractal(app):
    fractalWrapper(app)
    if app.trailsOn:
        drawFractalClones(app)

def fractalWrapper(app):
    sideLength = app.sideLength
    sides = app.baseStructureSides
    relativeAngle = math.radians((360 / sides)) 
    if sides == 1: relativeAngle = math.pi
    startX, startY = app.fractalCenter
    mathHelpAngle = (math.pi/2) - (relativeAngle/2) # angle to top right vertex 
    radius = sideLength / (2 * math.cos(mathHelpAngle))
    startX += math.cos(mathHelpAngle + app.fractalRotation) * radius
    startY -= math.sin(mathHelpAngle+ app.fractalRotation) * radius
    baseStructureHelper(app, startX, startY, relativeAngle, sideLength, sides, 
                        app.mirrorFractal)

def baseStructureHelper(app, startX, startY, relativeAngle, length, sidesLeft, 
                        lastAngle = 0):
    if sidesLeft == 0: # base case
        return
    else: # recursive case
        if sidesLeft == app.baseStructureSides:
            totalAngle = math.pi
            totalAngle += app.fractalRotation
        else:
            totalAngle = lastAngle + relativeAngle
        dx =  length * math.cos(totalAngle)
        dy = length * math.sin(totalAngle)
        newX = startX + dx
        newY = startY - dy
        drawMotifWrapper(app, startX, startY, newX, newY)
        baseStructureHelper(app, newX, newY, relativeAngle, length, 
                            sidesLeft-1, totalAngle)

def setSideLength(app):
    if app.baseStructureSides > 2: # dont change length for 2 sided
        app.sideLength = app.startingSideLength * (0.88**app.baseStructureSides)
        # 0.88 is magic to keep fractal roughly the right size
        # (based off starting side length and BG image)

def myDrawLine(app, currX, currY, interimTheta, length, repsLeft, repsPassed, 
               recursionDepth, prevLineAngle, scalableAngle = None):
    fill = app.fractalFill
    currentlyMirrored = False
    if scalableAngle == None:
        scalableAngle = app.scalableAngle # normal case
    else:
        interimTheta *= -1 # mirrored case
    
    if repsLeft == 0: # base case
        return
    
    else: # recursive case
        if repsLeft == repsPassed: # drawing first line of motif
            totalAngle = prevLineAngle - math.radians(scalableAngle)
            bisectorAngle = None # only want bisectors on interim vertices
        else:
            totalAngle = prevLineAngle + interimTheta
            if interimTheta < 0: currentlyMirrored = True
            bisectorAngle = findBisectorAngle(prevLineAngle, interimTheta, 
                                              currentlyMirrored)

        dx =  length * math.cos(totalAngle)
        dy = length * math.sin(totalAngle)
        newX = currX + dx
        newY = currY - dy # up is negative...

        if (app.bisectorsOn) and (bisectorAngle != None): 
            drawBisector(app, currX, currY, length, bisectorAngle, 
                         recursionDepth)

        if recursionDepth == 0: # base case
            drawLine(currX, currY, newX, newY, lineWidth=app.lineWidth, 
                     fill=fill, opacity=app.fractalOpacity, dashes=app.dashes)
        else: # recursive case
            drawMotifWrapper(app, currX, currY, newX, newY, recursionDepth-1)
        myDrawLine(app, newX, newY, interimTheta, length, repsLeft-1, 
                   repsPassed, recursionDepth, totalAngle)

def drawMotifWrapper(app, x1, y1, x2, y2, recursionDepth = None):
    if recursionDepth == None:
        recursionDepth = app.recursionDepth

    distance = getDistance(x1, y1, x2, y2)
    centerX = (x1 + x2) / 2
    centerY = (y1 + y2) / 2
    sides = assignSides(app.motifStage)
    radius = distance / 4 if sides > 3 else distance / 6
    prevLineAngle = findPrevLineAngle(x1, y1, x2, y2)
    sideLength = lawOfCosines(radius, sides)
    motifDx, motifDy = findMotifDeltas(app, sideLength, sides, prevLineAngle)
    motifBegX, motifBegY, motifEndX, motifEndY = setMotifPoints(motifDx, 
                                                                motifDy, 
                                                                centerX, 
                                                                centerY)

    drawOuterSegments(app, x1, y1, motifBegX, motifBegY, motifEndX,
                       motifEndY, x2, y2, recursionDepth)
    drawMotif(app, sides, motifBegX, motifBegY, motifEndX, motifEndY, 
              prevLineAngle, sideLength, recursionDepth)

def drawMotif(app, sides, motifBegX, motifBegY, motifEndX, motifEndY, 
              prevLineAngle, sideLength, recursionDepth):
    if sides == 1: # simplest case
        drawLine(motifBegX, motifBegY, motifEndX, motifEndY, 
                 lineWidth=app.lineWidth, fill=app.fractalFill, 
                 opacity=app.fractalOpacity, dashes=app.dashes)
    elif sides == 3: # triangle edge case
        drawTriangularMotif(app, motifBegX, motifBegY, prevLineAngle, 
                            sideLength, recursionDepth)
    else:
        drawPolygonalMotif(app, motifBegX, motifBegY, prevLineAngle, sideLength,
                            sides, recursionDepth)

def setMotifPoints(dx, dy, centerX, centerY):
    x1 = centerX - (dx/2)
    y1 = centerY - (dy/2)
    x2 = centerX + (dx/2)
    y2 = centerY + (dy/2)
    return (x1, y1, x2, y2)

def findInterimTheta(app, prevLineAngle, sides):
    start = math.degrees(prevLineAngle) - app.scalableAngle
    end = math.degrees(prevLineAngle) + app.scalableAngle
    difference = end - start
    if sides > 3:
        totalInterims = (sides / 2) - 1
        interimTheta = math.radians(difference / totalInterims)
    else: 
        interimTheta = math.radians(difference)
    return interimTheta

def findMotifDeltas(app, sideLength, sides, prevLineAngle): 
    # simulates fractal drawing without drawing (... to find endpoints)
    dx, dy = 0,0
    interimTheta = findInterimTheta(app, prevLineAngle, sides)
    if sides > 3: loopBound = sides//2
    elif sides == 3: loopBound = 2
    else: loopBound = 1
    for i in range(loopBound):
        if i == 0:
            totalAngle = prevLineAngle - math.radians(app.scalableAngle)
        else:
            totalAngle = totalAngle + interimTheta
        dDx = sideLength * math.cos(totalAngle)
        dDy = sideLength * math.sin(totalAngle)
        dx += dDx
        dy -= dDy
    return (dx, dy)

def drawTriangularMotif(app, motifBegX, motifBegY, prevLineAngle, sideLength, 
                        recursionDepth):
    reps = 2
    interimTheta = findInterimTheta(app, prevLineAngle, 3)
    if app.mirrorFractal:
        scalableAngle = app.maxScalableAngle - app.scalableAngle
        myDrawLine(app, motifBegX, motifBegY, interimTheta, sideLength, reps, 
                   reps, recursionDepth, prevLineAngle, 
                   scalableAngle=scalableAngle)
    myDrawLine(app, motifBegX, motifBegY, interimTheta, sideLength, reps, reps, 
               recursionDepth, prevLineAngle)

def drawPolygonalMotif(app, motifBegX, motifBegY, prevLineAngle, sideLength, 
                       sides, recursionDepth):
    reps = sides // 2 # will always be whole num regardless
    interimTheta = findInterimTheta(app, prevLineAngle, sides)
    if app.mirrorFractal:
        scalableAngle = app.maxScalableAngle - app.scalableAngle
        myDrawLine(app, motifBegX, motifBegY, interimTheta, sideLength, reps, 
                   reps, recursionDepth, prevLineAngle, 
                   scalableAngle=scalableAngle)
    myDrawLine(app, motifBegX, motifBegY, interimTheta, sideLength, reps, reps, 
               recursionDepth, prevLineAngle)

def drawBisector(app, currX, currY, length, bisectorAngle, recursionDepth):
    dx = length * math.cos(bisectorAngle)
    dy = length * math.sin(bisectorAngle)
    newX = currX + dx
    newY = currY - dy
    if recursionDepth == 0:
        drawLine(currX, currY, newX, newY, fill=app.fractalFill, 
                 lineWidth=app.lineWidth, opacity=app.fractalOpacity, 
                 dashes=app.dashes)
    else:
        drawMotifWrapper(app, currX, currY, newX, newY, recursionDepth-1)

def drawOuterSegments(app, x1, y1, motifBegX, motifBegY, motifEndX, motifEndY, 
                      x2, y2, recursionDepth):
    if recursionDepth == 0:
        drawLine(x1, y1, motifBegX, motifBegY, lineWidth=app.lineWidth, 
                 fill=app.fractalFill, opacity=app.fractalOpacity, 
                 dashes=app.dashes)
        drawLine(motifEndX, motifEndY, x2, y2, lineWidth=app.lineWidth, 
                 fill=app.fractalFill, opacity=app.fractalOpacity, 
                 dashes=app.dashes)
    else:
        drawMotifWrapper(app, x1, y1, motifBegX, motifBegY, recursionDepth-1)
        drawMotifWrapper(app, motifEndX, motifEndY, x2, y2, recursionDepth-1)

def assignSides(stage):
    if stage == 0:
        sides = 1
    elif stage == 1:
        sides = 3 # equilateral triangle edge case
    else:
        sides = (stage * 2) + 2 # stage --> even sided regular polygons
    return sides

def addFractalClone(app):
    args = (app.fractalCenter, app.sideLength, app.dashes, 
            app.baseStructureSides, app.recursionDepth, app.motifStage, 
            app.mirrorFractal, app.bisectorsOn, app.lineWidth, app.width, 
            app.height, app.fractalRotation, app.fractalOpacity-10, 
            app.scalableAngle, app.defaultScalableAngle, app.maxScalableAngle, 
            app.fractalFill)
    clone = makeAppClone(*args)
    app.fractalClones.append((fractalWrapper, clone))
    if len(app.fractalClones) > app.maxClones:
        app.fractalClones.popleft() # O(1) <3
        # ... although a list would also be O(1) because app.maxClones
        # is constant...

def drawFractalClones(app):
    i = 0
    while i < len(app.fractalClones):
        funct, clone = app.fractalClones[i]
        clone.fractalOpacity -= 100 // app.maxClones
        if clone.fractalOpacity <= 0:
            app.fractalClones.popleft()
        else:
            i += 1
            funct(clone)

def randBool():
    return random.random() > 0.5 # 50/50 rand boolean

def randomizeParameters(app):
    app.autoSlider = randBool()
    app.autoKnob = randBool()
    app.mirrorFractal = randBool()
    app.bisectorsOn = randBool()
    app.dashes = randBool()
    app.recursionDepth = random.randint(0, 1)
    app.motifStage = random.randint(1,5)
    app.baseStructureSides = random.randint(1,8)
    setSideLength(app)
    app.fractalRotation = random.uniform(0, 2 * math.pi)
    app.lineWidth = random.randint(1,4)
    red = random.randint(1,255)
    blue = random.randint(1,255)
    green = random.randint(1,255)
    app.fractalFill = rgb(red, blue, green)

def resetFractalForTutorial(app):
    setupDefaultFractalApp(app)
    app.motifStage = 2
    app.mirrorFractal = True
    # ^this button was just clicked in tutorial, so i want to show its effect
    app.bisectorsOn = True
    # ^helps visualize horizontal slider effect
    
def takeFractalStep(app):
    if app.trailsOn:
        app.stepCount += 1
        if app.stepCount % 2 == 0:
            addFractalClone(app)
            app.stepCount = 0
    if app.autoKnob:
        app.fractalRotation += math.radians(1)
        app.fractalRotation %= math.pi * 2
        setKnobLineCoords(app)
    if app.autoSlider:
        app.scalableAngle += 1
        app.scalableAngle %= app.maxScalableAngle
        setHorzSlider(app)

def fractalOKP(app, key):
    pass
    
def fractalOMP(app, mouseX, mouseY):
    sides = assignSides(app.motifStage)
    horzSliderOMP(app, mouseX, mouseY, sides)
    knobOMP(app, mouseX, mouseY)
    
def fractalOMM(app, mouseX, mouseY):
    pass

def fractalOMR(app, mouseX, mouseY):
    horzSliderOMR(app, mouseX, mouseY)
    knobOMR(app, mouseX, mouseY)

def fractalOMD(app, mouseX, mouseY):
    sides = assignSides(app.motifStage)
    horzSliderOMD(app, mouseX, mouseY, sides)
    knobOMD(app, mouseX, mouseY)

# ----------------------------------------------------------------------------

def onAppStart(app):
    app.width, app.height = 1000, 800
    setupFractalApp(app)
    app.fractalFill = 'black' # makes it visible in this file (white BG)
    setupHorzSliderApp(app)
    setupKnobApp(app)

def redrawAll(app):
    drawFractal(app)

def onMousePress(app, mouseX, mouseY):
    pass

def onMouseDrag(app, mouseX, mouseY):
    fractalOMD(app, mouseX, mouseY)

def onMouseMove(app, mouseX, mouseY):
    fractalOMM(app, mouseX, mouseY)

def onMouseRelease(app, mouseX, mouseY):
    fractalOMR(app, mouseX, mouseY)

def onKeyPress(app, key):
    fractalOKP(app, key)

def onStep(app):
    takeFractalStep(app)

def main():
    runApp()

if __name__ == '__main__':
    main()