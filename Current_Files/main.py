from Factory_Screen import *
from Home_Screen import *
from Match_Game import *
from More_Info import *

# BIG citation to the website "Nico's Fractal Machine"
# Found here: https://sciencevsmagic.net/fractal/#0060,0090,1,1,0,0,1
# Freeplay (RnD) mode is largely my own rendition of Nico's amazing software;
# though I did make some notable changes in the specifics of generating the 
# fractals, this project would not have been possible without Nico's website
# as visual inspiration and high-level guidance. I also cite his work on the
# 'More Info' screen within my actual program.

# Note: 
# At the bottom of all files (except main.py), there is a dashed line
# that separates some code from the rest of the file. The code below this 
# dashed line is scaffolding that is useful to run each file individually for 
# debugging purposes. Hence, this code could be deleted, and the program
# would work the same IF run from main.py. This also means some of the imports 
# at the top of each file do not impact overall functionality. Similarly, 
# there are also a handful of functions defined across the files that just pass 
# and do nothing; I wrote and am choosing to include these because they make my 
# program more extensible, e.g. it would save future development time if I 
# chose to add some onMouseDrag functionality to the Home Screen. Again, these 
# do not currently impact the functionality of the project.

def onAppStart(app):
    setupMainApp(app)

def setupMainApp(app):
    app.width, app.height = 1000, 800
    setupFractalApp(app)
    setupKnobApp(app)
    setupCustomizationApp(app)
    setupHorzSliderApp(app)
    setupHomeScreenApp(app)
    setupDashboardApp(app)
    setupMatchGameApp(app)
    
def redrawAll(app):
    drawMain(app)

def drawMain(app):
    if app.selectedScreen == 'Home':
        drawHomeScreen(app)
    elif app.selectedScreen == 'Fractal':
        drawFactoryScreen(app)
    elif app.selectedScreen == 'MatchGame':
        drawMatchGameScreen(app)
    elif app.selectedScreen == 'MoreInfo':
        drawInfoScreen(app)

def onMousePress(app, mouseX, mouseY):
    mainOMP(app, mouseX, mouseY)

def mainOMP(app, mouseX, mouseY):
    if app.selectedScreen == 'Home':
        homeScreenOMP(app, mouseX, mouseY)
    elif app.selectedScreen == 'Fractal':
        factoryScreenOMP(app, mouseX, mouseY)
    elif app.selectedScreen == 'MatchGame':
        matchGameOMP(app, mouseX, mouseY)
    elif app.selectedScreen == 'MoreInfo':
        moreInfoOMP(app, mouseX, mouseY)

def onMouseDrag(app, mouseX, mouseY):
    mainOMD(app, mouseX, mouseY)

def mainOMD(app, mouseX, mouseY):
    if app.selectedScreen == 'Home':
        homeScreenOMD(app, mouseX, mouseY)
    elif app.selectedScreen == 'Fractal':
        factoryScreenOMD(app, mouseX, mouseY)
    elif app.selectedScreen == 'MatchGame':
        matchGameOMD(app, mouseX, mouseY)
    elif app.selectedScreen == 'MoreInfo':
        moreInfoOMD(app, mouseX, mouseY) 

def onMouseMove(app, mouseX, mouseY):
    mainOMM(app, mouseX, mouseY)

def mainOMM(app, mouseX, mouseY):
    if app.selectedScreen == 'Home':
        homeScreenOMM(app, mouseX, mouseY)
    elif app.selectedScreen == 'Fractal':
        factoryScreenOMM(app, mouseX, mouseY)
    elif app.selectedScreen == 'MatchGame':
        matchGameOMM(app, mouseX, mouseY)
    elif app.selectedScreen == 'MoreInfo':
        moreInfoOMM(app, mouseX, mouseY)

def onMouseRelease(app, mouseX, mouseY):
    mainOMR(app, mouseX, mouseY)

def mainOMR(app, mouseX, mouseY):
    if app.selectedScreen == 'Home':
        homeScreenOMR(app, mouseX, mouseY)
    elif app.selectedScreen == 'Fractal':
        factoryScreenOMR(app, mouseX, mouseY)
    elif app.selectedScreen == 'MatchGame':
        matchGameOMR(app, mouseX, mouseY)
    elif app.selectedScreen == 'MoreInfo':
        moreInfoOMR(app, mouseX, mouseY)

def onKeyPress(app, key):
    mainOKP(app, key)

def mainOKP(app, key):
    if app.selectedScreen == 'Home':
        homeScreenOKP(app, key)
    elif app.selectedScreen == 'Fractal':
        factoryScreenOKP(app, key)
    elif app.selectedScreen == 'MatchGame':
        matchGameOKP(app, key)
    elif app.selectedScreen == 'MoreInfo':
        moreInfoOKP(app, key)

def onStep(app):
    takeMainStep(app)

def takeMainStep(app):
    if app.selectedScreen == 'Home':
        takeHomeStep(app)
    elif app.selectedScreen == 'Fractal':
        takeFactoryStep(app)
    elif app.selectedScreen == 'MatchGame':
        takeMatchGameStep(app)
    elif app.selectedScreen == 'MoreInfo':
        takeInfoStep(app)

def main():
    runApp()

if __name__ == '__main__':
    main()