from cmu_graphics import *
from Fractal import *
from Line_Customization import *
import copy

def setupDashboardApp(app):
    app.tutorialFinished = False
    app.tutorialStage = 0
    app.buttonSize = 105 # matches BG image well
    app.buttonCount = 5
    app.selectedButton = None 
    setButtonStartY(app)
    loadButtons(app)

def loadButtons(app):
    app.buttonList = []
    stageLims = loadStageLims()
    dashboardApps = loadDashboardApps(app)
    titles = loadButtonAppTitles()
    for i in range(app.buttonCount):
        currApp = dashboardApps[i]
        title = titles[i]
        cx, cy = findButtonCX(app, i), findButtonCY(app, i)
        currApp.fractalCenter = (cx, cy)
        width, height = app.buttonSize, app.buttonSize
        stageLim = stageLims[i]
        newButton = Button(i, title, cx, cy, width, height, stageLim, currApp)
        app.buttonList.append(newButton)

def loadButtonAppTitles():
    return ['base', 'motif', 'recursion', 'bisectors', 'mirror']

def loadTutorialTexts():
    box0 = [
            'This first button controls the underlying',
            'structure of your fractal! It starts',
            'out as a line and goes up to an octagon!',
            'For each button, clicking the top half',
            'increases it, and the bottom half decreases',
            'it. Increase this button twice to set the',
            'structure to a triangle.'
            ]
    box1 = [
            "This button controls the 'motif' of your",
            'fractal. This is what is drawn for each',
            'line of your underlying base structure.',
            'As you can tell, three motifs are drawn',
            'for this triangle. Increase the motif',
            'once, to the top of a hexagon, before',
            'we move on to the next button.'
            ]
    box2 = [
            'This button controls the recursion depth',
            'of your fractal. This is where the shapes',
            'start becoming fractal-y! When you click',
            'this, every line, rather than only the',
            'sides of the base structure, will be',
            'replaced with a motif. Increase it once',
            'and see how more motifs are drawn.'
            ]
    box3 = [
            'This button turns bisectors on and off.',
            'Essentially, bisectors are lines that',
            'cut an angle in half. So, there will be one',
            'bisector drawn for each vertex of each',
            'motif. The bisectors also become motifs',
            'with recursion, leading to interesting',
            'patterns! Turn on bisectors to continue.'
            ]
    box4 = [
            'The last button controls whether the fractal',
            'is mirrored or not. As you have seen,',
            'motifs are drawn outward on the fractal;',
            'however, this button draws them inward, too.',
            'It is interesting how the fractal begins to',
            'overlap with itself. Turn mirroring on before',
            'we learn about the other controls.'
            ]
    box5 = [
            'This slider here is a bit more complicated.',
            "I've reset your fractal to simplify things.",
            'As you drag the slider, you will notice the',
            'left- and right-most sides of the motif',
            'change angle. All angles between adjust',
            'to become symmetrical. This is a powerful',
            'tool. Slide it to the right end to continue.'
        ]
    box6 = [
            'This knob is way simpler: it rotates your',
            "fractal. Don't worry, I built it with strong",
            'material, so you can spin it as fast as',
            "you'd like! Now is a good time to say that",
            'crazy fractals WILL slow down CMU graphics.',
            'Considerably. Proceed with caution : ).',
            'Double click the knob to move on.'
            ]
    box7 = [
            'These last controls are all for fun! You',
            'can make your fractal out of thick, pink,',
            "dashed lines if you'd like! You can also",
            'automate the slider and knob for some cool',
            'animations; adding trails will make them',
            'even cooler! My favorite is to keep clicking',
            "random. That's all! Press reset to finish."
            ]
    return [box0, box1, box2, box3, box4, box5, box6, box7]

def findButtonCX(app, i):
    return app.buttonSize//2

def findButtonCY(app, i):
    return app.buttonStartY + (i * app.buttonSize)

