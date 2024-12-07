from cmu_graphics import *
import math
from Back_Button import *

def setupInfoApp(app):
    pass

def loadText():
    text = ['This is my final project for',
            '15-112, a CS course at CMU.',
            'My idea for this was heavily',
            "inspired by the website 'Nico's",
            "Fractal Machine', made by Nico",
            'Disseldorp. The emergent',
            'complexity of fractals from',
            'such simple conditions has',
            'always amazed me; I find',
            'visualizing this through a',
            'simple user interface to be',
            'powerful and engaging. Plus,',
            'it helped me freshen up on',
            'my trigonometry : )']
    return text

def drawInfoScreen(app):
    drawBGImage(app)
    drawInfoHeader(app)
    drawBGBox(app)
    drawText(app)
    drawHazardTapes(app)
    drawBackButton(app)

def drawBGBox(app):
    drawRect(app.width//2, app.height//2+50, 500, 500, fill='darkGrey',
             border='black', borderWidth=5, align='center')
    
def drawText(app):
    text = loadText()
    lines = len(text)
    lineGap = 30
    size = 30
    startY = app.height//2+50 - (lineGap * (lines-1)/2) # vertically centers
    for i in range(len(text)):
        line = text[i]
        currY = startY + (lineGap * i)
        drawLabel(line, app.width//2, currY, bold=True, size=size)

def drawInfoHeader(app):
    drawRect(app.width//2, 80, 640, 110, fill='yellow', border='black',
             borderWidth=5, align='center')
    text = 'About This Project'
    drawLabel(text, app.width//2, 80, size=60, bold=True)

def drawBGImage(app):
    path = './Info_Background.webp' 
    # from https://wallpapercave.com/industrial-wallpapers#google_vignette
    drawImage(path, 0, 0, width=1200, height=800)

def drawHazardTapes(app): 
    # can't just import from Home_Screen + not worth its own separate file
    width, height = 50, app.height
    stripWidth = int(width * math.sqrt(2))
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

def moreInfoOMP(app, mouseX, mouseY):
    backButtonOMP(app, mouseX, mouseY)

def moreInfoOMD(app, mouseX, mouseY):
    pass

def moreInfoOMM(app, mouseX, mouseY):
    pass

def moreInfoOMR(app, mouseX, mouseY):
    pass

def moreInfoOKP(app, key):
    pass

def takeInfoStep(app):
    pass

# ----------------------------------------------------------------------------

def onAppStart(app):
    app.width, app.height = 1000, 800
    setupInfoApp(app)

def redrawAll(app):
    drawInfoScreen(app)

def onMousePress(app, mouseX, mouseY):
    moreInfoOMP(app, mouseX, mouseY)

def onMouseDrag(app, mouseX, mouseY):
    moreInfoOMP(app, mouseX, mouseY)

def onMouseMove(app, mouseX, mouseY):
    moreInfoOMM(app, mouseX, mouseY)

def onMouseRelease(app, mouseX, mouseY):
    moreInfoOMP(app, mouseX, mouseY)

def onKeyPress(app, key):
    moreInfoOKP(app, key)

def onStep(app):
    takeInfoStep(app)

def main():
    runApp()

if __name__ == '__main__':
    main()