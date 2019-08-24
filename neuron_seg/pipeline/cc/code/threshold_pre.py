import cv2
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import glob
import os 



for j in range(31):
	folder_path = "../norm_tiles/NA3777-02_AB/0/"+str(j)+"/neuron_seg"
	# create a folter neuron_seg to store all the preprocessing image
	try:
		os.mkdir(folder_path)
	except OSError:
		print("Folder is already created ", str(j))
	else:
		print("Successfully created the directory ", str(j))	
	
	image_list = []
	read_path = "../norm_tiles/NA3777-02_AB/0/"+str(j)+"/*.jpg"
	# first read in all section in large image slide, has 30 sections in total
	for filename in glob.glob(read_path):
		im = np.array(Image.open(filename),dtype=np.uint8)
		image_list.append(im)

	i = 0
	for original_img in image_list:
		original = original_img.copy()
		quartile = np.percentile(original_img, 10) 
		# Preprocessing image to remove pixels above 170, which are commonly as background
		original_img[original_img >= quartile] = 255

		# turn background to black and grayscale the post processing image
		ret,thresh = cv2.threshold(original_img,254,255,cv2.THRESH_BINARY_INV)
		gray = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
		savepath = "../norm_tiles/NA3777-02_AB/0/"+str(j)+"/neuron_seg/post_threshold_morphology_170_" + str(i) + ".png"
		cv2.imwrite(savepath, gray)
		i = i + 1
