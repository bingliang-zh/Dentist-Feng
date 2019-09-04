import csv
import os
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt

filename = '1.csv'
output_name = '2.csv'
directory = r'C:\Projects\Dentist-Feng\mesh-interpolation'  # <-- if windows, the r is important
fullpath = os.path.join(directory, filename)
output_path = os.path.join(directory, output_name)

columns_count = 5

scale = 3

def Scale(x):
    xScaled = []
    for i, val in enumerate(x):
        if (i % 5 == 0) :
            xScaled.append(val)
        else:
            last = x[i - 1]
            current = x[i]
            step = (current - last) / scale
            k = 0
            while k < scale:
                xScaled.append(last + (k+1) * step)
                k = k + 1
    return xScaled

with open(fullpath, 'r', newline='') as csvfile:
    ofile = csv.reader(csvfile, delimiter=',')
    rows = (r for r in ofile if r)
    verts = [[float(i) for i in r] for r in rows]
    x = [i[0] for i in verts]
    y = [i[1] for i in verts]
    z = [i[2] for i in verts]

    xScaled = np.array(Scale(x))
    yScaled = np.array(Scale(y))

    tck = interpolate.bisplrep(x, y, z, s=0)

    vex = []
    new_verts = []
    for i, val in enumerate(xScaled):
        vex.append(interpolate.bisplev(xScaled[i], yScaled[i], tck))
        new_verts.append([xScaled[i], yScaled[i], vex[i]])

    # with open(output_path, 'w', newline='') as myfile:
    #  wr = csv.writer(myfile)
    #  wr.writerow(new_verts)
    with open(output_path,"w+", newline='') as my_csv:
        csvWriter = csv.writer(my_csv,delimiter=',')
        csvWriter.writerows(new_verts)