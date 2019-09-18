from xml.dom import minidom
import csv

mydoc = minidom.parse('NA3777-02_AB.xml')

items = mydoc.getElementsByTagName('Vertex')

datapoints = []
for row in items:
    x = int(row.attributes['X'].value)
    y = int(row.attributes['Y'].value)
    datapoints.append([x,y])

with open("NA3777-02_AB.csv","w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(datapoints)
