import numpy as np
import pandas as pd
import ROUSSEAU_SPEC_Commands as SPEC
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


#######################################################
# Define function that organizes laser scan output data
#######################################################
def read_values_from_txt(filename):
    values_list = []
    with open(filename, 'r') as file:
        sublist = []
        for line in file:
            line = line.strip()
            if line:
                try:
                    value = float(line)
                    sublist.append(value)
                except ValueError:
                    print(f"Invalid value in line: {line}. Skipping.")
            if len(sublist) == 3200:
                values_list.append(sublist)
                sublist = []

        # Append the remaining sublist if it contains any values (less than 3200)
        if sublist:
            values_list.append(sublist)

    return values_list

if __name__ == "__main__":


    side_0_scans = read_values_from_txt("KeyenceScan_0.txt")
    side_90_scans = read_values_from_txt("KeyenceScan_90.txt")
    side_180_scans = read_values_from_txt("KeyenceScan_180.txt")
    side_270_scans = read_values_from_txt("KeyenceScan.txt")
    

#################################################
# Define function that reduces laser output data
#################################################
def reduce_data(array_name):
    array_indices = []
    for i in range(len(array_name)):
        for j in range(len(array_name[i])):
            while True:
                if array_name[i][j] != -99.99:
                    array_indices.append(i)
                    break
                break
    array_indices = list(np.unique(array_indices))
    array_red = array_name[np.min(array_indices):np.max(array_indices)]
    return [array_indices,array_red]
if __name__ == "__main__":
    
    [side_0_index,side_0_red] = reduce_data(side_0_scans)
    [side_90_index,side_90_red] = reduce_data(side_90_scans)
    [side_180_index,side_180_red] = reduce_data(side_180_scans)
    [side_270_index,side_270_red] = reduce_data(side_270_scans)
    

#############################################
# Import SPEC_Command text file as data frame
#############################################
spec_file = pd.read_csv('SPEC.txt', sep=" ", header=None)
spec_file.columns = ['data pt', 'X', 'Y', 'Z', 'PHI', 'scan flag', 'rotation flag']


def generate_data_pts(spec_command_file, phi, array_indices):
    # Initialize lists to store X, Y, and Z values
    x_values = []
    y_values = []
    z_values = []

    # Loop through the DataFrame to filter rows with scan flag = 1 and extract values
    for index, row in spec_command_file.iterrows():
        if row['scan flag'] == 1:
            if row['PHI'] == phi:
                x_values.append(row['X'])
                y_values.append(row['Y'])
                z_values.append(row['Z'])
    x_values = x_values[np.min(array_indices):np.max(array_indices)]
    y_values = y_values[np.min(array_indices):np.max(array_indices)]
    z_values = z_values[np.min(array_indices):np.max(array_indices)]
    return [x_values, y_values, z_values]
if __name__ == "__main__":
    
    [x_values_0, y_values_0, z_values_0] = generate_data_pts(spec_file, 0, side_0_index)
    [x_values_90, y_values_90, z_values_90] = generate_data_pts(spec_file, 90, side_90_index)
    [x_values_180, y_values_180, z_values_180] = generate_data_pts(spec_file, 180, side_180_index)
    [x_values_270, y_values_270, z_values_270] = generate_data_pts(spec_file, 270, side_270_index)


#############################
# Generate points in 3D space
#############################
side_0_x = []
side_0_y = []
side_0_z = []
for i in range(len(side_0_red)):
    for j in range(3200):
        if side_0_red[i][j] != -99.99:
            if SPEC.motor_parallel_0 == 1:
                side_0_x.append((SPEC.center_dist - (x_values_0[i] - 75)) - (76.25 - side_0_red[i][j]))
            else:
                side_0_x.append((SPEC.center_dist + (x_values_0[i] - 75)) - (76.25 - side_0_red[i][j]))
            
            if SPEC.motor_parallel_90 == 1:
                side_0_y.append(SPEC.laser_dist - (y_values_0[i] - 75))
            else:
                side_0_y.append(-SPEC.laser_dist - (y_values_0[i] - 75))
                
            side_0_z.append(0 + j*0.0125)


side_90_x = []
side_90_y = []
side_90_z = []
for i in range(len(side_90_red)):
    for j in range(3200):
        if side_90_red[i][j] != -99.99:
            if SPEC.motor_parallel_90 == 1:
                side_90_y.append((SPEC.center_dist - (y_values_90[i] - 75)) - (76.25 - side_90_red[i][j]))
            else:
                side_90_y.append((SPEC.center_dist + (y_values_90[i] - 75)) - (76.25 - side_90_red[i][j]))
            
            if SPEC.motor_parallel_0 == 1:
                side_90_x.append(-SPEC.laser_dist - (x_values_90[i] - 75))
            else:
                side_90_x.append(SPEC.laser_dist - (x_values_90[i] - 75))
                
            side_90_z.append(0 + j*0.0125)
            
            
side_180_x = []
side_180_y = []
side_180_z = []
for i in range(len(side_180_red)):
    for j in range(3200):
        if side_180_red[i][j] != -99.99:
            if SPEC.motor_parallel_0 == 0:
                side_180_x.append(-((SPEC.center_dist - (x_values_180[i] - 75)) - (76.25 - side_180_red[i][j])))
            else:
                side_180_x.append(-((SPEC.center_dist + (x_values_180[i] - 75)) - (76.25 - side_180_red[i][j])))
            
            if SPEC.motor_parallel_90 == 0:
                side_180_y.append(SPEC.laser_dist - (y_values_180[i] - 75))
            else:
                side_180_y.append(-SPEC.laser_dist - (y_values_180[i] - 75))
                
            side_180_z.append(0 + j*0.0125)


side_270_x = []
side_270_y = []
side_270_z = []
for i in range(len(side_270_red)):
    for j in range(3200):
        if side_270_red[i][j] != -99.99:
            if SPEC.motor_parallel_90 == 0:
                side_270_y.append(-((SPEC.center_dist - (y_values_270[i] - 75)) - (76.25 - side_270_red[i][j])))
            else:
                side_270_y.append(-((SPEC.center_dist + (y_values_270[i] - 75)) - (76.25 - side_270_red[i][j])))
            
            if SPEC.motor_parallel_0 == 0:
                side_270_x.append(-SPEC.laser_dist - (x_values_270[i] - 75))
            else:
                side_270_x.append(SPEC.laser_dist - (x_values_270[i] - 75))
                
            side_270_z.append(0 + j*0.0125)


x_coord = side_0_x + side_90_x + side_180_x + side_270_x
y_coord = side_0_y  + side_90_y + side_180_y + side_270_y
z_coord = side_0_z + side_90_z + side_180_z + side_270_z

# creating figure
fig = plt.figure()
ax = Axes3D(fig)

# creating the plot
plot_geeks = ax.scatter(side_0_x, side_0_y, side_0_z, color='blue')

 
# setting title and labels
ax.set_title("3D plot")
ax.set_xlabel('x-axis')
ax.set_ylabel('y-axis')
ax.set_zlabel('z-axis')
 
# displaying the plot
plt.show()

# Write to text file
f = open('Model_3D.txt','w')
for i in range(len(x_coord)):
    f.write("{:.6f}".format(x_coord[i]) + '\t' + "{:.6f}".format(y_coord[i]) + '\t' + "{:.6f}".format(z_coord[i]) + '\n')