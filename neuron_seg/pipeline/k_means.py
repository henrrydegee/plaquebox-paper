import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.metrics.pairwise import pairwise_distances_argmin
# unit testing using print

image = np.array(Image.open("post_threshold_morphology_170.png"),dtype=np.uint8)
datapoints = np.where(image != 0)
x_coords = list(datapoints[0])
y_coords = list(datapoints[1])
# y_coords = list(255 - datapoints[1])
# generate all the datapoints coordinates
coords = np.array(list((zip(x_coords,y_coords))))
print(coords)
# compute clustering with Means
k_means = KMeans(init='k-means++', n_clusters=2, n_init=10)
k_means.fit(coords)

# plot result
fig = plt.figure(figsize=(8, 8))
fig.subplots_adjust(left=0.02, right=0.98, bottom=0.05, top=0.9)
colors = ['#4EACC5', '#FF9C34']

# same color applied to the same cluster from K-means
# pair the cluster centers with closet data points
k_means_cluster_centers = np.sort(k_means.cluster_centers_, axis=0)
k_means_labels = pairwise_distances_argmin(coords, k_means_cluster_centers)

ax = fig.add_subplot(1,1,1)
for k, col in zip(range(2), colors):
	my_members = k_means_labels == k
	cluster_center = k_means_cluster_centers[k]
	ax.plot(coords[my_members,1], 255 - coords[my_members,0], 'w', markerfacecolor=col, marker = '.')
	ax.plot(cluster_center[1], cluster_center[0], 'o', markerfacecolor=col,
            markeredgecolor='k', markersize=6)

ax.set_title('KMeans')
ax.set_xticks(())
ax.set_yticks(())

plt.show()


