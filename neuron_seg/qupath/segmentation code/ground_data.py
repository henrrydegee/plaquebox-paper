import csv
import math
import time
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

data_ls = []
with open('bbox_coords.csv') as csvfile:
    start_time = time.time()
    readCSV = csv.reader(csvfile, delimiter=",")
    next(readCSV) # skip the first line
    for row in readCSV:
        if row[0] != '':
            data_ls.append([int(float(row[0])),int(float(row[1]))])
    # sort the data list for efficient computation
    data_ls = sorted(data_ls, key = lambda x: x[0])
    data_ls = np.array(data_ls)
    second_time = time.time()
    print("time estimates to load the selected points csv file: %s seconds" % (second_time-start_time))

with open('cell_wo_residue.csv') as csvfile:
    start_time = time.time()
    coords = []
    readCSV = csv.reader(csvfile, delimiter=",")
    next(readCSV) # skip the first line
    for row in readCSV:
        if len(row) > 0:
            x = row[0].split()[3]
            y = row[0].split()[4]
            if x != 'NaN' and y != 'NaN':
                coord = [int(float(x)), int(float(y))]
                coords.append(coord)
    load_time = time.time()
    print("time estimates to load the entire slide csv file: %s seconds" % (load_time-start_time))

    x_list = [i[0] for i in coords]
    y_list = [i[1] for i in coords]
    datapoints = np.zeros((int(max(x_list))+1, int(max(y_list))+1), dtype='uint8')
    ini_data = time.time()
    print("time estimates to initialize data plane: %s seconds" % (ini_data-load_time))
    for x, y in coords:
        datapoints[int(x)][int(y)] = 1
    data_build = time.time()
    print("time estimates to finish building the data plane: %s seconds" % (data_build-ini_data))
    print(datapoints)

    feature_vec= []
    for x,y in data_ls:
        start_epoach = time.time()
        box_coords = datapoints[x:x+301, y:y+301]
        print("current coordinates: ", (x,y))
        points = np.array(list(zip(np.where(box_coords == 1)[0], np.where(box_coords == 1)[1])))
        box_dist = []
        points_count = 0
        #print(points)
        for box_x, box_y in points:
            dist = math.sqrt(math.pow(box_x-150,2) + math.pow(box_y-150,2))
            box_dist.append(dist)
            points_count += 1
        dist_sorted = sorted(box_dist)
        # compute average distance of closet 50  points
        feature_vec.append([x, y, sum(dist_sorted[0:20])/20, points_count]) # transform each coordinate to be a feature vector
        print("time estimates to compute current epoach of feature vectors: %s seconds" % (time.time() - start_epoach))
        print()

    with open("groundtruth_20_thresholded_halfway.csv","w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(feature_vec)
    #print("total time in running this window based operation to compute feature vector: %s seconds" % (time.time() - start_time))
