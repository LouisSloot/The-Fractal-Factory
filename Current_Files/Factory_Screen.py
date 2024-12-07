from cmu_graphics import *
from TP_Dash import *
from Horizontal_Slider import *
from Knob import *
from Back_Button import *

def drawFactoryScreen(app):
    drawFactoryBackground(app)
    drawBackButton(app)
    drawFractal(app)
    drawDashboard(app)
    if app.tutorialStage >= 5:
        drawHorzSlider(app)
    if app.tutorialStage >= 6:
        drawKnob(app)
    if app.tutorialStage >= 7:
        drawLineCustomization(app)

def drawFactoryBackground(app):
    path = './Control_Panel.png' 
    # image ^^ from https://stock.adobe.com/ (heavily edited by me)
    drawImage(path, 0, -290, width=1000, height=1200)
    # tedious offset to make image sit right

def factoryScreenOMP(app, mouseX, mouseY):
    sides = assignSides(app.motifStage)
    backButtonOMP(app, mouseX, mouseY)
    if not app.tutorialFinished:
        tutorialFactoryOMP(app, mouseX, mouseY, sides)
    else:
        horzSliderOMP(app, mouseX, mouseY, sides)
        knobOMP(app, mouseX, mouseY)
        customOMP(app, mouseX, mouseY)
    dashboardOMP(app, mouseX, mouseY)

def tutorialFactoryOMP(app, mouseX, mouseY, sides):
    if app.tutorialStage == 5:
        horzSliderOMP(app, mouseX, mouseY, sides)
    if app.tutorialStage == 6:
        knobOMP(app, mouseX, mouseY)
    if app.tutorialStage == 7:
        customOMP(app, mouseX, mouseY)

def factoryScreenOMD(app, mouseX, mouseY):
    sides = assignSides(app.motifStage)
    dashboardOMD(app, mouseX, mouseY)
    horzSliderOMD(app, mouseX, mouseY, sides)
    knobOMD(app, mouseX, mouseY)

def factoryScreenOMR(app, mouseX, mouseY):
    dashboardOMR(app, mouseX, mouseY)
    horzSliderOMR(app, mouseX, mouseY)
    knobOMR(app, mouseX, mouseY)

def factoryScreenOMM(app, mouseX, mouseY):
    dashboardOMM(app, mouseX, mouseY)
    horzSliderOMM(app, mouseX, mouseY)
    knobOMM(app, mouseX, mouseY)

def factoryScreenOKP(app, key):
    dashboardOKP(app, key)
    fractalOKP(app, key)

def takeFactoryStep(app):
    takeKnobStep(app)
    takeFractalStep(app)

# ----------------------------------------------------------------------------

def onAppStart(app):
    app.width, app.height = 1000, 800
    app.selectedScreen = None 
    setupKnobApp(app)
    setupFractalApp(app)
    setupCustomizationApp(app)
    setupHorzSliderApp(app)
    setupDashboardApp(app)

def redrawAll(app):
    drawFactoryScreen(app)

def onMousePress(app, mouseX, mouseY):
    factoryScreenOMP(app, mouseX, mouseY)

def onMouseDrag(app, mouseX, mouseY):
    factoryScreenOMD(app, mouseX, mouseY)

def onMouseMove(app, mouseX, mouseY):
    factoryScreenOMM(app, mouseX, mouseY)

def onMouseRelease(app, mouseX, mouseY):
    factoryScreenOMR(app, mouseX, mouseY)

def onKeyPress(app, key):
    factoryScreenOKP(app, key)

def onStep(app):
    takeFactoryStep(app)

def main():
    runApp()

if __name__ == '__main__':
    main()