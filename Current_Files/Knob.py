from cmu_graphics import *
import math
from Line_Tools import *

def setupKnobApp(app):
    app.fractalRotation = 0
    app.knobCX = 640
    app.knobCY = app.height - 50
    app.knobR = 30
    app.knobHeld = False
    app.knobLineX1, app.knobLineY1 = app.knobCX, app.knobCY
    app.knobLineX2, app.knobLineY2 = None, None
    setKnobLineCoords(app)
    app.waitingForSecondClick = False
    app.secondClickTimer = app.stepsPerSecond//2

def drawKnob(app):
    drawKnobBase(app)
    drawKnobLine(app)

def drawKnobBase(app):
    drawCircle(app.knobCX, app.knobCY, app.knobR, fill='red', border='black',
               borderWidth=3)

def drawKnobLine(app):
    drawLine(app.knobLineX1, app.knobLineY1, app.knobLineX2, app.knobLineY2,
             fill='black', lineWidth=6) 

def setKnobLineCoords(app):
    app.knobLineX2 = (app.knobLineX1 + 
                      (app.knobR * math.cos(-app.fractalRotation)))
    app.knobLineY2 = (app.knobLineY1 + 
                      (app.knobR * math.sin(-app.fractalRotation)))
    
def setFractalRotation(app, mouseX, mouseY):
    app.fractalRotation = trackThetaFromPoint(app, mouseX, mouseY) * -1
    # negate because of how fractal is implemented; affects setKnobLineCoords

def trackThetaFromPoint(app, mouseX, mouseY):
    dx = mouseX - app.knobCX
    dy = mouseY - app.knobCY
    theta = math.atan2(dy, dx)
    return theta

def knobOMR(app, mouseX, mouseY):
    app.knobHeld = False

def knobOMD(app, mouseX, mouseY):
    if app.knobHeld:
        setFractalRotation(app, mouseX, mouseY)
        setKnobLineCoords(app)
    
def knobOMP(app, mouseX, mouseY):
    if getDistance(mouseX, mouseY, app.knobCX, app.knobCY) <= app.knobR:
        app.knobHeld = True
        setFractalRotation(app, mouseX, mouseY)
        setKnobLineCoords(app)
        if app.tutorialStage == 6:
            if app.waitingForSecondClick == True:
                app.tutorialStage += 1
            else:
                app.waitingForSecondClick = True

def knobOMM(app, mouseX, mouseY):
    pass

def knobOKP(app, key):
    pass

def takeKnobStep(app):
    if app.waitingForSecondClick:
        app.secondClickTimer -= 1
        if app.secondClickTimer <= 0:
            app.waitingForSecondClick = False
    else:
        app.secondClickTimer = app.stepsPerSecond//2

# ----------------------------------------------------------------------------

def onAppStart(app):
    app.width, app.height = 1000, 800
    setupKnobApp(app)

def redrawAll(app):
    drawKnob(app)

def onMousePress(app, mouseX, mouseY):
    knobOMP(app, mouseX, mouseY)

def onMouseDrag(app, mouseX, mouseY):
    knobOMD(app, mouseX, mouseY)

def onMouseMove(app, mouseX, mouseY):
    knobOMM(app, mouseX, mouseY)

def onMouseRelease(app, mouseX, mouseY):
    knobOMR(app, mouseX, mouseY)

def onKeyPress(app, key):
    knobOKP(app, key)

def onStep(app):
    takeKnobStep(app)

def main():
    runApp()

if __name__=='__main__':
    main()