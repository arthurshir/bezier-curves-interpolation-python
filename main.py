from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import pygame
import math
import time

# My Modules
import settings
import ASDrawing 
import ASUI
import ASMath
import ASWindow



# Set initial Screen
def refresh2d(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def setBackground(hexString):
  rgb = ASDrawing.getRgbTuple(hexString)
  glClearColor(rgb[0], rgb[1], rgb[2], 0.0)


# Interface
def addControlPoint(x,y):
    settings.points.append([x, y])

def getCurvePoint(t, drawLine):
    pointsCopy = settings.points
    resultArray = pointsCopy
    while len(resultArray) > 1:
        resultArray = calculateNextLevel(resultArray, t, drawLine)
    return resultArray[0]


def draw():
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
  ASDrawing.drawControlPoints(settings.points)
  ASDrawing.drawControlPolygon(settings.points)

  ASDrawing.drawAitkenInterpolation(settings.points)
  ASDrawing.drawSingleAitkenPoint(settings.selectedT, settings.points)

  # ASDrawing.drawBernsteinBezierCurve(settings.points)
  # ASDrawing.drawElevatedOrReducedCurve(settings.points, settings.degreeOffset)

  glutSwapBuffers()




# Point Array Manipulation Functions
def getClosestPointIndex(x, y, points):
  minDistance = 8
  closestPointIndex = None
  if len(points) >= 1:
    for i in range(0, len(points)):
      if ASMath.distancePoints(x, y, points[i][0], points[i][1]) < minDistance:
        closestPointIndex = i
        minDistance = ASMath.distancePoints(x, y, points[i][0], points[i][1])
  return closestPointIndex




# Mouse Functions
lastMouseDown = None
currentDraggedPoint = None
selectedPointIndex = None
controlPointSelected = False
vectorSelected = False

def on_keyboard(key, x, y):
  if key == "+" or key == "=":
    settings.degreeOffset += 1
    print "up"
  elif key == "-":
    settings.degreeOffset -= 1
    print "down"
  draw()

def on_click(button, state, x, y):
    mouseX = x
    mouseY = settings.height - y
    vectorEndpoints = settings.getVectorEndpoints(settings.points, settings.vectors)
    global selectedPointIndex
    global controlPointSelected

    selectedPointIndex = getClosestPointIndex(mouseX, mouseY, settings.points)
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
      if selectedPointIndex == None:
        if getClosestPointIndex(mouseX, mouseY, vectorEndpoints) == None:
          controlPointSelected = False
          addControlPoint(mouseX, mouseY)
          selectedPointIndex = len(settings.points) - 1
          draw()
        else:
          selectedPointIndex = getClosestPointIndex(mouseX, mouseY, vectorEndpoints)
          if selectedPointIndex != None:
            controlPointSelected = False
            draw()
      else:
        controlPointSelected = True
    if button == GLUT_RIGHT_BUTTON:
      if selectedPointIndex != None:
        settings.points.pop(selectedPointIndex)
        draw()     

def on_drag(x, y):
  mouseX = x
  mouseY = settings.height - y
  global selectedPointIndex
  global controlPointSelected
  if len(settings.points) > 0:
    if controlPointSelected:
      settings.points[selectedPointIndex] = [mouseX, mouseY]
      draw()
    else:
      settings.vectors[selectedPointIndex] = settings.convertVectorEndpointToVector([mouseX, mouseY], settings.points[selectedPointIndex])
      draw()

def main():
  settings.init()
  glutInit()
  ASWindow.setupWindow()
  glutMouseFunc(on_click)
  glutMotionFunc(on_drag)
  glutKeyboardFunc(on_keyboard)
  glutDisplayFunc(draw)
   # glutIdleFunc(draw)
  app = QApplication(sys.argv)
  ex = ASUI.sliderdemo()
  ex.show()
  glutMainLoop()

if __name__ == "__main__": main()
