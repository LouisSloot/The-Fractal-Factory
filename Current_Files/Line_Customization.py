from cmu_graphics import *
from Fractal import *

def setupCustomizationApp(app):
    app.fractalColors = loadFractalColors()
    app.fractalColorIndex = 0
    app.panelWidth = 105  # same as dashboard button size
    app.maxFractalLineWidth = 4 # inclusive
    app.panelHeight = 5 * app.panelWidth
    app.customPanelLeft = app.width - app.panelWidth
    app.customPanelTop = 138

def loadFractalColors():
    return ['white',
            'red',
            'orange',
            'gold',
            'green',
            'mediumAquamarine',
            'blue',
            'midnightBlue',
            'darkOrchid',
            'hotPink',
            'peru'
            ]

def drawLineCustomization(app):
    drawPanelBorder(app)
    drawColorButton(app)
    drawWidthButton(app)
    drawDashButton(app)
    drawAutoSliderButton(app)
    drawAutoKnobButton(app)
    drawTrailsButton(app)
    drawRandomButton(app)
    drawResetButton(app)

def drawColorButton(app):
    left, top = app.customPanelLeft + 20, app.customPanelTop + 20
    width, height = 65, 65
    drawRect(left, top, width, height, fill=app.fractalFill, border='black', 
             borderWidth=3)

def checkColorPress(app, x, y):
    if ((app.customPanelLeft + 20 <= x <= app.customPanelLeft + 20 + 65) and 
        (app.customPanelTop + 20 <= y <= app.customPanelTop + 20 + 65)):
        app.fractalColorIndex += 1
        app.fractalColorIndex %= len(app.fractalColors)
        app.fractalFill = app.fractalColors[app.fractalColorIndex]

def drawWidthButton(app):
    left, top = app.customPanelLeft + 15, app.customPanelTop + 20 + 65 + 50
    right = app.width - 15
    drawLine(left, top, right, top, lineWidth=app.lineWidth,
             fill='white')
            # change fill (maybe) when testing in full app

def checkWidthPress(app, x, y):
    if ((app.customPanelLeft + 15 <= x <= app.width -15) and 
        (app.customPanelTop + 125 <= y <= app.customPanelTop + 145)):
        # +110 and +120 give some QOL cushioning on clicking the line
        app.lineWidth += 1
        app.lineWidth %= (app.maxFractalLineWidth + 1)
        # +1 makes my app variable an inclusive upper bound
        app.lineWidth = max(1, app.lineWidth) # can't have 0 width

def drawDashButton(app):
    left, top = app.customPanelLeft + 15, app.customPanelTop + 135 + 50
    right = app.width - 15
    drawLine(left, top, right, top, fill='white', dashes=app.dashes,
             lineWidth=4)
    
def checkDashPress(app, x, y):
    if ((app.customPanelLeft + 15 <= x <= app.width -15) and 
        (app.customPanelTop + 175 <= y <= app.customPanelTop + 195)):
        app.dashes = not app.dashes

