import cv2
import matplotlib.pyplot as plt
import argparse

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help='path to the image')
args = vars(ap.parse_args())

# generate histogram of the score image
score_img = cv2.imread(args["image"])

plt.hist(score_img.ravel(), 256, [0,256])
plt.show()

