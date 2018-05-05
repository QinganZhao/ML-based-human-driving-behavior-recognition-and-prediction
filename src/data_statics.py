import numpy as np
import matplotlib.pyplot as plt

"""
This function serves to concatenate the information of two cars into one array.

Note: car1 -- mainlane car; 
	  car2 -- merging car;
OutFormat:
0 case_ID
1 frame_ID

2 car1_long_pos
3 car1_long_vel
4 car1_lateral_pos
5 car1_lateral_displacement
6 car2_long_pos
7 car2_long_vel
8 car2_lateral_pos
9 car2_lateral_displacement

10 relative_long_vel (merge - mainlane)
11 relative_lateral_distance (merge - mainlane)
12 relative_long_distance (merge - mainlane)

13 car1_yaw
14 car2_yaw
15 situation label: (0: car1 yields car2; 1: car2 yields car1)
"""

traj_1 = np.loadtxt('./all_trajs_1.txt')
traj_2 = np.loadtxt('./all_trajs_2.txt')
data_matrix = np.loadtxt('./data_matrix.txt')

car1_long_velo_mean = np.mean(data_matrix[:, 3])
car1_long_velo_std = np.std(data_matrix[:, 3])

car1_lat_velo_mean = np.mean(data_matrix[:, 5])
car1_lat_velo_std = np.std(data_matrix[:, 5])

car2_long_velo_mean = np.mean(data_matrix[:, 7])
car2_long_velo_std = np.std(data_matrix[:, 7])

car2_lat_velo_mean = np.mean(data_matrix[:, 9])
car2_lat_velo_std = np.std(data_matrix[:, 9])
print ("car1_long_velo_mean: %g, car1_long_velo_std: %g" % (car1_long_velo_mean, car1_long_velo_std))
print ("car1_lat_velo_mean: %g, car1_lat_velo_std: %g" % (car1_lat_velo_mean, car1_lat_velo_std))
print ("car2_long_velo_mean: %g, car2_long_velo_std: %g" % (car2_long_velo_mean, car2_long_velo_std))
print ("car2_lat_velo_mean: %g, car2_lat_velo_std: %g" % (car2_lat_velo_mean, car2_lat_velo_std))

lower = -650
N = 150
interval = 130 / N
mean_ = np.zeros((N))
std_ = np.zeros((N))
mean_1 = np.zeros((N))
std_1 = np.zeros((N))

re_mean = np.zeros((N))
re_std = np.zeros((N))
for i in range(N):
	upper = lower + interval*(i+1)
	temp_data = data_matrix[np.where(data_matrix[:, 6] >= lower)]
	temp_data = temp_data[np.where(temp_data[:, 6] < upper)]
	mean_[i] = np.mean(temp_data[:, 7])
	std_[i] = np.std(temp_data[:, 7])

	temp_data_1 = data_matrix[np.where(data_matrix[:, 2] >= lower)]
	temp_data_1 = temp_data_1[np.where(temp_data_1[:, 2] < upper)]
	mean_1[i] = np.mean(temp_data_1[:, 3])
	std_1[i] = np.std(temp_data_1[:, 3])

	temp_data_2 = data_matrix[np.where(data_matrix[:, 2] >= lower)]
	temp_data_2 = temp_data_2[np.where(temp_data_2[:, 2] < upper)]
	re_mean[i] = np.mean(temp_data_2[:, 10])
	re_std[i] = np.std(temp_data_2[:, 10])

	lower = upper

plt.figure(1)
plt.plot(mean_)
plt.plot(mean_1)
#plt.plot(mean_ + std_)
#plt.plot(mean_ - std_)
t = range(N)
plt.fill_between(t, mean_ + std_, mean_ - std_, alpha=0.3,  facecolor='#FF9848') #edgecolor='#CC4F1B'
plt.fill_between(t, mean_1 + std_1, mean_1 - std_1, alpha=0.3,  facecolor='#089FFF') #edgecolor='#CC4F1B'
plt.ylim(5, 20)

plt.figure(2)
plt.plot(re_mean)
t = range(N)
plt.fill_between(t, re_mean + re_std, re_mean - re_std, alpha=0.3,  facecolor='#089FFF') #edgecolor='#CC4F1B'
plt.show()













