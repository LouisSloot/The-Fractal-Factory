from cmu_graphics import *
from Fractal import *
from TP_Dash import *
from Back_Button import *
import random

def setupMatchGameApp(app):
    app.showingPopup = False
    app.generateFill = 'darkGrey'
    app.difficulty = 'Moderate'
    app.frameCX, app.frameCY = app.width-100, 100
    app.targetAnimationDX, app.targetAnimationDY = None, None
    resetMatchGame(app)

def resetMatchGame(app):
    setupDefaultFractalApp(app)
    updateDashboardButtons(app)
    app.gameLost = False
    app.submitsLeft = 3
    app.generated = False
    app.targetFractalApp = None
    app.showTarget = True
    app.showUserFractal = False
    app.targetAnimationStarted = False
    app.targetAnimationDone = False

def drawMatchGameScreen(app):
    if not app.generated:
        drawPreGame(app)
    else:
        drawGame(app)

def drawPreGame(app):
    drawPreGameBackground(app)
    drawBackButton(app)
    drawDifficultyLabel(app)
    drawDifficultyButtons(app)
    drawGenerateButton(app)

def drawPreGameBackground(app):
    path = './Industrial_Background.jpg'
    # from https://stock.adobe.com/
    drawImage(path, 0, 0, width=app.width, height=app.height)

def drawDifficultyButtons(app):
    buttonWidth = 200
    buttonHeight = 75
    gap = 20
    startX = app.width//2 - (1.5 * (buttonWidth+gap))
    startY = app.height//2 - buttonHeight//2
    fills = ['gold', 'darkOrange', 'darkRed']
    labels = ['Moderate', 'Difficult', 'Extreme']
    for i in range(3):
        fill = fills[i]
        text = labels[i]
        leftEdge = startX + ((buttonWidth+gap) * i)
        cx = leftEdge + buttonWidth//2
        cy = startY + buttonHeight//2
        borderWidth = 5 if text == app.difficulty else 2
        drawRect(leftEdge, startY, buttonWidth, buttonHeight, fill=fill, 
                 border='black', borderWidth=borderWidth)
        drawLabel(text, cx, cy, size=40, bold=True)

def checkDifficultyClick(app, x, y):
    buttonWidth = 200
    buttonHeight = 75
    startX = app.width//2 - (1.5 * (buttonWidth))
    startY = app.height//2 - buttonHeight//2
    if ((startX <= x <= startX + buttonWidth) and 
        (startY <= y <= startY+buttonHeight)):
        app.difficulty = 'Moderate'
    elif ((startX + buttonWidth <= x <= startX + (2*buttonWidth)) and 
          (startY <= y <= startY+buttonHeight)):
        app.difficulty = 'Difficult'
    elif ((startX + (2*buttonWidth) <= x <= startX + (3*buttonWidth)) and 
          (startY <= y <= startY+buttonHeight)):
        app.difficulty = 'Extreme'

