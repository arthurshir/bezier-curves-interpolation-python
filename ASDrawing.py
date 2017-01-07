# ASDrawing
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import ASMath
import settings

# Colors
def getRgbTuple(hexString):
  h = hexString.lstrip('#')
  return tuple(float(int(h[i:i+2], 16))/255 for i in (0, 2 ,4))

def setHex(hexString):
  rgb = getRgbTuple(hexString)
  glColor3f(rgb[0], rgb[1], rgb[2])


# Low Level Drawing Functions
def draw_point(x, y):
    glColor3f(1,1,1)
    glPointSize(3);
    glBegin(GL_POINTS);
    glVertex2f(x , y);
    glEnd();

def draw_pointHighlighted(x,y):
    setHex('FC354C')
    glPointSize(10);
    glBegin(GL_POINTS);
    glVertex2f(x , y);
    glEnd();

def draw_line(xi, yi, xf,yf):
    glColor3f(1,1,1)
    glLineWidth(1)
    glBegin(GL_LINES)
    glVertex2f(xi , yi)
    glVertex2f(xf, yf)
    glEnd()





# Higher Level Drawing Functions
def drawControlPoints(points):
    if len(points) > 0:
        for i in range (0,len(points)):
            draw_point(points[i][0],points[i][1])

def drawControlPolygon(points):
    if len(points) > 1:
        for i in range (1,len(points)):
            draw_line(points[i - 1][0], points[i - 1][1], points[i][0], points[i][1])

def drawBernsteinBezierCurve(points):
    if len(points) > 2:
        for i in range(0, settings.interpolationNumber):
            x, y = ASMath.bernstein_generatePoint(float(i)/settings.interpolationNumber, points)
            draw_point(x, y)

def drawAitkenInterpolation(points):
    if len(points) > 2:
        for i in range(0, settings.interpolationNumber):
          x, y = ASMath.aitken_generatePoint(float(i)/settings.interpolationNumber, points, False)
          print "Drawing: ", x, y
          draw_point(x, y)

def drawSingleAitkenPoint(t, points):
  if len(points) > 2:
    x, y = ASMath.aitken_generatePoint(t, points, True)
    draw_pointHighlighted(x, y)

def drawElevatedOrReducedCurve(points, degreeOffset):
  if len(points) >= 2:
    if degreeOffset == 0:
      elevatedPoints = points
    elif degreeOffset > 0:
      elevatedPoints = ASMath.elevatedControlPointsMultiple(settings.points, degreeOffset)
    else:
      elevatedPoints = ASMath.reducedControlPointsMultiple(settings.points, degreeOffset)
    drawBernsteinBezierCurve(elevatedPoints)
    drawControlPolygon(elevatedPoints)
    for point in elevatedPoints:
      draw_pointHighlighted(point[0], point[1])

def drawHermiteInterpolation(points):
  if len(points) > 1:
    if len(settings.vectors) < len(points):
      for i in range(len(settings.vectors), len(points)):
        settings.vectors.append(ASMath.centralDifferenceVector(points[i-1], points[i], 2, 1))
      settings.vectors.append(settings.vectors[len(settings.vectors) - 1])

    vectors = settings.vectors
    for i in range(len(points)):
      draw_line(points[i][0], points[i][1], points[i][0] + vectors[i][0], points[i][1] + vectors[i][1])
    for n in range(1, len(points)):
      for i in range(0, settings.interpolationNumber):
        t = float(i)/settings.interpolationNumber
        x, y = ASMath.hermite_generatePoint(t, points[n - 1], points[n], vectors[n-1], vectors[n])
        draw_point(x, y)