def loadDashboardApps(app):
    baseApp = copy.copy(app) # button logos should not be aliased!
    baseApp.motifStage = 0
    baseApp.sideLength = 80
    baseApp.lineWidth = 3

    motifApp = copy.copy(app)
    motifApp.sideLength = 80
    motifApp.lineWidth = 3

    recursionApp = copy.copy(app)
    recursionApp.sideLength = 80
    recursionApp.lineWidth = 3

    bisectorApp = copy.copy(app)
    bisectorApp.sideLength = 80
    bisectorApp.lineWidth = 3

    mirrorApp = copy.copy(app)
    mirrorApp.sideLength = 80
    mirrorApp.lineWidth = 3
    
    return [baseApp, motifApp, recursionApp, bisectorApp, mirrorApp]

def loadStageLims():
    return [9, 6, 4, 2, 2] # cycle lengths on buttons

class Button:
    def __init__(self, id, title, centerX, centerY, width, height, stageLim, 
                 app):
        self.id = id
        self.title = title
        self.centerX = centerX
        self.centerY = centerY
        self.width = width
        self.height = height
        self.fill = None
        self.border = 'black'
        self.align = 'center'
        self.stage = 1
        self.stageLim = stageLim
        self.app = app
    
    def __repr__(self):
        return f'CX: {self.centerX}, CY: {self.centerY}, Title: {self.title}'

    def __eq__(self, other):
        return (isinstance(other, Button)) and (self.title == other.title)

    def incStage(self, app):
        self.stage += 1
        self.stage %= self.stageLim
        self.stage = max(1, self.stage)
        self.adjustParam(app)
    
    def decStage(self, app):
        self.stage -= 1
        self.stage %= self.stageLim
        self.stage = max(1, self.stage)
        self.adjustParam(app)
    
    def adjustParam(self, app):
        if self.title == 'base':
            self.app.baseStructureSides = self.stage
            if self.app.baseStructureSides != 2: 
                self.app.sideLength = 65 * (0.93 ** self.app.baseStructureSides)
            app.baseStructureSides = self.stage
            setSideLength(app)
        elif self.title == 'motif':
            self.app.motifStage = self.stage
            app.motifStage = self.stage
            motifSides = assignSides(app.motifStage)
            app.maxScalableAngle = getMaxScalableAngle(motifSides)
        elif self.title == 'recursion':
            self.app.recursionDepth = self.stage - 1 # i 0-counted recursion
            app.recursionDepth = self.stage - 1
        elif self.title == 'bisectors':
            self.app.bisectorsOn = not self.app.bisectorsOn
            app.bisectorsOn = not app.bisectorsOn
        elif self.title == 'mirror':
            self.app.mirrorFractal = not self.app.mirrorFractal
            app.mirrorFractal = not app.mirrorFractal
    
    def reverseAdjustParam(self, app):
        if self.title == 'base':
            self.app.baseStructureSides = app.baseStructureSides
            self.app.sideLength = 65 * (0.93 ** self.app.baseStructureSides)
            self.stage = app.baseStructureSides
        elif self.title == 'motif':
            self.app.motifStage = app.motifStage
            self.stage = app.motifStage
        elif self.title == 'recursion':
            self.app.recursionDepth = app.recursionDepth
            self.stage = app.recursionDepth + 1
        elif self.title == 'bisectors':
            self.app.bisectorsOn = app.bisectorsOn
        elif self.title == 'mirror': 
            self.app.mirrorFractal = app.mirrorFractal
        # don't need to change these last two params because they're binary
  
