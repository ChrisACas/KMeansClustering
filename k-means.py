#!/usr/bin/python
from PIL import Image, ImageStat
import numpy as np
import random

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
		d = np.sqrt(int((centroids[i][0] - pixel[0]))**2 + int((centroids[i][1] - pixel[1]))**2 + int((centroids[i][2] - pixel[2]))**2)
		if d < minDist:
			minDist = d
			minIndex = i

	return minIndex
#end getMin


def assignPixels(centroids:list) -> dict:
	"""Groups pixels and assigns to closes centroid

	Args:		list containing centroid coords

	Returns:	dict with keys being centroid 
		and vals being pixels closest to that centroid
	"""
	clusters = dict.fromkeys(centroids)

	for h in range(img_height):
		for w in range(img_width):
			closest_centroid = getMin(px[h, w], centroids)
			clusters[closest_centroid] = px[h, w]

	return clusters	


def adjustCentroids(clusters: dict) -> list:
	"""Recenter the centroid using the mean average of each clusters pixels

	Args: 		dict of centroids with assigned pixels {centroid: [pixel list]}

	Returns:	list of new centroid coords
	"""
	new_centroids = []
	
	for old_centroid, pixels in clusters.items(): 
		new_centroids += tuple(np.mean(pixels, axis=0))

	return new_centroids


def initializeKmeans(k: int) -> list:
	"""Create a list of k number of centroids by randomly sampling pixels

	Args: 		k int representing number of clusters

	Returns: 	list of centroids
	"""
	centroids = []

	for i in range(k): 
		random_pixel = px[random.randint(0, img_width), random.randint(0, img_height)]
		centroids += random_pixel

	print("Centroids Initialized")
	print("===========================================")

	return centroids


def iterateKmeans(centroids: list) -> list:
	"""Iterate the k-means clustering steps for <= 20 steps or for convergence

	Args:		list of old centroids

	Returns:  	list of centroids (final result)
	"""
	old_centroids = []
	print("Starting Assignments")
	print("===========================================")
	
	for i in range(20):
		
		if converged(old_centroids, centroids):
			break
	
	print("===========================================")
	print("Convergence Reached!")
	return centroids

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


num_input = str(3)	# str(input("Enter image number: "))
k_input = 4			# int(input("Enter K value: "))

img = "img/test" + num_input.zfill(2) + ".jpg"
im = Image.open(img)
img_width, img_height = im.size
px = im.load()
initial_centroid=initializeKmeans(k_input)
print(initial_centroid)
# result = iterateKmeans(initial_centroid)
# drawWindow(result)
print(type(px[3,4]))
test_centroid = (3, 4, 5)
test_pixels = [(1, 2, 2), (2, 1, 1), (3, 3, 3), (4, 4, 4)]
test_cluster = {test_centroid: test_pixels}

new_test_centroic = adjustCentroids(test_cluster)


