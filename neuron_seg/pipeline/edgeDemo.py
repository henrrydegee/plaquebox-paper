import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('./image.jpg', 0)
# currently, using Otsu's method is not necessary 
# high_thresh1, thresh_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# lowThresh1 = 0.5*high_thresh1
# Based on openCV documentation, choose low threshold as 180 and high as 2oo
edges = cv2.Canny(img, 180, 200)

plt.title('Colored Overall Image'), plt.xticks([]), plt.yticks([])
plt.subplot(221),plt.imshow(img,cmap = 'gray')
plt.title('Overall Image'), plt.xticks([]), plt.yticks([])
plt.subplot(222),plt.imshow(edges,cmap = 'gray')
plt.title('Overall Edge Image'), plt.xticks([]), plt.yticks([])
cv2.imwrite("../image/preprocessing_pipeline/overall_edge.png", edges)

img2 = cv2.imread('./neuron.png', 0)
# with arbitrary threshold
edges2 = cv2.Canny(img2, 180, 200)

#plt.subplot(321), plt.imshow(img2, cmap = 'gray')
#plt.title('Colored patch'), plt.xticks([]), plt.yticks([])

#high_thresh2, thresh_img2 = cv2.threshold(img2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#lowThresh2 = 0.5*high_thresh2
# with new threshold
#edges_new = cv2.Canny(img2, lowThresh2, high_thresh2)
#print("low threshold: ", lowThresh2)
#print("high threshold: ", high_thresh2)

#plt.subplot(322), plt.imshow(edges_new)
#plt.title('Colored patch'), plt.xticks([]), plt.yticks([])

plt.subplot(223),plt.imshow(img2,cmap = 'gray')
plt.title('Neuron Image'), plt.xticks([]), plt.yticks([])
plt.subplot(224),plt.imshow(edges2,cmap = 'gray')
plt.title('Neuron Edge Image'), plt.xticks([]), plt.yticks([])
cv2.imwrite("../image/preprocessing_pipeline/Neuron_patch.png", edges2)

plt.show()


