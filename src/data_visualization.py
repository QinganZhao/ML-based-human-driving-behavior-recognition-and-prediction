import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib as mpl 
import matplotlib.patches as patches

def loaddata(file_name, car_flag):
	if car_flag == 1:
		data = np.loadtxt('./car1/'+str(file_name))
	elif car_flag == 2:
		data = np.loadtxt('./car2/'+str(file_name))

	return data

def plot_phase(car1,car2, ax1):
	#ax1 = fig.asubplot(111, aspect='equal')
	ax1.add_patch(
	    patches.Rectangle(
	        (-650, -650),   # (x,y)
	        212,          # width
	        212,          # height
	         alpha=0.1
	    )
	)
	ax1.scatter(car1[:, 1], car2[:,1], c = range(T), s=1, cmap = 'viridis')
	ax1.plot(car1[:, 1], car1[:,1])
	ax1.axis('equal')
	#ax1.set_title('longitudinal velocity phase portrait')
	ax1.set_xticks([])  
	ax1.set_yticks([])

def plot_relative_long_vel(car1,car2, ax):
	# longitudinal velocity
	# plt.figure(figsize=(20,2))
	vel1 = 100*(car1[1:,1] - car1[0:-1, 1])
	vel2 = 100*(car2[1:,1] - car2[0:-1, 1])
	ax.plot(range(T-1), vel1-vel2)
	ax.set_ylim(-6, 6)
	#plt.set_title('relative longitudinal velocities')
	ax.set_xticks([])  
	ax.set_yticks([])

def plot_long_vel(car1,car2,ax):
	# longitudinal velocity
	vel1 = 100*(car1[1:,1] - car1[0:-1, 1])
	vel2 = 100*(car2[1:,1] - car2[0:-1, 1])
	ax.plot(range(T-1), vel1, c='b',label='vel1')
	ax.plot(range(T-1), vel2, c='g',label='vel2')
	ax.set_ylim(7,18)
	#ax.set_title('longitudinal velocities')
	#ax.set_xticks([])  
	#ax.set_yticks([])

def plot_long_acc(car1,car2,ax):
	vel1 = 100*(car1[1:,1] - car1[0:-1, 1])
	vel2 = 100*(car2[1:,1] - car2[0:-1, 1])
	acc1 = 100*(vel1[1:] - vel1[0:-1])
	acc2 = 100*(vel2[1:] - vel2[0:-1])
	ax.plot(range(T-2), acc1, c='b',label='acc1')
	ax.plot(range(T-2), acc2, c='g',label='acc2')


def plot_lateral_pos(car1,car2,ax):
	# lateral position
	ax.plot(range(T), car1[:,2],c='b')
	ax.plot(range(T), car2[:,2],c='g')
	#ax.set_title('lateral positions')
	ax.set_xticks([])  
	ax.set_yticks([])

def plot_lateral_vel(car1,car2,ax):
	vel1 = 100*(car1[1:,2] - car1[0:-1, 2])
	vel2 = 100*(car2[1:,2] - car2[0:-1, 2])
	ax.plot(range(T-1), vel1, c='b',label='lateral_vel1')
	ax.plot(range(T-1), vel2, c='g',label='lateral_vel2')
	#ax.set_title('lateral velocities')
	ax.set_xticks([])  
	ax.set_yticks([])

def plot_yaw(car1,car2,ax):
	# yaw angle
	ax.plot(range(T), car1[:,3],c='b')
	ax.plot(range(T), car2[:,3],c='g')
	#ax.set_title('yaw angle')
	ax.set_xticks([])  
	ax.set_yticks([])

def plot_traj(car1,car2, ax):
	# Trajectory
	#plt.figure()
	#cm = mpl.cm.get_cmap('Greens') 
	ax.scatter(car1[:,1],car1[:,2],c= range(T), s = 1,label='car1', cmap='viridis')
	ax.scatter(car2[:,1],car2[:,2],c= range(T), s = 1, label='car2', cmap='viridis')
	ax.axis('equal')
	#ax.set_title('Trajectorys')
	ax.set_xticks([])  
	ax.set_yticks([])

def stats():
	label = np.zeros((128, 1))
	
	for i in range(128):
		
		file_name_1 = 'data_'+str(i)+'_1.txt'
		file_name_2 = 'data_'+str(i)+'_2.txt'

		car1 = loaddata(file_name_1, 1)
		car2 = loaddata(file_name_2, 2)
		print (car1.shape)
		final_x_1 = car1[-1, 1]
		final_x_2 = car2[-1, 1]
		
		if (final_x_2 > final_x_1):
			label[i, 0] = 1;

	print ("the percent of main lane car yield:" + str(sum(label)/label.shape[0]))

	return label




# data = np.loadtxt('./7data.txt')
N = 5
fig1, axs1 = plt.subplots(N,N, figsize=(15, 3))
fig2, axs2 = plt.subplots(N,N, figsize=(15, 3))
fig3, axs3 = plt.subplots(N,N, figsize=(15, 3))
fig4, axs4 = plt.subplots(N,N, figsize=(15, 3))
fig5, axs5 = plt.subplots(N,N, figsize=(15, 3))
fig6, axs6 = plt.subplots(N,N, figsize=(15, 3))
axs1 = axs1.ravel()
axs2 = axs2.ravel()
axs3 = axs3.ravel()
axs4 = axs4.ravel()
axs5 = axs5.ravel()
axs6 = axs6.ravel()
#stats()

for i in range(N*N):
	file_name_1 = 'data_'+str(i)+'_1.txt'
	file_name_2 = 'data_'+str(i)+'_2.txt'

	car1 = loaddata(file_name_1, 1)
	car2 = loaddata(file_name_2, 2)
	# print(car1.shape)

	T = int(car1.shape[0])

	final_x_1 = car1[-1, 1]
	final_x_2 = car2[-1, 1]
		
	#if (final_x_2 < final_x_1): # only plot 'mainlane yield merge'
		#label[i, 0] = 0;
	plot_relative_long_vel(car1,car2,axs1[i])
	#plot_long_vel(car1, car2, axs2[i-76])
		# plot_traj(car1, car2, axs3[i])
		# plot_lateral_pos(car1,car2,axs4[i])
		# plot_long_acc(car1,car2,axs5[i])
	plot_phase(car1,car2,axs6[i])

	#plot_phase(car1,car2, axs1[i])


plt.show()


