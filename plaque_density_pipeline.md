# Pipeline for white_grey_matter segmentation & plague-density calculation

#### Preprocssing of data image
* Need to get rid of the useless pixels during the preprocessing. Goal is to only contain useful organism, which contains grey and white matters.
* Since the distribution of grey matter and white matter are similiar to the shape of "concentric circle". Therefore, if we want to apply k-means in the regular manner, we need to split the original image into two, in a way we can locate centers of grey and white matter easily.
* Consult histogram of the current image, removing irrelavant pixels according to their intensity(too high or too low).

#### Extract "neuron" in processed image
* Design a window size which is similar to the neuron size in the image.
* Design several different masks which have several different shapes of neuron in the window.
* Distance transform on the original image.
* Use Chamfier distance of several different oriented masks to get the score of local region <br> (original image size is shrinked).
* Based on the score of local region, threshold local score value, only neuron locations <br> are left on the image. Otherwise, white space.

#### Apply K-means in the post-score-threshold image
* Select two centers on the post-score-threshold image.
* Apply k-means algorithm to spread region and draw a curve in between for demonstration.

#### Project centers on the heatmap image
* Project two centers in post-score-threshold image to heatmap image.

#### Calculate plague-white-grey density distribution on the heatmap
* Based on the specific intensity to distinguish plague, use morphological operator(closing) to <br> extract single plague.
* Based on plague-center distance, group plagues into white, gray regions.
* Calculate plague-white, plague-grey density.
* Further calculate specifc-plaque-white, specifc-plague-grey density based <br> on above algorithm.
