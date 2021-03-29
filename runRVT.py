import RevisitTime
from itertools import product
import numpy as np
import multiprocessing
import csv

#Initial Values
period = [60]
rE = 6378.137 #Earth Radius

alt_init = list(range(500, 801, 50)) #Initial Altitude
inc_init = [-1, 52, 80] #Initial Inclination, -1 represents SSO(Sun Sychronized Oribit
num_sat = [1, 4, 16, 32] #Number of Satellites
num_plane = [4] #Number of Planes
look_ang = [10, 20, 30] #Sensor Angle
constellation = [360] #Raan Spreading

#Create Input Arrays
items = [alt_init, inc_init, num_sat, num_plane, look_ang, constellation, period]
dff = list(product(*items)) #Full Factorial Design
result = np.zeros((len(dff), 7))
f = np.zeros((len(dff), 7))
RVTime = RevisitTime.RevisitTime()

#Run Engine
def RunEngine(i):
   result[i,:] = RVTime.create_and_run_engine(dff[i][0]+rE, dff[i][1], dff[i][2], dff[i][3], dff[i][4], dff[i][5], dff[i][6])
   print(i+1,'/',len(dff))
   print(dff[i])
   f = result[i,:]
   return f


if __name__ == '__main__':
    #print(RVTime.create_and_run_engine(800+rE, 42, 16, 4, 20, 360, 3))
    #print(RVTime.create_and_run_engine(800 + rE, 42, 16, 4, 80, 360, 3))
    pool = multiprocessing.Pool(processes=5)
    wow = pool.map(RunEngine, range(0, len(dff), 1))
    #wow = pool.map(RunEngine, range(0, 2, 1))
    #print(wow)

    with open('Output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        header_list = ['Altitude', 'Inclination', 'NumberSats', 'SenAng', 'avgVar', 'minVar', 'maxVar']
        writer.writerow(header_list)
        writer.writerows(wow)