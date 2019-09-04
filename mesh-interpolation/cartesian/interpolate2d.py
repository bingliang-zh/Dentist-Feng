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

intersection = 3

def Bicubic(lt, rt, lb, rb, hor_percent, ver_percent):
    t_bar = (rt - lt) * hor_percent + lt
    b_bar = (rb - lb) * hor_percent + lb
    bar = (b_bar - t_bar) * ver_percent + t_bar
    # print(lt, rt, lb, rb)
    # print(t_bar, b_bar, bar)
    return bar

def NotHigher(v, m):
    if v > m:
        return m
    else :
        return v

def Scale(x):
    xScaled = x
    xScaled2 = []
    rows_count = len(x) // columns_count
    # for i, val in enumerate(x):
    #     if (i % columns_count == 0) :
    #         xScaled.append(val)
    #     else:
    #         last = x[i - 1]
    #         current = x[i]
    #         step = (current - last) / (intersection + 1)
    #         k = 0
    #         while k <= intersection:
    #             xScaled.append(last + (k+1) * step)
    #             k = k + 1

    gap = intersection + 1
    new_columns_count = (columns_count - 1) * gap + 1
    new_rows_count = (rows_count - 1) * gap + 1
    for r in range(new_rows_count):
        for c in range(new_columns_count):
            # print(r,c)
            hor_percent = c % gap / gap
            ver_percent = r % gap / gap
            lt_index = (r // gap) * columns_count + c // gap
            rt_index = NotHigher(lt_index + 1, columns_count * rows_count - 1)
            lb_index = NotHigher(lt_index + columns_count, columns_count * rows_count - 1)
            rb_index = NotHigher(lt_index + columns_count + 1, columns_count * rows_count - 1)
            # print(lt_index, rt_index, lb_index, rb_index, hor_percent, ver_percent)
            xScaled2.append(Bicubic(xScaled[lt_index], xScaled[rt_index], xScaled[lb_index], xScaled[rb_index], hor_percent, ver_percent))

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

    tck = interpolate.bisplrep(x, y, z, s=0, kx=2, ky=2)

    vex = []
    new_verts = []
    for i, val in enumerate(xScaled):
        vex.append(interpolate.bisplev(xScaled[i], yScaled[i], tck))
        new_verts.append([xScaled[i], yScaled[i], vex[i]])

    with open(output_path,"w+", newline='') as my_csv:
        csvWriter = csv.writer(my_csv,delimiter=',')
        csvWriter.writerows(new_verts)