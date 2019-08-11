import cv2
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

original_img = np.array(Image.open("../image/NA4009-02_AB_10_10_14.jpg"),dtype=np.uint8)
original = original_img.copy()

#original_img[original_img < 60] = 255
original_img[original_img >= 170] = 255

plt.subplot(121),plt.imshow(original)
plt.title('Original Image'), plt.xticks([]), plt.yticks([])

cv2.imwrite("../image/preprocessing/threshold_original_170.png", original_img)

plt.subplot(122),plt.imshow(original_img)
plt.title('Extracted Image'), plt.xticks([]), plt.yticks([])

plt.show()
