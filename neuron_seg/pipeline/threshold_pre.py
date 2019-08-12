import cv2
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

original_img = np.array(Image.open("image.jpg"),dtype=np.uint8)
original = original_img.copy()

# Preprocessing image to remove pixels above 170, which are commonly as background
original_img[original_img >= 170] = 255

plt.subplot(121),plt.imshow(original)
plt.title('Original Image'), plt.xticks([]), plt.yticks([])

cv2.imwrite("threshold_morphology_170.png", original_img)

plt.subplot(122),plt.imshow(original_img)
plt.title('Extracted Image'), plt.xticks([]), plt.yticks([])

plt.show()
