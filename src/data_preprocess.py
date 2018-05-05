import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib as mpl 
import matplotlib.patches as patches

def load_data(file_name, car_flag):
	if car_flag == 1:
		data = np.loadtxt('./car1/'+str(file_name))
	elif car_flag == 2:
		data = np.loadtxt('./car2/'+str(file_name))

	return data

def get_low_freq_data(data):
	"""
	Return a data matrix with 0.1s per time step data. (from 0.01s data)
	"""
	matrix = np.zeros((1, data.shape[1]))
	for i in range(data.shape[0]):
		if i % 10 == 0:
			matrix = np.concatenate((matrix, data[i,:].reshape(1,data.shape[1])),axis=0)

	return matrix[1:,:]


def data_process():
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
	data_matrix = np.zeros((1,16))
	for i in range(128):
		file_name_1 = 'data_'+str(i)+'_1.txt'
		file_name_2 = 'data_'+str(i)+'_2.txt'
		car1 = get_low_freq_data(load_data(file_name_1, 1))
		car2 = get_low_freq_data(load_data(file_name_2, 2))

		T = int(car1.shape[0])
		#print(T)
		current_data_matrix = np.zeros((T,16))
		for j in range(1, T):
			current_data_matrix[j,0] = i
			current_data_matrix[j,1] = j
			current_data_matrix[j,2] = car1[j,1]
			current_data_matrix[j,3] = 10 * (car1[j,1] - car1[j-1,1])
			current_data_matrix[j,4] = car1[j,2]
			current_data_matrix[j,5] = car1[j,2] - car1[j-1,2]

			current_data_matrix[j,6] = car2[j,1]
			current_data_matrix[j,7] = 10 * (car2[j,1] - car2[j-1,1])
			current_data_matrix[j,8] = car2[j,2]
			current_data_matrix[j,9] = car2[j,2] - car2[j-1,2]

			current_data_matrix[j,10] = current_data_matrix[j,7] - current_data_matrix[j,3]
			current_data_matrix[j,11] = current_data_matrix[j,8] - current_data_matrix[j,4]
			current_data_matrix[j,12] = current_data_matrix[j,6] - current_data_matrix[j,2]

			current_data_matrix[j,13] = car1[j,3]
			current_data_matrix[j,14] = car2[j,3]


			if car1[-1,1] > car2[-1,1]:
				current_data_matrix[j,15] = 1
			else:
				current_data_matrix[j,15] = 0
		current_data_matrix = current_data_matrix[1:, :]
		data_matrix = np.concatenate((data_matrix, current_data_matrix),axis=0)

	np.savetxt('./data_matrix.txt', data_matrix[1:,:],'%.4f')




##################################################################



def divide_data(data_matrix, segment_length):
	"""
	This function serves to separate two situation cases.
	"""

	situation0_data = data_matrix[np.where(data_matrix[:,-1] == 0)]
	situation1_data = data_matrix[np.where(data_matrix[:,-1] == 1)]

	np.savetxt('./all_trajs_1.txt', situation0_data, '%.4f')
	np.savetxt('./all_trajs_2.txt', situation1_data, '%.4f')

	
	# count seq lengths
	# separate sequence segments
	# all_trajs_seg_1 = np.zeros((1, data_matrix.shape[1]))
	# all_trajs_seg_2 = np.zeros((1, data_matrix.shape[1]))
	all_trajs_1 = np.zeros((1, data_matrix.shape[1]))
	all_trajs_2 = np.zeros((1, data_matrix.shape[1]))
	count0, count1 = [], []

	# for i in range(128):
	# 	print('i = '+str(i))
	# 	temp_data = data_matrix[np.where(data_matrix[:,0] == i)]
	# 	if temp_data[0,-1] == 0:
	# 		for j in range(temp_data.shape[0]-segment_length+1):
	# 			temp_seg_data = temp_data[j:j+segment_length, :]
	# 			count0.append(temp_seg_data.shape[0])
	# 			all_trajs_seg_1 = np.concatenate((all_trajs_seg_1, temp_seg_data),axis=0)
	# 	else:
	# 		for j in range(temp_data.shape[0]-segment_length+1):
	# 			temp_seg_data = temp_data[j:j+segment_length, :]
	# 			count1.append(temp_seg_data.shape[0])
	# 			all_trajs_seg_2 = np.concatenate((all_trajs_seg_2, temp_seg_data),axis=0)

	for i in range(128):
		print('i = '+str(i))
		temp_data = data_matrix[np.where(data_matrix[:,0] == i)]
		if temp_data[0,-1] == 0:
			count0.append(temp_data.shape[0])
			all_trajs_1 = np.concatenate((all_trajs_1, temp_data),axis=0)
		elif temp_data[0,-1] == 1:
			count1.append(temp_data.shape[0])
			all_trajs_2 = np.concatenate((all_trajs_2, temp_data),axis=0)


	print(all_trajs_1.shape)
	print(all_trajs_2.shape)
	print(sum(count0))
	print(sum(count1))

	# np.savetxt('./all_trajs_seg_1.txt', all_trajs_seg_1[1:,:], '%.4f')
	# np.savetxt('./all_trajs_seg_2.txt', all_trajs_seg_2[1:,:], '%.4f')

	np.savetxt('./all_trajs_seq_length_1.txt', np.array(count0), '%d')
	np.savetxt('./all_trajs_seq_length_2.txt', np.array(count1), '%d')

