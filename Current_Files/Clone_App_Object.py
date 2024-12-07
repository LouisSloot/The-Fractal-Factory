from types import SimpleNamespace

def makeAppClone(fractalCenter, sideLength, dashes, baseStructureSides, 
                 recursionDepth, motifStage, mirrorFractal, 
                 bisectorsOn, lineWidth, width, height, fractalRotation, 
                 fractalOpacity, scalableAngle, defaultScalableAngle, 
                 maxScalableAngle, fractalFill):
    clone = SimpleNamespace()
    clone.fractalCenter = fractalCenter
    clone.sideLength = sideLength
    clone.trailsOn = False # don't want clones of clones
    clone.dashes = dashes
    clone.recursionDepth = recursionDepth
    clone.motifStage = motifStage
    clone.mirrorFractal = mirrorFractal
    clone.baseStructureSides = baseStructureSides
    clone.bisectorsOn = bisectorsOn
    clone.lineWidth = lineWidth
    clone.width = width
    clone.height = height
    clone.fractalRotation = fractalRotation
    clone.fractalOpacity = fractalOpacity
    clone.scalableAngle = scalableAngle
    clone.defaultScalableAngle = defaultScalableAngle
    clone.maxScalableAngle = maxScalableAngle
    clone.fractalFill = fractalFill
    return clone

