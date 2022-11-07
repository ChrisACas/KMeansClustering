#!/usr/bin/python
from PIL import Image, ImageStat
import numpy as np
import random
import matplotlib.pyplot as plt
from tqdm import tqdm
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


def getMin(pixel, centroids):
	"""Find and return the centroid that has the smalled distance to each pixel

	Args: 		pixel and list of centroids 

	Return: 	centroid with the minimum distance to the pixel
	"""
	minDist = 9999
	minIndex = 0
	
	for i in range(0, len(centroids)):
		d = np.sqrt(int((centroids[i][0] - pixel[0]))**2 + int((centroids[i][1] - pixel[1]))**2 + int((centroids[i][2] - pixel[2]))**2)
		if d < minDist:
			minDist = d
			minIndex = i

	return centroids[minIndex]


def assignPixels(centroids:list) -> dict:
	"""Groups pixels and assigns to closes centroid

	Args:		list containing centroid coords

	Returns:	dict with keys being centroid 
		and vals being pixels closest to that centroid
	"""
	clusters = dict.fromkeys(centroids)

	# initialize values in dict as list()
	for key in clusters:
		clusters[key] = list()

	for h in range(img_height):
		for w in range(img_width):
			closest_centroid = getMin(px[w, h], centroids)
			clusters[closest_centroid] += tuple(px[w, h]),

	return clusters	

def adjustCentroids(clusters: dict) -> list:
	"""Recenter the centroid using the mean average of each clusters pixels

	Args: 		dict of centroids with assigned pixels {centroid: [pixel list]}

	Returns:	list of new centroid coords
	"""
	new_centroids = []

	for old_centroid, pixels in clusters.items(): 
		new_centroids += tuple(np.mean(pixels, axis=0)),

	return new_centroids


def initializeKmeans(k: int) -> list:
	"""Create a list of k number of centroids by randomly sampling pixels

	Args: 		k int representing number of clusters

	Returns: 	list of centroids
	"""
	centroids = []

	for i in range(k): 
		random_pixel = px[random.randint(0, img_width-1), random.randint(0, img_height-1)]
		centroids += (random_pixel),

	return centroids


def iterateKmeans(centroids: list) -> list:
	"""Iterate the k-means clustering steps for <= 20 steps or for convergence

	Args:		initial list of centroics

	Returns:  	list of centroids (final result)
	"""
	old_centroids = centroids
	
	for i in range(20):
		clusters = assignPixels(old_centroids)
		centroids = adjustCentroids(clusters)

		if converged(centroids, old_centroids):
			break
		old_centroids = centroids

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
			RGB_value = getMin(px[x, y], result)
			p[x, y] = tuple([int(i) for i in list(np.round_(np.array(RGB_value)))])

	img.show()

def objectiveFunction(centroids: list) -> float: 
	"""Optimization criterion is to minimize total sqaured error
			between pixels and centroids

		Args: list of centroids, then used to make clusters 

		Returns: Summation of the squared errors between pixels and centroid
	"""
	clusters = assignPixels(centroids)
	SE_centroid = []
	for centroid, pixels in clusters.items():
		# Kmeans objective function
		SE_centroid += np.sum( np.sum ( np.subtract(pixels, centroid) **2, axis=0 ) ),
	

	Total_SE = np.sum(SE_centroid)
	return Total_SE

def elbowPlot():
	x = []
	y = []

	for k in tqdm(range(1, 10)):
		x += k,
		k_centroids=initializeKmeans(k)
		k_result = iterateKmeans(k_centroids)
		y += -objectiveFunction(k_result),
	
	plt.xlabel("k Clusters")
	plt.ylabel("Total Squared Error")
	plt.setTitle("Elbow Plot")
	plt.plot(x, y)
	plt.show()

num_input = str(input("Enter image number: "))
k_input = int(input("Enter K value: "))

img = "img/test" + num_input.zfill(2) + ".jpg"
im = Image.open(img)
img_width, img_height = im.size
px = im.load()
initial_centroid=initializeKmeans(k_input)
result = iterateKmeans(initial_centroid)
drawWindow(result)
elbowPlot()

# Some Testing

# print(type(px[3,4]))
# test_centroid = (3, 4, 5)
# test_pixels = [(1, 2, 2), (2, 1, 1), (3, 16, 3), (4, 4, 4)]
# test_cluster = {test_centroid: test_pixels}

# # new_test_centroic = adjustCentroids(test_cluster)
# print(tuple(np.mean(test_pixels, axis=0)))

