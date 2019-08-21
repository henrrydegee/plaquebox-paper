
import numpy as np
import cv2
from itertools import chain
import matplotlib.pyplot as plt
import statistics
import math

img = cv2.imread('../post_threshold_morphology_120.png', 0)	 
# store corresponding areas of each component, set thresholds of areas later on
print(img)
w = np.zeros(img.shape)

dx = [-1, 0, 1, 1, 1, 0, -1, -1]
dy = [1, 1, 1, 0, -1, -1, -1, 0]

def points(x, y):
	coords = list()
	# generate 8 neighbors of a point
	for k in range(8):
		nx = x + dx[k]
		ny = y + dy[k]
		coords.append((nx, ny))
	return coords
	
def cond_checker(nx, ny):
	# boundary check for image
	if (nx >= 0 and nx < img.shape[0] and ny >= 0 and ny < img.shape[1]):
	# check if image component is already detected 
		if (img[nx][ny] and not(w[nx][ny])):
			return True

Set = 1
area = 0
set_area = {}
# iterating all points 
for x in range(img.shape[0]):
	for y in range(img.shape[1]):
		if (cond_checker(x, y)):
			# first point of connected component
			w[x][y] = Set 
			test_points = points(x, y)
			left = math.inf
			right = 0
			top = math.inf
			bottom = 0
			# iterate while parts of connected components still detected
			while(len(test_points) > 0):
				# Initialize space to store next generation of test points
				temp = list()
				# looping through all the current test points			
				for (nx, ny) in test_points:
					if (cond_checker(nx, ny)):			
						w[nx][ny] = Set
						temp.append(points(nx, ny))
						if (nx < left):
							left = nx
						if (nx > right):
							right = nx
						if (ny < top):
							top = ny
						if (ny > bottom):
							bottom = ny
				temp = list(chain(*temp))
				test_points = temp
				# print(test_points)	
			area = (bottom - top) * (right - left)
			set_area[Set] = area
			Set += 1

cc = np.array(w)
unique, counts = np.unique(cc, return_counts = True)
cc_stas = dict(zip(unique, counts))

print("max of those counts: ", max(counts))
print("min of those counts: ", min(counts))
print("median of those", statistics.median(counts))

"""
low_threshold = 30
high_threshold = 500
for key, value in cc_stas.items():
	if value > high_threshold or value < low_threshold:
		cc[cc == key] = 0	
"""

#plt.hist(np.array(counts), bins='auto')
#plt.gca().set(title='Area cc Histogram', ylabe,l='Frequency')
#plt.show()

# threshold this 2d array image if below certain value
#cc[cc >= 5000] = 0

high_area_thresh = 200
for key, value in set_area.items():
	if value > high_area_thresh:
		cc[cc == key] = 0

# print(set_area)
print("max of count: ", max(unique))
print("maximum set in the image: ", np.max(cc))
# cv2.imwrite("./ccbbox_300.png", cc)
cv2.imwrite("./ccbbox_200.png", cc)

