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
    load_time = time.time()
    print("time estimates to load the csv file: %s seconds" % (load_time-start_time))
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
    for x in range(150, len(datapoints)-150, 5):
        row_epoach = time.time()
        for y in range(150, len(datapoints[0])-150, 5):
            start_epoach = time.time()
            # Create a box shape 501*801, center is (250, 400)
            box_coords = datapoints[int(x)-150:int(x)+151, int(y)-150:int(y)+151]
            print("current coordinates: ", (x,y))
            #print("box matrix: ", box_coords)
            #print("width, height", (box_coords.shape[0],box_coords.shape[1]))
            #print(np.where(box_coords == 1))
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
            feature_vec.append([x, y, sum(dist_sorted[0:21])/20, points_count]) # transform each coordinate to be a feature vector
            print("time estimates to compute current epoach of feature vectors: %s seconds" % (time.time() - start_epoach))
            print()
        print("time estimates to compute current row of feature vectors: %s seconds" % (time.time() - row_epoach))
        print()

    with open("feature_vec_whole_20.csv","w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(feature_vec)
    print("total time in running this window based operation to compute feature vector: %s seconds" % (time.time() - start_time))
