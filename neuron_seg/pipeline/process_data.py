import numpy as np
from PIL import Image

# unit testing using print

image = np.array(Image.open("post_threshold_morphology_170.png"),dtype=np.uint8)
datapoints = np.where(image != 0)
# print(datapoints)