def drawAutoSliderButton(app):
    left, top = app.customPanelLeft + 10, app.customPanelTop + 185 + 50
    width, height = 85, 40
    fill = 'darkGrey' if not app.autoSlider else 'red'
    drawRect(left, top, width, height, fill=fill, border='black',
             borderWidth=3)
    text = 'Slider'
    drawLabel(text, left+width//2, top+height//2, bold=True, size=22)

def checkAutoSliderPress(app, x, y):
    if ((app.customPanelLeft + 10 <= x <= app.width - 10) and 
        (app.customPanelTop + 235 <= y <= app.customPanelTop + 235 + 40)):
        app.autoSlider = not app.autoSlider

def drawAutoKnobButton(app):
    left, top = app.customPanelLeft + 10, app.customPanelTop + 235 + 40 + 20
    width, height = 85, 40
    fill = 'darkGrey' if not app.autoKnob else 'red'
    drawRect(left, top, width, height, fill=fill, border='black',
             borderWidth=3)
    text = 'Knob'
    drawLabel(text, left+width//2, top+height//2, bold=True, size=22)

def checkAutoKnobPress(app,x , y):
    if ((app.customPanelLeft + 10 <= x <= app.width - 10) and 
        (app.customPanelTop + 295 <= y <= app.customPanelTop + 295 + 40)):
        app.autoKnob = not app.autoKnob

def drawTrailsButton(app):
    left, top = app.customPanelLeft + 10, app.customPanelTop + 295 + 40 + 20
    width, height = 85, 40
    fill = 'darkGrey' if not app.trailsOn else 'red'
    drawRect(left, top, width, height, fill=fill, border='black',
             borderWidth=3)
    text = 'Trails'
    drawLabel(text, left+width//2, top+height//2, bold=True, size=22)

def checkTrailsPress(app, x, y):
    if ((app.customPanelLeft + 10 <= x <= app.width - 10) and 
        (app.customPanelTop + 355 <= y <= app.customPanelTop + 355 + 40)):
        app.trailsOn = not app.trailsOn

def drawRandomButton(app):
    left, top = app.customPanelLeft + 10, app.customPanelTop + 355 + 40 + 20
    width, height = 85, 40
    fill = 'darkViolet'
    drawRect(left, top, width, height, fill=fill, border='black',
             borderWidth=3)
    text = 'Random'
    drawLabel(text, left+width//2, top+height//2, bold=True, size=19)

def checkRandomPress(app,x , y):
    if ((app.customPanelLeft + 10 <= x <= app.width - 10) and 
        (app.customPanelTop + 415 <= y <= app.customPanelTop + 415 + 40)):
        randomizeParameters(app)
        app.justRandomized = True

def drawResetButton(app):
    left, top = app.customPanelLeft + 10, app.customPanelTop + 415 + 40 + 20
    width, height = 85, 40
    fill = 'fireBrick'
    drawRect(left, top, width, height, fill=fill, border='black',
             borderWidth=3)
    text = 'Reset'
    drawLabel(text, left+width//2, top+height//2, bold=True, size=22)

def checkResetPress(app, x, y):
    if ((app.customPanelLeft + 10 <= x <= app.width - 10) and 
        (app.customPanelTop + 475 <= y <= app.customPanelTop + 475 + 40)):
        app.tutorialFinished = True
        setupDefaultFractalApp(app)
        app.justReset = True

def drawPanelBorder(app):
    drawRect(app.customPanelLeft, app.customPanelTop, app.panelWidth, 
             app.panelHeight, fill=None, border='black', borderWidth=4)

def customOMP(app, mouseX, mouseY):
    checkColorPress(app, mouseX, mouseY)
    checkWidthPress(app, mouseX, mouseY)
    checkDashPress(app, mouseX, mouseY)
    checkAutoSliderPress(app, mouseX, mouseY)
    checkAutoKnobPress(app, mouseX, mouseY)
    checkTrailsPress(app, mouseX, mouseY)
    checkRandomPress(app, mouseX, mouseY)
    checkResetPress(app, mouseX, mouseY)

def customOMD(app, mouseX, mouseY):
    pass

def customOMM(app, mouseX, mouseY):
    pass

def customOMR(app, mouseX, mouseY):
    pass

def customOKP(app, key):
    pass

def takeCustomStep(app):
    pass

# ----------------------------------------------------------------------------

def onAppStart(app):
    app.width, app.height = 1000, 800
    setupCustomizationApp(app)

def redrawAll(app):
    drawLineCustomization(app)

def onMousePress(app, mouseX, mouseY):
    customOMP(app, mouseX, mouseY)

def onMouseDrag(app, mouseX, mouseY):
    customOMD(app, mouseX, mouseY)

def onMouseMove(app, mouseX, mouseY):
    customOMM(app, mouseX, mouseY)

def onMouseRelease(app, mouseX, mouseY):
    customOMR(app, mouseX, mouseY)

def onKeyPress(app, key):
    customOKP(app, key)

def onStep(app):
    takeCustomStep(app)

def main():
    runApp()

if __name__ == '__main__':
    main()