def setButtonStartY(app):
    if app.buttonCount % 2 == 1:
        app.buttonStartY = app.height//2 - (app.buttonCount//2 * app.buttonSize)
    else:
        app.buttonStartY = (app.height//2 + app.buttonSize//2) - (app.buttonCount/2 * app.buttonSize)

def drawDashboard(app):
    if not app.tutorialFinished:
        drawTutorial(app)
    drawButtonsOOP(app)
    drawButtonBorder(app)

def drawTutorial(app):
    drawTutorialHeader(app)
    drawCurrTextbox(app)

def drawTutorialHeader(app):
    textL1 = "Not your first time?"
    textL2 = "Press 'enter' to skip the tutorial."
    drawRect(15, 15, 200, 50, fill='darkGrey', border='black', borderWidth=3)
    drawLabel(textL1, 15+(200/2), 15+(50/2)-8, bold=True)
    drawLabel(textL2, 15+(200/2), 15+(50/2)+8, bold=True)

def drawCurrTextbox(app):
    tutorialTexts = loadTutorialTexts()
    currText = tutorialTexts[app.tutorialStage]
    if app.tutorialStage <= 4: # walking through LHS buttons
        drawButtonTutorialBox(app, currText)
    elif app.tutorialStage == 5:
        drawSliderTutorialBox(app, currText)
    elif app.tutorialStage == 6:
        drawKnobTutorialBox(app, currText)
    elif app.tutorialStage == 7:
        drawCustomizationTutorialBox(app, currText)
    
def drawButtonTutorialBox(app, currText):
    buttonCY = getButtonCY(app, app.tutorialStage)
    cx, cy = app.buttonSize * 2.8, buttonCY
    drawRect(cx, buttonCY, 300, 150, fill='darkGrey', border='black', 
             borderWidth=3, align='center')
    drawCurrTextboxLabel(app, cx, cy, currText)

def drawSliderTutorialBox(app, currText):
    cx = app.sliderX1 + app.sliderLength//2
    cy = app.sliderY - 120 # play with this
    drawRect(cx, cy, 300, 150, fill='darkGrey', border='black', borderWidth=3,
             align='center')
    drawCurrTextboxLabel(app, cx, cy, currText)

def drawKnobTutorialBox(app, currText):
    cx = app.knobCX
    cy = app.sliderY - 120 # match previous textbox
    drawRect(cx, cy, 310, 150, fill='darkGrey', border='black', borderWidth=3,
             align='center')
    drawCurrTextboxLabel(app, cx, cy, currText)

def drawCustomizationTutorialBox(app, currText):
    cx = app.width - (app.buttonSize * 2.8)
    cy = app.height//2
    drawRect(cx, cy, 300, 150, fill='darkGrey', border='black', borderWidth=3,
             align='center')
    drawCurrTextboxLabel(app, cx, cy, currText)

def drawCurrTextboxLabel(app, cx, cy, currText):
    lineGap = 16
    startY = cy - (lineGap * 3) # 7 lines always, so 4th should be center 
    for i in range(7): # 7 lines
        lineText = currText[i]
        currY = startY + (lineGap * i)
        drawLabel(lineText, cx, currY, bold=True, size=14)

def drawButtonsOOP(app):
    loopBound = min(app.buttonCount, app.tutorialStage+1) 
    # min handles index error; +1 because i 0-counted the stage
    for i in range(loopBound):
        button = app.buttonList[i]
        fill = button.fill
        if app.selectedButton is button:
            fill = 'lightGray'
        drawRect(button.centerX, button.centerY, button.width, button.height, 
                 fill = fill, align = button.align, border = button.border)
        drawButtonLabelOOP(button)
    
def drawButtonLabelOOP(button):
    if (button.title == 'base') and (button.stage == 2):
            drawLine(button.centerX-40, button.centerY-5, button.centerX+40, 
                     button.centerY-5, fill='white', lineWidth=3)
            drawLine(button.centerX-40, button.centerY+5, button.centerX+40, 
                     button.centerY+5, fill='white', lineWidth=3)
    else:
        fractalWrapper(button.app)
    
def drawButtonBorder(app):
    stage = min(app.buttonCount, app.tutorialStage+1) # same as drawButtonsOOP
    drawRect(0, app.buttonStartY-app.buttonSize//2, app.buttonSize, 
             app.buttonSize * (stage), fill=None,
             border='black', borderWidth=4)
            # +1 on stage to avoid multiplying by 0

def isMouseOverButton(app, x, y):
    topEdge = app.buttonStartY - app.buttonSize//2
    if ((topEdge) < y < (topEdge + (app.buttonCount * app.buttonSize)) 
        and (x <= app.buttonSize)): # because vertical column
        return True     # Note: ^^leq for y causes index out of range error
    return False

def getHoveredButtonOOP(app, y):
    dy = y - (app.buttonStartY - app.buttonSize//2) 
        #  ^^startY weird because center aligned
    buttonNum = dy // app.buttonSize
    button = app.buttonList[buttonNum]
    return button

def updateDashboardButtons(app):
    for button in app.buttonList:
        button.reverseAdjustParam(app)

def mouseInTopHalf(app, button, mouseY):
    buttonNum = button.id
    buttonCY = getButtonCY(app, buttonNum)
    return mouseY <= buttonCY 

def getButtonCY(app, buttonNum):
    return ((app.buttonStartY) + (app.buttonSize * buttonNum))

def dashboardOMR(app, mouseX, mouseY):
    fractalOMR(app, mouseX, mouseY)

def dashboardOMD(app, mouseX, mouseY):
    pass

def dashboardOMM(app, mouseX, mouseY):
    if isMouseOverButton(app, mouseX, mouseY):
        button = getHoveredButtonOOP(app, mouseY)
        app.selectedButton = button
    else:
        app.selectedButton = None

def dashboardOMP(app, mouseX, mouseY):
    if app.justRandomized:
        updateDashboardButtons(app)
        app.justRandomized = False
    elif app.justReset:
        updateDashboardButtons(app)
        setHorzSlider(app)
        setKnobLineCoords(app)
        app.justReset = False
    if isMouseOverButton(app, mouseX, mouseY):
        button = getHoveredButtonOOP(app, mouseY)
        if app.tutorialFinished:
            adjustButtonAfterClick(app, button, mouseX, mouseY)
        else:
            if button.id == app.tutorialStage: 
                if mouseInTopHalf(app, button, mouseY):
                    button.incStage(app)
                    if not (button.title == 'base' and button.stage != 3):
                        app.tutorialStage += 1
                        # user must set base to triangle (two clicks)
                        if app.tutorialStage == 5:
                            resetFractalForTutorial(app)
                            updateDashboardButtons(app)        

def adjustButtonAfterClick(app, button, mouseX, mouseY):
    if mouseInTopHalf(app, button, mouseY):
        button.incStage(app)
    else:
        button.decStage(app)   

def dashboardOKP(app, key):
    if key == 'enter':
        app.tutorialStage = 7 # max tutorial stage
        app.tutorialFinished = True

def takeDashboardStep(app):
    pass

# ----------------------------------------------------------------------------

def onAppStart(app):
    app.width, app.height = 1000, 800
    setupFractalApp(app)
    setupCustomizationApp(app)
    setupHorzSliderApp(app)
    setupKnobApp(app)
    setupDashboardApp(app)

def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='green')
    # ^ makes white elements visible (for debugging/testing)
    drawDashboard(app)
    drawHorzSlider(app)
    drawKnob(app)
    drawLineCustomization(app)

def onMousePress(app, mouseX, mouseY):
    knobOMP(app, mouseX, mouseY)
    customOMP(app, mouseX, mouseY)
    dashboardOMP(app, mouseX, mouseY)

def onMouseDrag(app, mouseX, mouseY):
    dashboardOMD(app, mouseX, mouseY)

def onMouseMove(app, mouseX, mouseY):
    dashboardOMM(app, mouseX, mouseY)

def onMouseRelease(app, mouseX, mouseY):
    dashboardOMR(app, mouseX, mouseY)

def onKeyPress(app, key):
    dashboardOKP(app, key)

def onStep(app):
    takeDashboardStep(app)
    takeKnobStep(app)

def main():
    runApp()

if __name__ == '__main__':
    main()