import csv
import math
import time
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

# load data into the program, store all the coordinates
with open('cell_wo_residue.csv') as csvfile:
    start_time = time.time()
    readCSV = csv.reader(csvfile, delimiter=",")
    coords = []
    next(readCSV) # skip the first line
    for row in readCSV:
        if len(row) > 0:
            x = row[0].split()[3]
            y = row[0].split()[4]
            if x != 'NaN' and y != 'NaN':
                coord = [float(x), float(y)]
                coords.append(coord)
    second_time = time.time()
    print("time estimates to load the csv file: %s seconds" % (second_time-start_time))
    feature_vec= []
    for coord in coords:
        start_time = time.time()
        x = coord[0]
        y = coord[1]
        left_range = x - 100
        right_range = x  + 100
        top_range = y + 100
        bottom_range = y - 100
        box_dist = []
        for x_box, y_box in coords:
            if (x < right_range and x >= left_range) and (y_box < top_range >= bottom_range):
                dist = math.sqrt(math.pow(x_box-x,2) + math.pow(y_box-y,2))
                box_dist.append(dist)
        inner_time = time.time()
        print("In each epoach, time estimates on coordnate candidates: %s seconds" % (inner_time-start_time))
        dist_sorted = sorted(box_dist)

        # print("first 10 distances: ", dist_sorted[0:11])
        # get the first 11 numbers, however, coord itself will be returned also. Therefore, average distance only divides by 10
        feature_vec.append([x, y, sum(dist_sorted[0:11])/10]) # transform each coordinate to be a feature vector
        print("time estimates to compute current epoach of feature vectors: %s seconds" % (time.time() - start_time))
        print("current feature vector: ", [x, y, sum(dist_sorted[0:11])/10])
        print()
    print("time estimates for entire feature vector computation: %s seconds" %s (time.time() - second_time))
    with open("feature_vec.csv","w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(feature_vec)
