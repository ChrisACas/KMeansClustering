#!/usr/bin/python
from PIL import Image, ImageStat
import numpy


# =========
# converged
# =========
#
# Will determine if the centroids have converged or not.
# Essentially, if the current centroids and the old centroids
# are virtually the same, then there is convergence.
#
# Absolute convergence may not be reached, due to oscillating
# centroids. So a given range has been implemented to observe
# if the comparisons are within a certain ballpark
#


def converged(centroids, old_centroids):
	if len(old_centroids) == 0:
		return False


	if len(centroids) <= 5:
		a = 1
	elif len(centroids) <= 10:
		a = 2
	else:
		a = 4

	for i in range(0, len(centroids)):
		cent = centroids[i]
		old_cent = old_centroids[i]

		if ((int(old_cent[0]) - a) <= cent[0] <= (int(old_cent[0]) + a)) and ((int(old_cent[1]) - a) <= cent[1] <= (int(old_cent[1]) + a)) and ((int(old_cent[2]) - a) <= cent[2] <= (int(old_cent[2]) + a)):
			continue
		else:
			return False

	return True

#end converged


# ======
# getMin
# ======
#
# Method used to find the closest centroid to the given pixel.
#
def getMin(pixel, centroids):
	minDist = 9999
	minIndex = 0

	for i in range(0, len(centroids)):
		d = numpy.sqrt(int((centroids[i][0] - pixel[0]))**2 + int((centroids[i][1] - pixel[1]))**2 + int((centroids[i][2] - pixel[2]))**2)
		if d < minDist:
			minDist = d
			minIndex = i

	return minIndex
#end getMin




# ============
# assignPixels
# ============
def assignPixels(centroids):
        clusters = {}

        ## Write your code here
        return clusters

#end assignPixels



# ===============
# adjustCentroids
# ===============

def adjustCentroids(clusters):
	new_centroids = []

        ## Write your code here
	return new_centroids

#end adjustCentroids


# ===========
# initializeKmeans
# ===========
#
# Used to initialize the k-means clustering
#
def initializeKmeans(someK):
	centroids = []

	## Write your code here
	

	print("Centroids Initialized")
	print("===========================================")

	return centroids
#end initializeKmeans





# ===========
# iterateKmeans
# ===========
#
# Used to iterate the k-means clustering
#
def iterateKmeans(centroids):
	old_centroids = []
	print("Starting Assignments")
	print("===========================================")

	## Write your code here
	
	print("===========================================")
	print("Convergence Reached!")
	return centroids
#end iterateKmeans


# ==========
# drawWindow
# ==========
#
# Once the k-means clustering is finished, this method
# generates the segmented image and opens it.
#
def drawWindow(result):
	img = Image.new('RGB', (img_width, img_height), "white")
	p = img.load()

	for x in range(img.size[0]):
		for y in range(img.size[1]):
			RGB_value = result[getMin(px[x, y], result)]
			p[x, y] = RGB_value

	img.show()

#end drawWindow



num_input = str(input("Enter image number: "))
k_input = int(input("Enter K value: "))

img = "img/test" + num_input.zfill(2) + ".jpg"
im = Image.open(img)
img_width, img_height = im.size
px = im.load()
initial_centroid=initializeKmeans(k_input)
result = iterateKmeans(initial_centroid)
drawWindow(result)