#data_process()
#data_matrix = np.loadtxt('./data_matrix.txt')
#divide_data(data_matrix=data_matrix, segment_length=30)


###############################################

def check_data():

	data = np.loadtxt('../simulation_data/data_matrix.txt')
	temp_data = data[np.where(data[:,0]==69)]
	T = temp_data.shape[0]
	car1_long_vel = temp_data[:,3]
	car2_long_vel = temp_data[:,7]
	car1_acc = 10*(temp_data[1:,3]-temp_data[:-1,3])
	car2_acc = 10*(temp_data[1:,7]-temp_data[:-1,7])
	
	# plt.figure(1)
	# plt.plot(range(T-1), car1_acc, c='b', label='main lane car acceleration')
	# plt.plot(range(T-1), car2_acc, c='r', label='merging car acceleration')
	# plt.legend()

	plt.figure(2,figsize=(14,4))
	plt.plot(range(T), car1_long_vel, c='b', label='main lane car velocity')
	plt.plot(range(T), car2_long_vel, c='r', label='merging car velocity')
	plt.legend()

	plt.savefig('./long_vel_69.eps', bbox_inches='tight')

	#plt.show()


#check_data()

###############################################

def plot_vehicles(case_id, data_matrix):
	"""
	This function is to plot vehicle trajectories with bounding boxes.
	"""

	current_case_data = data_matrix[np.where(data_matrix[:,0]==case_id)]
	T = current_case_data.shape[0]

	fig = plt.figure(figsize=(20,2))
	for i in range(T):
		
		if i<10:
			name='00'+str(i)
		elif i>=10 and i<100:
			name = '0'+str(i)
		elif i>=100:
			name = str(i)

		ax = fig.add_subplot(111, aspect='equal')
		ax.add_patch(
    		patches.Rectangle(
        		(current_case_data[i,2]-2.0, current_case_data[i,4]-0.9),   # (x,y)
        		4.0,          # width
        		1.8,          # height
        		alpha = 0.3 + 0.7*(T-i) / float(T),
        		facecolor='blue',
        		edgecolor='black',
        		linewidth=0.5
   		 	)
		)
		ax.add_patch(
    		patches.Rectangle(
        		(current_case_data[i,6]-2.0, current_case_data[i,8]-0.9),   # (x,y)
        		4.0,          # width
        		1.8,          # height
        		alpha = 0.3 + 0.7*(T-i) / float(T),
        		facecolor='red',
        		edgecolor='black',
        		linewidth=0.5
   		 	)
		)
		ax.plot(range(-805,-360),-605*np.ones(445), color='k',linewidth=1)
		ax.plot(range(-805,-584),-610*np.ones(221), color='k',linewidth=1)
		ax.plot(range(-445,-360),-610*np.ones(85), color='k',linewidth=1)
		x = [[-584,-805],[-445,-805]]
		y = [[-610,-618],[-610,-622]]
		for l in range(len(x)):
			ax.plot(x[l], y[l], color='k',linewidth=1)

		ax.set_xlim(-680, -400)
		ax.set_ylim(-620, -600)
		ax.set_xticks([])  
		ax.set_yticks([])
		fig.savefig('./vehicles_plot/'+str(case_id)+'_'+str(name)+'.png', bbox_inches='tight')


data_matrix = np.loadtxt('./data_matrix.txt')
plot_vehicles(case_id=8, data_matrix=data_matrix)


		








