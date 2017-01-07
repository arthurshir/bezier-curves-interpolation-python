# settings.py

def init():
	global window, width, height, points, vectors, showLineSegments, interpolationNumber, selectedT, splitLine, degreeOffset
	window = 0
	width, height = 1000, 700
	points = []
	vectors = []
	showLineSegments = False
	interpolationNumber = 100
	selectedT = 0.5
	splitLine = False
	degreeOffset = 0

def getVectorEndpoints(points, vectors):
	endPoints = []
	for i in range(min(len(points), len(vectors))):
		endPoints.append([points[i][0] + vectors[i][0], points[i][1] + vectors[i][1]])
	return endPoints

def convertVectorEndpointToVector(vectorEndpoint, point):
	return vectorEndpoint[0] - point[0], vectorEndpoint[1] - point[1]