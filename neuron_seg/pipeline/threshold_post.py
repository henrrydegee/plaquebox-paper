import cv2
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

original_img = np.array(Image.open("dilation_erosion2.png"),dtype=np.uint8)
original = original_img.copy()

# remove plaque pixels which based on experiments are around 130
original_img[original_img <= 130] = 255

plt.subplot(121),plt.imshow(original)
plt.title('Original Image'), plt.xticks([]), plt.yticks([])

cv2.imwrite("post_threshold_morphology_170.png", original_img)

plt.subplot(122),plt.imshow(original_img)
plt.title('Extracted Image'), plt.xticks([]), plt.yticks([])

plt.show()
