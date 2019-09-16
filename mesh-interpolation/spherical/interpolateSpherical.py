import csv
import os
import math
import numpy as np
from scipy import interpolate
from scipy.interpolate import Rbf
import matplotlib.pyplot as plt

filename = '1.csv'
output_name = '2.csv'
directory = r'C:\Projects\Dentist-Feng\mesh-interpolation'  # <-- if windows, the r is important
fullpath = os.path.join(directory, filename)
output_path = os.path.join(directory, output_name)

columns_count = 5
intersection = 7
scale_factor = 1

# 球面坐标系使用以下图的坐标表示
# https://zh.wikipedia.org/wiki/%E7%90%83%E5%BA%A7%E6%A8%99%E7%B3%BB#/media/File:3D_Spherical_2.svg

def Bicubic(lt, rt, lb, rb, hor_percent, ver_percent):
    t_bar = (rt - lt) * hor_percent + lt
    b_bar = (rb - lb) * hor_percent + lb
    bar = (b_bar - t_bar) * ver_percent + t_bar
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
    # print(xScaled2)
    return xScaled2

with open(fullpath, 'r', newline='') as csvfile:
    ofile = csv.reader(csvfile, delimiter=',')
    rows = (r for r in ofile if r)
    verts = [[float(i) for i in r] for r in rows]

    spherical_positions = []

    for vert in verts:
        x = vert[0]
        y = vert[1]
        z = vert[2]
        r = math.sqrt(x * x + y * y + z * z)
        theta = math.atan2(y, x) * scale_factor
        phi = math.atan2(math.sqrt(x * x + y * y), z) * scale_factor
        spherical_positions.append([r, theta, phi])
        # print(r, theta, phi)

    r = [i[0] for i in spherical_positions]
    theta = [i[1] for i in spherical_positions]
    phi = [i[2] for i in spherical_positions]
    

    thetaScaled = np.array(Scale(theta))
    phiScaled = np.array(Scale(phi))

    # tck = interpolate.bisplrep(theta, phi, r, s=0, kx=3, ky=3)
    rbfi = Rbf(theta, phi, r)

    vex = []
    new_verts = []
    for i, val in enumerate(thetaScaled):
        # vex.append(interpolate.bisplev(thetaScaled[i], phiScaled[i], tck))
        vex.append(rbfi(thetaScaled[i], phiScaled[i]))
        r = vex[i]
        z = r * math.cos(phiScaled[i] / scale_factor)
        r_xy = math.sqrt(r * r - z * z)
        y = r_xy * math.sin(thetaScaled[i] / scale_factor)
        x = r_xy * math.cos(thetaScaled[i] / scale_factor)
        
        # print(r, thetaScaled[i], phiScaled[i])
        new_verts.append([round(x, 4), round(y, 4), round(z, 4)])

    with open(output_path,"w+", newline='') as my_csv:
        csvWriter = csv.writer(my_csv,delimiter=',')
        csvWriter.writerows(new_verts)