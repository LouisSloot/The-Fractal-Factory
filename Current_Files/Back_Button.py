from cmu_graphics import *

def drawBackButton(app):
    drawRect(20, app.height-57, 75, 37, fill='dimGray', border='black',
             borderWidth=3)
    drawLabel('Back', 20+37, app.height-39, size=15, bold=True)

def backButtonOMP(app, x, y):
    if (20 <= x <= 20+75) and (app.height-57 <= y <= app.height-57+37):
        app.selectedScreen = 'Home'

# ----------------------------------------------------------------------------

def onAppStart(app):
    app.width, app.height = 1000, 800
    app.selectedScreen = None

def redrawAll(app):
    drawBackButton(app)

def onMousePress(app, mouseX, mouseY):
    backButtonOMP(app, mouseX, mouseY)

def main():
    runApp()

if __name__ == '__main__':
    main()