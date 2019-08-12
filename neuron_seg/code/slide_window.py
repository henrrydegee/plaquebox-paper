import cv2
import matplotlib.pyplot as plt
import numpy as np

# read the image and window in
overall_img = cv2.imread("../image/preprocessing_pipeline/transformed_img.png")
img_patch = cv2.imread("../image/preprocessing_pipeline/Neuron_patch.png")
print("rows: ", img_patch.shape[0])
print("cols: ", img_patch.shape[1])
print("rows: ", overall_img.shape[0])
print("cols: ", overall_img.shape[1])

# define step size and define window width and height
stepSize = 1
(w_width, w_height) = (img_patch.shape[1], img_patch.shape[0])

# initialize a matrix to hold score image
score_img = np.zeros((overall_img.shape[0] - w_height, overall_img.shape[1] - w_width))

for x in range(0, overall_img.shape[0] - w_height, stepSize):
	for y in range(0, overall_img.shape[1] - w_width, stepSize):
		#print(np.multiply(overall_img[x:x + w_width, y:y + w_height],img_patch))
		score_img[x, y] = np.sum(np.multiply(overall_img[x:x + w_height, y:y + w_width],img_patch))
		#print("x ", x)
		#print("y ", y)

# normalization on the score image value, normaize the maximum to 255
max_value = np.max(score_img)
score_img = score_img * 255 / max_value
cv2.imwrite('../image/preprocessing_pipeline/score_image.png', score_img)
# monitor the intensity distribution in the image
#print(np.max(score_img))
#print(np.min(score_img))

# generate different score image by examining different thresholds
img = cv2.imread('../image/preprocessing_pipeline/score_image.png', 0)
img2 = cv2.imread('../image/preprocessing_pipeline/threshold_original_160.png', 0)
# generate thresholded image for scores above 180
ret,thresh1 = cv2.threshold(img,180,255,cv2.THRESH_BINARY_INV)
# generate thresholded image for score above 220
ret,thresh2 = cv2.threshold(img,220,255,cv2.THRESH_BINARY_INV)
# generate thresholded image for score above 215
ret,thresh3 = cv2.threshold(img,215,255,cv2.THRESH_BINARY_INV)
# generate thresholded image for score above 205
ret,thresh4 = cv2.threshold(img,210,255,cv2.THRESH_BINARY_INV)
# generate thresholded image for score above 195
ret,thresh5 = cv2.threshold(img,195,255,cv2.THRESH_BINARY_INV)

titles = ['Original Image','180','220','215','210','195']
images = [img2, thresh1, thresh2, thresh3, thresh4, thresh5]

for i in range(6):
    plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])

plt.show()
