import numpy.random.common
import numpy.random.bounded_integers
import numpy.random.entropy

from numpy import array, concatenate, newaxis
from numpy.linalg import svd
from pandas import read_excel, ExcelWriter, ExcelFile

df = read_excel('data.xlsx')

x = array(df['X'])
y = array(df['Y'])
z = array(df['Z'])

data = concatenate((x[:, newaxis], 
                       y[:, newaxis], 
                       z[:, newaxis]), 
                      axis=1)

datamean = data.mean(axis=0)

uu, dd, vv = svd(data - datamean)

print('start | centroid')
print(datamean)
print('end')
print(datamean + vv[0] * 5)
print('direction')
print(vv[0])
