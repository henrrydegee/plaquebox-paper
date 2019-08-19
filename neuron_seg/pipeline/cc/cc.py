import numpy as np
import cv2
from itertools import chain

img = cv2.imread('../post_threshold_morphology_170.png', 0)	 
# store corresponding areas of each component, set thresholds of areas later on
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
# iterating all points 
for x in range(img.shape[0]):
	for y in range(img.shape[1]):
		if (cond_checker(x, y)):
			# first point of connected component
			w[x][y] = Set 
			test_points = points(x, y)
			# iterate while parts of connected components still detected
			while(len(test_points) > 0):
				# Initialize space to store next generation of test points
				temp = list()
				# looping through all the current test points			
				for (nx, ny) in test_points:
					if (cond_checker(nx, ny)):			
						w[nx][ny] = Set
						temp.append(points(nx, ny))
				# reset the test points
				temp = list(chain(*temp))
				test_points = temp
				# print(test_points)	
			Set += 1
cc = np.array(w)
cv2.imwrite("./cc.png", cc)
unique, counts = np.unique(cc, return_counts = True)
# print(dict(zip(unique, counts)))	 

