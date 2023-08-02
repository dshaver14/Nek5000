import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import glob
import os

l2_norm_rans =[1] * 8

for i in range(1,9):

    l2_norm=[]
    l1_norm=[]
    l2_norm_r=[]
    l1_norm_r=[]
    l2_norm_bet=[]
    l1_norm_bet=[]
    
    # Experimental Results
    experimental_file = 'exp/y'+str(i)+'.csv'
    experimental_data = np.loadtxt(experimental_file, delimiter=',')
    experimental_x = experimental_data[:, 0]  # Assuming x values are in the first column
    experimental_v = experimental_data[:, 1]  /np.max(experimental_data[:, 1])# Assuming velocity values are in the second column

    # LES Results
    simulation_file = 'les/Re_12819_'+str(i)+'.csv'
    simulation_data = np.loadtxt(simulation_file,skiprows=1, delimiter=',')
    simulation_x = simulation_data[:, 0]  # Assuming x values are in the first column
    simulation_v = simulation_data[:, 2]  # Assuming velocity values are in the second column
    simulation_v_n= simulation_data[:, 2] /np.max(simulation_v)
    #TKE
    simulation_tke_n = simulation_data[:,3] / np.max(simulation_data[:,3])
    # Linear Interpolation
    interp_func = interp1d(simulation_x, simulation_v_n)
    interpolated_v = interp_func(experimental_x)
    
    relative_difference_l = np.abs(interpolated_v - experimental_v) / experimental_v * 100
    
    absolute_difference = np.abs(interpolated_v - experimental_v)
    
    # L1 and L2 norms LES to Exp
    l2_norm =  np.linalg.norm(absolute_difference)/np.linalg.norm(experimental_v) *100
    l1_norm =  np.linalg.norm(absolute_difference,ord=1)/np.linalg.norm(experimental_v,ord=1) *100
    
    # Results of RANS
    rans_file = 'dome.0000'+str(i)+'.dat'
    rans_data = np.loadtxt(rans_file,skiprows=1)
    simulation_x_r = rans_data[:, 1]  # Assuming x values are in the first column
    simulation_v_r = -rans_data[:, 2]  # Assuming velocity values are in the second column
    simulation_v_n_r= simulation_v_r /np.max(np.abs(simulation_v_r))
    #TKE
    simulation_tke_r_n = rans_data[:,6] / np.max(rans_data[:,6])
    interp_func = interp1d(simulation_x_r, simulation_tke_r_n)
    interpolated_tke_r = interp_func(simulation_x)
   
    #Linear Interpolation
    interp_func = interp1d(simulation_x_r, simulation_v_n_r)
    interpolated_v_r = interp_func(experimental_x)
    
    relative_difference_r = np.abs(interpolated_v_r - experimental_v) / experimental_v * 100
    
    absolute_difference_r = np.abs(interpolated_v_r - experimental_v)
    
    # L1 and L2 Norms RANS to Exp
    l2_norm_r =  np.linalg.norm(absolute_difference_r)/np.linalg.norm(experimental_v) *100
    l1_norm_r =  np.linalg.norm(absolute_difference_r,ord=1)/np.linalg.norm(experimental_v,ord=1) *100
    # L1 and L2 Norms RANS to LES
    absolute_difference_bet = np.abs(interpolated_v_r - interpolated_v)
    l2_norm_bet =  np.linalg.norm(absolute_difference_bet)/np.linalg.norm(experimental_v) *100
    l1_norm_bet =  np.linalg.norm(absolute_difference_bet,ord=1)/np.linalg.norm(experimental_v,ord=1) *100
    #TKE
    simulation_tke_r_n = rans_data[:,6] / np.max(rans_data[:,6])
    interp_func = interp1d(simulation_x_r, simulation_tke_r_n)
    interpolated_tke_r = interp_func(simulation_x)


#    Comparison of velocities as graph on each axial location    
    plt.clf()
    plt.plot(simulation_x, interpolated_tke_r,'b' ,label='RANS-TKE')
    plt.plot(simulation_x, simulation_tke_n, 'r', label='LES-TKE')
    plt.legend()
    plt.xlabel('Radial Location')
    plt.grid(True,linestyle='--')
    plt.ylabel('Normalized TKE')
    plt.title('Axial Location =' +str(i))

    plt.savefig('TKE_loc'+str(i)+'.png')
#    Comparison of velocities as graph on each axial location    
    plt.clf()
    plt.plot(experimental_x, interpolated_v,'b' ,label='LES-Vel_z')
    plt.plot(experimental_x, interpolated_v_r, 'r', label='RANS-Vel_z')
    plt.plot(experimental_x, experimental_v, 'g*', label='Exp-Vel_z')
    plt.legend()
    plt.xlabel('Radial Location')
    plt.ylabel('Normalized Velocity')
    plt.grid(True,linestyle='--')
    plt.title('Axial Location =' +str(i))
    plt.savefig('Vel_loc'+str(i)+'.png')

    l2_norm_rans[i-1]=l2_norm_r
    print("Location => ",i,"Relative difference (%):")
    
    print("L1 Norm of LES to EXP => ",l1_norm)
    
    print("L1 Norm of RANS to EXP => ",l1_norm_r)
    
    print("L1 Norm of RANS to LES => ",l1_norm_bet)
    
    print(f"\033[33m L2 Norm \033[0mof LES to EXP =>", l2_norm)
    
    print(f"\033[33m L2 Norm \033[0mof RANS to EXP => ", l2_norm_r)
    
    print(f"\033[33m L2 Norm \033[0mof RANS to LES => ",l2_norm_bet,"\n")
    

    
max_value = max(*l2_norm_rans)
print("Max of L2 Norm of RANS to EXP => ",max_value)

directory_path = os.getcwd()

log_files = glob.glob(directory_path + "/dome.log*")

file_path = log_files
for path in file_path:
    with open(path, "a") as file:
        file.write("Max of L2 Norm of RANS to EXP : "+str(max_value) + "\n")  # Write the value to the file