def drawDifficultyLabel(app):
    drawRect(app.width//2, 80, 550, 110, fill='yellow', border='black',
             borderWidth=5, align='center')
    text = 'Production Zone'
    drawLabel(text, app.width//2, 80, size=60, bold=True)

def drawGame(app):
    drawGameBackground(app)
    if not app.targetAnimationDone:
        drawPreAnimationUI(app)
    else:
        drawPostAnimationUI(app)
    
def drawPreAnimationUI(app):
    fractalWrapper(app.targetFractalApp)
    drawPreHeaders(app)
    drawGotIt(app)

def drawGotIt(app):
    buttonLabel = 'Got it.'
    drawRect(app.width//2-(150/2), app.height-40-(60/2), 150, 60, 
             fill='cadetBlue', border='black', borderWidth=3)
    drawLabel(buttonLabel, app.width//2, app.height-40, size=25, bold=True)

def drawPreHeaders(app):
    header = 'A new order for this fractal just came in!'
    subHeader = 'We need you to produce it!'
    drawRect(app.width//2, (50+20)/2, 750, 90, fill='darkGrey', border='black',
             borderWidth=5, align='center')
    drawLabel(header, app.width//2, 20, size=35, bold=True)
    drawLabel(subHeader, app.width//2, 50, size=20, bold=True)

def drawGameBackground(app):
    path = './Control_Panel.png' # exact same as Factory_Screen
    drawImage(path, 0, -290, width=1000, height=1200)

def drawPostAnimationUI(app):
    drawPostHeaders(app)
    fractalWrapper(app.targetFractalApp)
    fractalWrapper(app)
    drawTools(app)
    drawLivesLeft(app)
    drawSubmitButton(app)
    drawPopups(app)

def drawPopups(app):
    if app.showingPopup:
        drawCloseBox(app)
        if app.gameLost:
            drawLoseScreen(app)
        elif matchesTargetFractal(app):
            drawCorrectScreen(app)
        else:
            drawIncorrectScreen(app)

def drawTools(app):
    drawDashboard(app)
    if app.difficulty == 'Difficult' or app.difficulty == 'Extreme':
        drawKnob(app)
    if app.difficulty == 'Extreme':
        drawHorzSlider(app)

def drawPostHeaders(app):
    header = 'Here are your tools!'
    subHeader = "Press 'Submit' when you are done."
    drawRect(app.width//2, (50+20)/2, 400, 90, fill='darkGrey', border='black',
             borderWidth=5, align='center')
    drawLabel(header, app.width//2, 20, size=35, bold=True)
    drawLabel(subHeader, app.width//2, 50, size=20, bold=True)
    drawRect(app.width-200, 0, 200, 200, border='black', fill='darkGrey',
             borderWidth=4)

def drawSubmitButton(app):
    drawRect(app.width-130, app.height-65, 100, 50, fill='lightBlue', border='black',
             borderWidth=3)
    drawLabel('Submit', app.width-130+(100/2), app.height-65+(50/2), 
              size=22, bold=True)
    
def drawLivesLeft(app):
    path = './Robot_Heart.png'
    # from https://en.ac-illust.com/clip-art/23726307/robot-heart
    # (I converted to .png)
    width, height = 120, 80
    startLeft, startTop = app.width-110, 230
    gap = 130
    for _ in range(app.submitsLeft):
        drawImage(path, startLeft, startTop, width=width, height=height)
        startTop += gap

def takeMatchGameStep(app):
    if app.generated and not app.targetAnimationStarted:
        setTargetAnimationValues(app) 
    if app.showUserFractal and not app.targetAnimationDone:
        app.targetAnimationStarted = True
        cx, cy = app.targetFractalApp.fractalCenter
        cx = cx + app.targetAnimationDX
        cy = cy + app.targetAnimationDY 
        # add DY because of setTargetAnimationValues implementation
        app.targetFractalApp.fractalCenter = (cx, cy)
        if app.targetFractalApp.baseStructureSides < 5: decayConst = 0.986  
        else: decayConst = 0.981 # magic to shrink fractal properly
        app.targetFractalApp.sideLength *= decayConst
        if cx >= app.frameCX: # target fractal has reached destination
            app.targetFractalApp.fractalCenter = (app.frameCX, app.frameCY)
            app.targetAnimationDone = True

def setTargetAnimationValues(app):
    cx, cy = app.targetFractalApp.fractalCenter
    dx = app.frameCX - cx
    dy = app.frameCY - cy # always negative
    app.targetAnimationDX = dx / (app.stepsPerSecond * 2)
    app.targetAnimationDY = dy / (app.stepsPerSecond * 2)

def getRandFractalApp(app):
    args = getRandFractalAppArgs(app)
    fractalApp = makeAppClone(*args)
    return fractalApp

def getRandFractalAppArgs(app):
    width, height = 1000, 800
    motifStage = random.randint(1,5)
    scalableAngle = 60  # these need to be above conditional cases
    sides = assignSides(motifStage)
    maxScalableAngle = getMaxScalableAngle(sides)
    if app.difficulty == 'Moderate':
        recursionDepth = random.randint(0, 1)
        fractalRotation = 0
        bisectorsOn = False
    elif app.difficulty == 'Difficult':
        recursionDepth = random.randint(0, 1)
        fractalRotation = random.uniform(0, math.pi * 2)
        bisectorsOn = randBool()
    elif app.difficulty == 'Extreme':
        recursionDepth = random.randint(1, 2)
        fractalRotation = random.uniform(0, math.pi * 2)
        bisectorsOn = randBool()
        scalableAngle = random.randint(0, maxScalableAngle)
    mirrorFractal = randBool()
    sideLength = 400
    baseStructureSides = random.randint(1,8)
    if baseStructureSides > 2:
        sideLength *= (0.88**baseStructureSides)
    dashes = False
    lineWidth = 1
    fractalFill = 'red'
    fractalOpacity = 100
    defaultScalableAngle = 60
    fractalCenter = (width//2, height//2-5)
    return (fractalCenter, sideLength, dashes, baseStructureSides, 
            recursionDepth, motifStage, mirrorFractal, bisectorsOn, lineWidth, 
            width, height, fractalRotation, fractalOpacity, scalableAngle, 
            defaultScalableAngle, maxScalableAngle, fractalFill)

def drawGenerateButton(app):
    drawRect(app.width//2, app.height-150, 300, 100, align='center', fill=app.generateFill, border='black', borderWidth=5)
    drawLabel('Generate', app.width//2, app.height-150, size=50, bold=True)
    
def matchGameOMP(app, mouseX, mouseY):
    if not app.showingPopup: # freeze while message is shown
        if not app.generated:
            backButtonOMP(app, mouseX, mouseY)
            checkGenerateClick(app, mouseX, mouseY)
            checkDifficultyClick(app, mouseX, mouseY)
        else: 
            checkGotItClick(app, mouseX, mouseY)
        if app.targetAnimationDone:
            checkSubmitClick(app, mouseX, mouseY)
            sides = assignSides(app.motifStage)
            dashboardOMP(app, mouseX, mouseY)
            if app.difficulty == 'Difficult' or app.difficulty == 'Extreme':
                knobOMP(app, mouseX, mouseY)
            if app.difficulty == 'Extreme':
                horzSliderOMP(app, mouseX, mouseY, sides)

def checkGotItClick(app, x, y):
    app.showUserFractal = ((app.width//2-(150/2) <= x <= app.width//2+(150/2)) 
                           and 
                           (app.height-40-(60/2) <= y <= app.height-40+(60/2)))

def checkSubmitClick(app, x, y):
    if ((app.width-130 <= x <= app.width-130+100) and 
        (app.height-65 <= y <= app.height-65+50)):
        if not matchesTargetFractal(app):
            app.submitsLeft -= 1
            if app.submitsLeft == 0:
                app.gameLost = True
        app.showingPopup = True

def matchGameOMR(app, mouseX, mouseY):
    if app.targetAnimationDone:
        dashboardOMR(app, mouseX, mouseY)
        if app.difficulty == 'Difficult' or app.difficulty == 'Extreme':
            knobOMR(app, mouseX, mouseY)
        if app.difficulty == 'Extreme':
            horzSliderOMR(app, mouseX, mouseY)

def checkGenerateClick(app, x, y):
    leftEdge = app.width//2 - 150
    rightEdge = app.width//2 + 150
    topEdge = app.height-150 - 50
    btmEdge = app.height-150 + 50
    if (leftEdge <= x <= rightEdge) and (topEdge <= y <= btmEdge):
        app.targetFractalApp = getRandFractalApp(app)  
        app.generated = True

def matchGameOMD(app, mouseX, mouseY):
    if app.targetAnimationDone:
        dashboardOMD(app, mouseX, mouseY)
        sides = assignSides(app.motifStage)
        if app.targetAnimationDone:
            if app.difficulty == 'Difficult' or app.difficulty == 'Extreme':
                knobOMD(app, mouseX, mouseY)
            if app.difficulty == 'Extreme':
                horzSliderOMD(app, mouseX, mouseY, sides)

def matchGameOMM(app, mouseX, mouseY):
    if app.targetAnimationDone:
        dashboardOMM(app, mouseX, mouseY)
        if app.difficulty == 'Difficult' or app.difficulty == 'Extreme':
            knobOMM(app, mouseX, mouseY)
        if app.difficulty == 'Extreme':
            horzSliderOMM(app, mouseX, mouseY)

def matchGameOKP(app, key):
    if key == 'v':
        app.showTarget = not app.showTarget
    elif key == 'k' and app.generated and not app.showUserFractal:
        app.showUserFractal = True
    elif key == 'enter':
        if app.showingPopup:
            app.showingPopup = False
            if app.gameLost: 
                resetMatchGame(app)
            elif matchesTargetFractal(app):
                resetMatchGame(app)

def matchesTargetFractal(app):
    submission = app
    target = app.targetFractalApp
    sides = assignSides(target.motifStage)
    targetMaxScalable = getMaxScalableAngle(sides)
    moderate = ((submission.baseStructureSides == target.baseStructureSides or 
                 (target.mirrorFractal and (target.baseStructureSides == 1 or
                target.baseStructureSides == 2) and (submission.baseStructureSides == 1
                  or submission.baseStructureSides == 2))) and 
            (submission.motifStage == target.motifStage) and
            (submission.recursionDepth == target.recursionDepth) and
            (submission.mirrorFractal == target.mirrorFractal) and 
            (submission.bisectorsOn == target.bisectorsOn)
           )
    if not moderate: 
        moderate = ((target.recursionDepth == submission.recursionDepth == 0) and
                  (target.baseStructureSides == 1 or target.baseStructureSides == 2) and
                  (submission.baseStructureSides == 1 or submission.baseStructureSides == 2) and
                  (target.baseStructureSides != submission.baseStructureSides) and 
                  (target.mirrorFractal != submission.mirrorFractal)) 
                 # ^^ visually identical edge case
    if not moderate:
        moderate = ((target.mirrorFractal and target.baseStructureSides == 2) and
                    ((submission.mirrorFractal and 
                     (submission.baseStructureSides == 1 or 
                     submission.baseStructureSides == 2)) or 
                     submission.baseStructureSides == 2 and 
                     not submission.mirrorFractal))
    sidesForRotationAngle = max(2, app.baseStructureSides)
    difficult = (
              sufficientlyClose(submission.fractalRotation%(math.pi*2/sidesForRotationAngle), 
                                target.fractalRotation%(math.pi*2/sidesForRotationAngle))
             )
    extreme = (sufficientlyClose(submission.scalableAngle, target.scalableAngle) or 
            sufficientlyClose(submission.scalableAngle, targetMaxScalable-target.scalableAngle))
    if app.difficulty == 'Moderate':
        return moderate
    elif app.difficulty == 'Difficult':
        return moderate and difficult
    else:
        return moderate and difficult and extreme
    
def sufficientlyClose(val1, val2):
    absoluteDifference = abs(val1-val2)
    if (val1 == val2 == 0): return True
    relativeDifference = absoluteDifference / max(val1, val2)
    return (relativeDifference < 0.15) # arbitrary threshold

def drawCorrectScreen(app):
    drawRect(app.width//2, app.height//2, 700, 300, fill='darkGrey', 
             border='black', borderWidth=5, align='center')
    line1 = "The customer is thrilled!"
    line2 = "Good work. I'm impressed."
    drawLabel(line1, app.width//2, app.height//2-30, size=30, bold=True) 
    drawLabel(line2, app.width//2, app.height//2+30, size=30, bold=True)

def drawIncorrectScreen(app):
    drawRect(app.width//2, app.height//2, 700, 300, fill='darkGrey', 
             border='black', borderWidth=5, align='center')
    line1 = "Hmmm... the customer isn't quite happy."
    line2 = findCorrectFeedback(app)
    drawLabel(line1, app.width//2, app.height//2-30, size=30, bold=True)
    drawLabel(line2, app.width//2, app.height//2+30, size=30, bold=True,
              italic=True)
    
def drawLoseScreen(app):
    drawRect(app.width//2, app.height//2, 700, 300, fill='darkGrey', 
             border='black', borderWidth=5, align='center')
    line1 = "Three failed orders... rough."
    line2 = "Look, the customer is out the door."
    drawLabel(line1, app.width//2, app.height//2-30, size=30, bold=True) 
    drawLabel(line2, app.width//2, app.height//2+30, size=30, bold=True)

def drawCloseBox(app):
    drawRect(app.width//2, app.height//2+200, 200, 50, fill='darkGrey', 
             border='black', borderWidth=5, align='center')
    text = "Press 'enter' to close."
    drawLabel(text, app.width//2, app.height//2+200, size=15, bold=True)

def findCorrectFeedback(app):
    submission = app
    target = app.targetFractalApp
    if submission.baseStructureSides != target.baseStructureSides:
        feedback = 'Maybe try changing your base structure...'
    elif submission.motifStage != target.motifStage:
        feedback = 'Does that motif look right?'
    elif submission.recursionDepth != target.recursionDepth:
        feedback = "Man, isn't recursion confusing?"
    elif submission.bisectorsOn != target.bisectorsOn:
        feedback = 'Make sure your bisectors match!'
    elif submission.mirrorFractal != target.mirrorFractal:
        feedback = 'Double check that mirroring button.'
    elif  not sufficientlyClose(
                submission.fractalRotation%(math.pi*2/app.baseStructureSides), 
                target.fractalRotation%(math.pi*2/app.baseStructureSides)):
        feedback = 'Keep messing with the knob!'
    elif not (sufficientlyClose(submission.scalableAngle, target.scalableAngle) 
           or sufficientlyClose(submission.scalableAngle, 
                                target.maxScalableAngle-target.scalableAngle)):
        feedback = 'Make sure that slider is right.'
    return feedback

# ----------------------------------------------------------------------------

def onAppStart(app):
    app.width, app.height = 1000, 800
    setupKnobApp(app)
    setupHorzSliderApp(app)
    setupFractalApp(app)
    setupDashboardApp(app)
    setupMatchGameApp(app)

def redrawAll(app):
    drawMatchGameScreen(app)

def onMousePress(app, mouseX, mouseY):
    matchGameOMP(app, mouseX, mouseY)

def onMouseDrag(app, mouseX, mouseY):
    matchGameOMD(app, mouseX, mouseY)

def onMouseMove(app, mouseX, mouseY):
    matchGameOMM(app, mouseX, mouseY)

def onMouseRelease(app, mouseX, mouseY):
    matchGameOMR(app, mouseX, mouseY)

def onKeyPress(app, key):
    fractalOKP(app, key)
    matchGameOKP(app, key)

def onStep(app):
    takeMatchGameStep(app)

def main():
    runApp()

if __name__ == '__main__':
    main()