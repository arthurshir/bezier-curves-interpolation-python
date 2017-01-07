#ASMath.py
import math
import ASDrawing

# Single Point Generation
def hermite_generatePoint(t, point1, point2, vector1, vector2):
	s = t
	h1 = float(2*s**3) - 3*s**2 + 1
	h2 = float(-2*s**3) + 3*s**2
	h3 = float(s**3) - 2*s**2 + s
	h4 = float(s**3) -  s**2
	x = h1*point1[0] + h2*point2[0] + h3*vector1[0] + h4*vector2[0]
	y = h1*point1[1] + h2*point2[1] + h3*vector1[1] + h4*vector2[1]
	return [x, y]

def bernstein_generatePoint(t, points):
  bezierPoint = [0,0]
  n = len(points)
  for i in range(0, n):
    bern = bernstein_polynomialGenerator(n - 1, i, t)
    bezierPoint[0] += (points[i][0] * bern)
    bezierPoint[1] += (points[i][1] * bern)
  return bezierPoint

def aitken_generatePoint(t, points, showLines):
	layer = [points]
	tRatios = []
	tValues = [0]
	for i in range(1, len(layer[0])):
		L = distancePoints(layer[0][i][0], layer[0][i][1], layer[0][i-1][0], layer[0][i-1][1])
		tValues.append(tValues[-1] + L)

	for i in range(len(layer[0])):
		tRatios.append(tValues[i] / tValues[-1])

	for r in range(1, len(layer[0]) + 1):
		layer.append([])
		for i in range(0, len(layer[0]) - r):
			# print "Checking", (t - d[i])
			# print "Checking", (tRatios[i+r] - tRatios[i])
			# print "Checking", layer[r-1][i + 1][0]

			x = (tRatios[i+r] - t)/(tRatios[i+r] - tRatios[i])*layer[r - 1][i][0] + (t - tRatios[i])/(tRatios[i+r] - tRatios[i])*layer[r-1][i + 1][0]
			y = (tRatios[i+r] - t)/(tRatios[i+r] - tRatios[i])*layer[r - 1][i][1] + (t - tRatios[i])/(tRatios[i+r] - tRatios[i])*layer[r-1][i + 1][1]
			layer[r].append([x, y])
			if showLines:
				ASDrawing.draw_line(x, y, layer[r - 1][i][0], layer[r - 1][i][1])
		if showLines:
			for i in range(1, len(layer[r])):
				ASDrawing.draw_line(layer[r][i][0], layer[r][i][1], layer[r][i - 1][0], layer[r][i - 1][1])
	# print layer
	return layer[len(layer[0]) - 1][0][0], layer[len(layer[0]) - 1][0][1]


# Control Point Elevation / Reduction
def reducedControlPointsMultiple(points, degreeOffset):
	result = points
	for i in range(0, -(degreeOffset)):
		result = reducedControlPoints(result)
	return result

def reducedControlPoints(points):
	if len(points) >= 2:
		newPoints = [points[0]]
		n = len(points)
		for i in range(1, len(points) - 1):
			leftMultiplier = n / float(n - i)
			rightMultiplier = i / float(n - i)
			x = points[i][0]*leftMultiplier - newPoints[i - 1][0]*rightMultiplier
			y = points[i][1]*leftMultiplier - newPoints[i - 1][1]*rightMultiplier
			newPoints.append([x, y])
		return newPoints
	else:
		print points

def elevatedControlPointsMultiple(points, degreeOffset):
	result = points
	for i in range(0, degreeOffset):
		result = elevatedControlPoints(result)
	return result

def elevatedControlPoints(points):
	if len(points) >= 2:
		newPoints = [points[0]]
		for i in range(1, len(points)):
			multiplier = (float(i)/float(len(points)+1))
			x = points[i - 1][0]*multiplier + points[i][0]*(1 - multiplier)
			y = points[i - 1][1]*multiplier + points[i][1]*(1 - multiplier)
			newPoints.append([x, y])
		newPoints.append(points[len(points) - 1])
		return newPoints
	else:
		return points

#Calculations: 
def distancePoints(xi, yi, xf, yf):
	return math.sqrt( abs(xi - xf)**2 + abs(yi - yf)**2  )

def bernstein_polynomialGenerator(n, i, t):
	choose = float( math.factorial(n) )/( math.factorial(i) * math.factorial((n-i)) )
	return choose * (t**i) * (1-t)**(n-i)

def centralDifferenceVector(point1, point2, t1, t2):
	x = (point2[0] - point1[0])/ float(t2 - t1)
	y = (point2[1] - point1[1])/ float(t2 - t1)
	ratio = x/y
	dist = distancePoints(point1[0], point1[1], point2[0], point2[1])/2
	return [dist*ratio, dist/ratio]





