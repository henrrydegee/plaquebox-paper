import cv2
import matplotlib.pyplot as plt

# generate histogram of the score image
score_img = cv2.imread('score_image.png', 0)

plt.hist(score_img.ravel(), 256, [0,256])
plt.show()

