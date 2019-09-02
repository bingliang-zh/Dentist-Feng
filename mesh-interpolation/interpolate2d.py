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

intersection = 2

def Scale(x):
    xScaled = []
    xScaled2 = []
    rows_count = len(x) // columns_count
    for i, val in enumerate(x):
        if (i % columns_count == 0) :
            xScaled.append(val)
        else:
            last = x[i - 1]
            current = x[i]
            step = (current - last) / (intersection + 1)
            k = 0
            while k <= intersection:
                xScaled.append(last + (k+1) * step)
                k = k + 1
    new_columns_count = (columns_count - 1) * (intersection + 1) + 1
    for i in range(rows_count):
        for j in range(new_columns_count):
            if j == 0:
                if i == 0:
                    xScaled2.append(xScaled[i * new_columns_count + j])
                else :
                    for m in range(intersection + 1):
                        for k in range(new_columns_count):
                            last = xScaled[(i - 1) * new_columns_count + k]
                            current = xScaled[i * new_columns_count + k]
                            step = (current - last) / (intersection + 1)
                            xScaled2.append(last + (m + 1) * step)
            else :
                xScaled2.append(xScaled[i * new_columns_count + j])
                
    print(new_columns_count)
    return xScaled2

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

    with open(output_path,"w+", newline='') as my_csv:
        csvWriter = csv.writer(my_csv,delimiter=',')
        csvWriter.writerows(new_verts)