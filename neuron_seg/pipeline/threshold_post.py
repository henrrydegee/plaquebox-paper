import cv2
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from skimage import io

original_img = np.array(Image.open("dilation_erosion2.png"))
original = original_img.copy()

# remove plaque pixels which based on experiments are around 130
original_img[original_img <= 130] = 255

plt.subplot(121),plt.imshow(original)
plt.title('Original Image'), plt.xticks([]), plt.yticks([])

# turn background to black and grayscale the post processing image
ret,thresh = cv2.threshold(original_img,254,255,cv2.THRESH_BINARY_INV)
gray = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
cv2.imwrite("post_threshold_morphology_170.png", gray)

plt.subplot(122),plt.imshow(original_img)
plt.title('Extracted Image'), plt.xticks([]), plt.yticks([])

plt.show()
