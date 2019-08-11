import cv2
from PIL import Image
import numpy as np
from scipy import ndimage

# load image in as nd array, normalized it by dividing by 255
im_overall = np.array(Image.open("overall_edge.png"),dtype=np.uint8) / 255
im_patch = np.array(Image.open("Neuron_patch.png"),dtype=np.uint8) / 255 

# transform data to fit chamfer distance, where edge points will be 0s
im_overall = 1 - im_overall

im_transform = ndimage.distance_transform_edt(im_overall)

# save the transformed image
cv2.imwrite("transformed_img.png", im_transform)

# testing if image is chamfer distance transformed
print(im_overall)
print(im_transform)

# set stepsize equals to 1
#for y in range(0, im_overall.shape[0], 1):
#	for x in range(0, im_overall.shape[1], 1):

