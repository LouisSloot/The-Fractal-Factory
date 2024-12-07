from cmu_graphics import *
import math
from Fractal import *
from TP_Dash import *

def setupHomeScreenApp(app):
    app.selectedScreen = 'Home'
    app.homeScreenPopupShowing = False
    
def drawHomeScreen(app):
    drawHomeScreenBackground(app)
    drawHazardTapes(app)
    drawAppTitle(app)
    drawScreenButtons(app)
    if app.homeScreenPopupShowing:
        drawLockedScreen(app)

def drawHazardTapes(app):
    width, height = 50, app.height
    stripWidth = int(width * math.sqrt(2)) # ?
    stripHeight = 10
    stripeNum = 15
    gap = app.height//stripeNum
    drawRect(0, 0, width, height, fill='yellow', border='black',
             borderWidth=6)
    drawRect(app.width-width, 0, width, height, fill='yellow', border='black',
             borderWidth=6)
    for i in range(stripeNum):
        y = i * gap
        drawRect(-13, y, stripWidth, stripHeight, rotateAngle=45, fill='black')
        drawRect(app.width-57, y, stripWidth, stripHeight, rotateAngle=135,
                 fill='black')
        # slightly-magic numbers that work : )

def drawHomeScreenBackground(app):
    path = './Metal_Background.jpg'
    # from https://stock.adobe.com/
    drawImage(path, -100, 0, width=1500, height=800)

def drawScreenButtons(app):
    freeGenScreenLabel = 'Research & Development'
    freeGenHeight = 100
    freeGenWidth = 480
    drawRect(app.width//2-freeGenWidth//2, app.height//2-170-freeGenHeight//2,
             freeGenWidth, freeGenHeight, fill='lightSlateGray', border='black',
             borderWidth = 3)
    drawLabel(freeGenScreenLabel, app.width//2, app.height//2-170, size=35, 
              bold=True)
    
    matchGameLabel = 'Production'
    matchGameHeight = 100
    matchGameWidth = 280
    drawRect(app.width//2-matchGameWidth//2, 
             app.height//2+50-matchGameHeight//2, matchGameWidth, 
             matchGameHeight, fill='darkSlateGray', border='black',
             borderWidth = 3)
    drawLabel(matchGameLabel, app.width//2, app.height//2+50, size=35, 
              bold=True)
    
    moreInfoLabel = 'More Info'
    moreInfoHeight = 100
    moreInfoWidth = 230
    drawRect(app.width//2-moreInfoWidth//2, app.height//2+270-moreInfoHeight//2,
             moreInfoWidth, moreInfoHeight, fill='darkGray', border='black',
             borderWidth = 3)
    drawLabel(moreInfoLabel, app.width//2, app.height//2+270, size=35, 
              bold=True)

def drawAppTitle(app):
    drawRect(app.width//2, 80, 640, 110, fill='yellow', border='black',
             borderWidth=5, align='center')
    text = 'The Fractal Factory!'
    drawLabel(text, app.width//2, 80, size=60, bold=True)

def drawLockedScreen(app):
    drawPopup(app)
    drawCloseBox(app)

def drawPopup(app):
    drawRect(app.width//2, app.height//2, 580, 200, fill='darkGrey', 
             border='black', borderWidth=5, align='center')
    line1 = "Hey! Not so fast..."
    line2 = "You need some training in RnD first."
    drawLabel(line1, app.width//2, app.height//2-30, size=30, bold=True) 
    drawLabel(line2, app.width//2, app.height//2+30, size=30, bold=True,
              italic=True)

def drawCloseBox(app): # a little different than matchGame's function
    drawRect(app.width//2, app.height//2+150, 200, 50, fill='darkGrey', 
             border='black', borderWidth=5, align='center')
    text = "Press 'enter' to close."
    drawLabel(text, app.width//2, app.height//2+150, size=15, bold=True)

def homeScreenOMP(app, mouseX, mouseY):
    buttonNum = getClickedHomeScreenButton(app, mouseX, mouseY)
    if buttonNum == 1:
        app.selectedScreen = 'Fractal'
    elif buttonNum == 2:
        if not app.tutorialFinished:
            app.homeScreenPopupShowing = True
        else:
            setupDefaultFractalApp(app)
            updateDashboardButtons(app)
            app.selectedScreen = 'MatchGame'
    elif buttonNum == 3:
        app.selectedScreen = 'MoreInfo'

def homeScreenOMD(app, mouseX, mouseY):
    pass

def homeScreenOMM(app, mouseX, mouseY):
    pass

def homeScreenOMR(app, mouseX, mouseY):
    pass

def getClickedHomeScreenButton(app, x, y):
    buttonNum = None
    if (((app.width//2)-(480/2) <= x <= (app.width//2)+(480/2)) and 
        ((app.height//2)-170-(100/2) <= y <= (app.height//2)-170+(100/2))):
        buttonNum = 1
    elif (((app.width//2)-(280/2) <= x <= (app.width//2)+(280/2)) and 
          ((app.height//2)+50-(100/2) <= y <= (app.height//2)+50+(100/2))):
        buttonNum = 2
    elif (((app.width//2)-(230/2) <= x <= (app.width//2)+(230/2)) and 
          ((app.height//2)+270-(100/2) <= y <= (app.height//2)+270+(100/2))):
        buttonNum = 3
    return buttonNum

def homeScreenOKP(app, key):
    if key =='enter':
        if app.homeScreenPopupShowing:
            app.homeScreenPopupShowing = False

def takeHomeStep(app):
    pass

# ----------------------------------------------------------------------------

def onAppStart(app):
    app.width, app.height = 1000, 800

def redrawAll(app):
    drawHomeScreen(app)

def onMousePress(app, mouseX, mouseY):
    homeScreenOMP(app, mouseX, mouseY)

def onMouseDrag(app, mouseX, mouseY):
    homeScreenOMD(app, mouseX, mouseY)

def onMouseMove(app, mouseX, mouseY):
    homeScreenOMM(app, mouseX, mouseY)

def onMouseRelease(app, mouseX, mouseY):
    homeScreenOMR(app, mouseX, mouseY)

def onKeyPress(app, key):
    homeScreenOKP(app, key)

def onStep(app):
    takeHomeStep(app)

def main():
    runApp()

if __name__ == '__main__':
    main()