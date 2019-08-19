import cv2
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

# Apply erosion and dilation of images on binary image

#img = np.array(Image.open("../image/unpreprocessing_pipline/NA4009-02_AB_10_10_14.jpg"),dtype=np.uint8)
img2 = np.array(Image.open("threshold_morphology_120.png"),dtype=np.uint8)

# generate thresholded image for score below 160

#ret, thresh = cv2.threshold(img, 160, 255, cv2.THRESH_BINARY_INV)

# arbitrarily design kernel size
# patch = cv2.imread('../image/preprocessing_pipeline/Neuron_patch.png')
# kernel = np.ones((patch.shape[0], patch.shape[1]), np.uint8)
kernel = np.ones((3,3),np.uint8) 

# erosion and diation operation demo
# original image applied to dilation and erosion
img_dilation = cv2.dilate(img2, kernel, iterations=1)
# img_erosion = cv2.erode(img_dilation, kernel, iterations=1)

# thresholded image applied to dilation and erosion
# img2_dilation = cv2.dilate(img2, kernel, iterations=1)
img2_erosion = cv2.erode(img2, kernel, iterations=1)

# thresholded binary image applied to dilation and erosion
img3_dilation = cv2.dilate(img2, kernel, iterations=1)
img3_erosion = cv2.erode(img3_dilation, kernel, iterations=2)

images = [img2, img_dilation, img2, img2_erosion, img2, img3_erosion]
titles = ['original image', "dilation", "original image", "erosion", "original image", "dilation+erosion"]

cv2.imwrite("dilation_erosion2.png", img3_erosion)

for i in range(6):
    plt.subplot(3,2,i+1),plt.imshow(images[i])
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])

plt.show()
