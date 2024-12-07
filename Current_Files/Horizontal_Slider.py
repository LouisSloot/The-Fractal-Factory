from cmu_graphics import *
import math

def setupHorzSliderApp(app):
    app.scalableAngle = 60
    app.horzSliderRadius = 20
    app.sliderHeld = False
    app.sliderLength = 200
    app.sliderX1 = 350
    app.sliderX2 = app.sliderX1 + app.sliderLength
    app.sliderY = app.height - 50
    app.cx, app.cy = app.sliderX1, app.sliderY
    setHorzSlider(app)
    app.sliderLineWidth = 2

def drawHorzSlider(app):
    drawSliderLine(app)
    drawSliderCircle(app)

def drawSliderLine(app):
    sliderDivetSize = 30
    circ1Fill = 'red' if app.cx >= app.sliderX1 else 'dimGrey'
    circ2Fill = 'red' if app.cx >= app.sliderX2 else 'dimGrey'
    leftRectFill = 'red'
    rightRectFill = 'dimGrey'
    drawCircle(app.sliderX1, app.sliderY, sliderDivetSize/2, fill=circ1Fill,
               border='black', borderWidth=3)
    drawCircle(app.sliderX2, app.sliderY, sliderDivetSize/2, fill=circ2Fill,
               border='black', borderWidth=3)
    drawRect((app.sliderX1), (app.sliderY-sliderDivetSize/2),
             (app.cx-app.sliderX1)+1, sliderDivetSize, fill=leftRectFill)
    drawRect(app.cx, (app.sliderY-sliderDivetSize/2), (app.sliderX2-app.cx)+1,
             sliderDivetSize, fill=rightRectFill)
            # ^^+1's avoid 0-width error (could also do max(1, ~~~))
    drawLine((app.sliderX1), (app.sliderY-sliderDivetSize/2)+1, app.sliderX2+1, 
             (app.sliderY-sliderDivetSize/2)+1, fill='black', lineWidth=3) 
    drawLine(app.sliderX1, (app.sliderY+sliderDivetSize/2)-1, app.sliderX2+1,
             (app.sliderY+sliderDivetSize/2)-1, fill='black', lineWidth=3) 
                # ^^horz. sides of rects; +-1's are visual adjustments

def drawSliderCircle(app):
    drawCircle(app.cx, app.cy, app.horzSliderRadius, fill='grey',
               border='black', borderWidth=3)
        
def setHorzSlider(app, mouseX=None):
    if mouseX == None:
        sliderDegree = app.scalableAngle / app.maxScalableAngle
        app.cx = app.sliderX1 + (app.sliderLength * sliderDegree)
    else:
        app.cx = mouseX
        if (app.cx < app.sliderX1):
            app.cx = app.sliderX1
        elif (app.cx > app.sliderX2):
            app.cx = app.sliderX2
        if (app.cx == app.sliderX2) and (app.tutorialStage == 5):
            app.tutorialStage += 1

def distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2+(y1-y2)**2)

def updateScalableAngle(app, sides):
    maxScalableAngle = app.maxScalableAngle
    sliderDegree = 0
    if app.cx != app.sliderX1:
        sliderDegree = (app.cx-app.sliderX1) / app.sliderLength
    app.scalableAngle = maxScalableAngle * sliderDegree

def getMaxScalableAngle(sides):
    max = (360+90*(sides-6)) # observed pattern; period of cycle
    if sides % 4 == 0:
        max *= 2
    elif sides == 3:
        max = 360 # hardcoding triangle edge case
    return max

def horzSliderOMP(app, mouseX, mouseY, sides):
    if distance(mouseX, mouseY, app.cx, app.cy) < app.horzSliderRadius:
        app.sliderHeld = True
        setHorzSlider(app, mouseX)
        updateScalableAngle(app, sides)

def horzSliderOMR(app, mouseX, mouseY):
    app.sliderHeld = False

def horzSliderOMD(app, mouseX, mouseY, sides):
    if app.sliderHeld:
        setHorzSlider(app, mouseX)
    updateScalableAngle(app, sides)

def horzSliderOMM(app, mouseX, mouseY):
    pass

# ----------------------------------------------------------------------------

def onAppStart(app):
    app.width, app.height = 1000, 800
    setupHorzSliderApp(app)

def redrawAll(app):
    drawHorzSlider(app)

def onMousePress(app, mouseX, mouseY):
    horzSliderOMP(app, mouseX, mouseY)

def onMouseDrag(app, mouseX, mouseY):
    horzSliderOMD(app, mouseX, mouseY)

def onMouseMove(app, mouseX, mouseY):
    horzSliderOMM(app, mouseX, mouseY)

def onMouseRelease(app, mouseX, mouseY):
    horzSliderOMR(app, mouseX, mouseY)

def main():
    runApp()

if __name__ == '__main__':
    main()