# -*- coding: 'unicode' -*-
# Copyright (c) 2021 KEYENCE CORPORATION. All rights reserved.
# This script takes samples from the sample_ImageAcquisition.py script made 
# by Keyence.


import LJXAwrap # Import Keyence wrapper script
import ctypes
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
import PySimpleGUI as sg # Install pysimplegui with pip
from astropy import modeling


##############################################################################
# StrainAcquisition.py: LJ-X8000A to acquire strain data using a specimen with
# clear extrusions by collecting line profiles.
##############################################################################


##############################################################################
# Define global variables to be manipulated throughout the script.
##############################################################################

force = [] # Array to store manually entered force data
stress = [] # Array to store stress data
lengths = [] # Specimen lengths at each measurement point
strain = [] # Strain at each measurement point (relies on input gauge length)
status_info = {} # Dataset of helpful data 

def main(): 
    global force
    global lengths
    global strain
    global stress
    
    
    ###########################################################################
    # GUI
    ###########################################################################
    
    # Define the layout of the GUI 
    layout = [
    [sg.Text('Enter a force value (N):'), sg.Input(key='-INPUT-')],
    [sg.Button('Add'), sg.Button('Done')],
    [sg.Listbox(values=[], size=(40, 10), key='-LISTBOX-')]
    ]
    
    # Create the window
    window = sg.Window('Data Entry', layout)
    
    # Event loop for GUI inputs
    while True:
        event, values = window.read() 

        if event == sg.WINDOW_CLOSED or event == 'Done':
            break
        elif event == 'Add':
                value = values['-INPUT-']
        if value:  # Check if a value was entered
            try:
                value = int(value)  # Convert input to integer
                force.append(value)
                window['-LISTBOX-'].update(force)  # Update the listbox with the new data
                window['-INPUT-'].update('')  # Clear the input field
                
                
                ###############################################################
                # Define more global variables.
                ###############################################################
                image_available = False  # Flag to confirm the completion of image acquisition.
                ysize_acquired = 0       # Number of Y lines of acquired image.
                z_val = []               # The buffer for height image.
                
                
                ###############################################################
                # CHANGE THIS BLOCK TO MATCH YOUR SPECIMEN PROPERTIES
                ###############################################################
                                    
                gauge_length = 33.5 # Specimen gauge length (mm)
                cross_section = 40.3225 # Specimen cross sectional area (mm^2)

                ###############################################################
                # CHANGE THIS BLOCK TO MATCH YOUR SAMPLE PROPERTIES
                ###############################################################

                def main():

                    global image_available
                    global ysize_acquired
                    global z_val
                    global lumi_val


                    ###########################################################
                    # CHANGE THIS BLOCK TO MATCH YOUR SENSOR SETTINGS
                    ###########################################################

                    deviceId = 0                        # Set "0" if you use only 1 head.
                    ysize = 10                        # Number of measurements desired (Must be even #).
                    timeout_sec = 10                   # Timeout value for the acquiring image
                    use_external_batchStart = False     # 'True' if you start batch externally.

                    ethernetConfig = LJXAwrap.LJX8IF_ETHERNET_CONFIG()
                    ethernetConfig.abyIpAddress[0] = 192    # IP address
                    ethernetConfig.abyIpAddress[1] = 168
                    ethernetConfig.abyIpAddress[2] = 182
                    ethernetConfig.abyIpAddress[3] = 66
                    ethernetConfig.wPortNo = 24691          # Port No.
                    HighSpeedPortNo = 24692                 # Port No. for high-speed

                    ###########################################################
                    # CHANGE THIS BLOCK TO MATCH YOUR SENSOR SETTINGS (TO HERE)
                    ###########################################################
                    
                    
                    ###########################################################
                    # Establish Communication with the Laser
                    ###########################################################

                    # Ethernet open
                    res = LJXAwrap.LJX8IF_EthernetOpen(0, ethernetConfig)
                    print("LJXAwrap.LJX8IF_EthernetOpen:", hex(res))
                    if res != 0:
                        print("Failed to connect controller.")
                        print("Exit the program.")
                        sys.exit()

                    # Initialize Hi-Speed Communication
                    my_callback_s_a = LJXAwrap.LJX8IF_CALLBACK_SIMPLE_ARRAY(callback_s_a)

                    res = LJXAwrap.LJX8IF_InitializeHighSpeedDataCommunicationSimpleArray(
                        deviceId,
                        ethernetConfig,
                        HighSpeedPortNo,
                        my_callback_s_a,
                        ysize,
                        0)
                    print("LJXAwrap.LJX8IF_InitializeHighSpeedDataCommunicationSimpleArray:",
                          hex(res))
                    if res != 0:
                        print("\nExit the program.")
                        sys.exit()

                    # PreStart Hi-Speed Communication
                    req = LJXAwrap.LJX8IF_HIGH_SPEED_PRE_START_REQ()
                    req.bySendPosition = 2
                    profinfo = LJXAwrap.LJX8IF_PROFILE_INFO()
                    

                    res = LJXAwrap.LJX8IF_PreStartHighSpeedDataCommunication(
                        deviceId,
                        req,
                        profinfo)
                    print("LJXAwrap.LJX8IF_PreStartHighSpeedDataCommunication:", hex(res))
                    if res != 0:
                        print("\nExit the program.")
                        sys.exit()

                    # allocate the memory
                    xsize = profinfo.wProfileDataCount
                    z_val = [0] * xsize * ysize
                    lumi_val = [0] * xsize * ysize

                    # Start Hi-Speed Communication
                    image_available = False
                    res = LJXAwrap.LJX8IF_StartHighSpeedDataCommunication(deviceId)
                    print("LJXAwrap.LJX8IF_StartHighSpeedDataCommunication:", hex(res))
                    if res != 0:
                        print("\nExit the program.")
                        sys.exit()

                    # Start Measure (Start Batch)
                    if use_external_batchStart is False:
                        LJXAwrap.LJX8IF_StartMeasure(deviceId)

                    # wait for the image acquisition complete
                    start_time = time.time()
                    while True:
                        if image_available:
                            break
                        if time.time() - start_time > timeout_sec:
                            break

                    # Stop
                    res = LJXAwrap.LJX8IF_StopHighSpeedDataCommunication(deviceId)
                    print("LJXAwrap.LJX8IF_StoptHighSpeedDataCommunication:", hex(res))

                    # Finalize
                    res = LJXAwrap.LJX8IF_FinalizeHighSpeedDataCommunication(deviceId)
                    print("LJXAwrap.LJX8IF_FinalizeHighSpeedDataCommunication:", hex(res))

                    # Close
                    res = LJXAwrap.LJX8IF_CommunicationClose(deviceId)
                    print("LJXAwrap.LJX8IF_CommunicationClose:", hex(res))

                    if image_available is not True:
                        print("\nFailed to acquire image (timeout)")
                        print("\nTerminated normally.")
                        sys.exit()

                    ##################################################################
                    # Information of the acquired image
                    ##################################################################
                    ZUnit = ctypes.c_ushort()
                    LJXAwrap.LJX8IF_GetZUnitSimpleArray(deviceId, ZUnit)

                    print("----------------------------------------")
                    print(" Number of X points    : ", profinfo.wProfileDataCount)
                    print(" Number of measurements: ", ysize_acquired)
                    print(" X pitch in micrometer : ", profinfo.lXPitch / 100.0)
                    print(" Z pitch in micrometer : ", ZUnit.value / 100.0)
                    print("----------------------------------------")


                    ##################################################################
                    # Display part:
                    #
                    # <NOTE> Additional modules are required to execute the next block.
                    # -'Numpy' for handling array data.
                    # -'matplotlib' for profile display.
                    #
                    # If you want to skip,
                    # set the next conditional branch to 'False'.
                    #
                    ##################################################################
                    if True:
                        
                        fig = plt.figure(figsize=(8.0, 8.0))
                        plt.subplots_adjust(hspace=0.5)

                        # Height profile display
                        ax1 = fig.add_subplot(2, 2, 1)
                        sl = int(xsize * ysize_acquired / 2)  # the horizontal center profile

                        x_val_mm = [0.0] * xsize
                        z_val_mm = [0.0] * xsize
                        for i in range(xsize):
                            # Conver X data to the actual length in millimeters
                            x_val_mm[i] = (profinfo.lXStart + profinfo.lXPitch * i)/100.0  # um
                            x_val_mm[i] /= 1000.0  # mm

                            # Conver Z data to the actual length in millimeters
                            if z_val[sl + i] == 0:  # invalid value
                                z_val_mm[i] = -25
                            else:
                                # 'Simple array data' is offset to be unsigned 16-bit data.
                                # Decode by subtracting 32768 to get a signed value.
                                z_val_mm[i] = int(z_val[sl + i]) - 32768  # decode
                                z_val_mm[i] *= ZUnit.value / 100.0  # um
                                z_val_mm[i] /= 1000.0  # mm
                                
                        f = open('Strain_Distance.txt','a')
                        for i in range(xsize):
                            f.write(str(z_val_mm[i]) + '\n')
                        f.write('\n')
                            
                        plotz_min = np.nanmin(z_val_mm)
                        if np.isnan(plotz_min):
                            plotz_min = -1.0
                        else:
                            plotz_min -= 1.0
                            
                        plotz_max = np.nanmax(z_val_mm)
                        if np.isnan(plotz_max):
                            plotz_max = 1.0
                        else:
                            plotz_max += 1.0

                        plt.ylim(plotz_min, plotz_max)

                        ax1.plot(x_val_mm, z_val_mm)

                        plt.title("Height Profile 1")
                        

                        # Find extrema of profile (must be at least 2 mm apart)
                        max_value1 = max(z_val_mm)
                        index1 = z_val_mm.index(max_value1)
                        print(max_value1)
                        print(index1)
                        
                        if max(z_val_mm[0:index1-160]) > max(z_val_mm[index1+160:xsize]):
                            max_value2 = max(z_val_mm[0:index1-160])
                            index2 = z_val_mm[0:index1-160].index(max_value2)
                        else:
                            max_value2 = max(z_val_mm[index1+160:xsize])
                            index2 = z_val_mm[index1+160:xsize].index(max_value2)+index1+160
                            
                        print(max_value2)
                        print(index2)
                        
                        
                        # Wires
                        wire_red = []
                        for i in range(xsize):
                            if z_val_mm[i] != -25:
                                wire_red.append(z_val_mm[i])
                                
                                
                        wire1_index = []
                        wire1_zval = []
                        for i in range(index1-160,index1+160):
                            if z_val_mm[i] > np.average(wire_red)*1.10:
                                wire1_index.append(i)
                                wire1_zval.append(z_val_mm[i])
                                
                        wire1_z = []
                        for i in range(len(wire1_zval)):
                            wire1_z.append(wire1_zval[i] - np.min(wire1_zval))
                        
                        x1_peak = range(0,len(wire1_zval))
                        
                        print(wire1_index)
                        ax3 = fig.add_subplot(2,2,3)
                        ax3.plot(x1_peak,wire1_z,'o',color = 'red')
                        plt.title('Wire 1')
                        
                        wire2_index = []
                        wire2_zval = []
                        for i in range(index2-160,index2+160):
                            if z_val_mm[i] > np.average(wire_red)*1.10:
                                wire2_index.append(i)
                                wire2_zval.append(z_val_mm[i])
                        print(np.min(wire2_zval))
                        wire2_z = []
                        for i in range(len(wire2_zval)):
                            wire2_z.append(wire2_zval[i] - np.min(wire2_zval))
                        
                        x2_peak = range(0,len(wire2_zval))
                        
                        print(wire2_index)
                        ax4 = fig.add_subplot(2,2,4)
                        ax4.plot(x2_peak,wire2_z,'o',color = 'red')
                        plt.title('Wire 2')
                        
                        
                        # Gaussian Fit
                        fitter = modeling.fitting.LevMarLSQFitter()
                        model = modeling.models.Gaussian1D()   # depending on the data you need to give some initial values
                        fitted_model1 = fitter(model, x1_peak, wire1_z)
                        ax3.plot(x1_peak, fitted_model1(x1_peak),color = 'green')
                        model1_list = fitted_model1(x1_peak).tolist()
                        model1_max = np.max(model1_list)
                        model1_index = model1_list.index(model1_max)
                        index1 = wire1_index[model1_index]
                        print(index1)
                        
                        
                        fitter = modeling.fitting.LevMarLSQFitter()
                        model = modeling.models.Gaussian1D()   # depending on the data you need to give some initial values
                        fitted_model2 = fitter(model, x2_peak, wire2_z)
                        ax4.plot(x2_peak, fitted_model2(x2_peak),color = 'green')
                        model2_list = fitted_model2(x2_peak).tolist()
                        model2_max = np.max(model2_list)
                        model2_index = model2_list.index(model2_max)
                        index2 = wire2_index[model2_index]
                        print(index2)
                        
                        
                        # Calculate length between extrema based on laser 
                        # resolution and determine strain
                        length = abs(x_val_mm[index2]-x_val_mm[index1])
                        lengths.append(length)        
                        strain.append((length-gauge_length)/length)
                        
                        # Convert force to stress
                        stress.append(force[-1]/cross_section)
                        
                        status = { 
                            'Peak 1': max_value1,
                            'Index 1': index1,
                            'Peak 2': max_value2,
                            'Index 2': index2,
                            'Length': length,
                        }
                        
                        status_info['status'] = status
                        
                        ax2 = fig.add_subplot(2, 2, 2)
                        if strain:
                            if force: 
                                ax2.plot(strain,stress, marker = 'o', linestyle = 'dashed')
                                plt.title('Stress-Strain Plot')
                                plt.xlabel('Strain')
                                plt.ylabel('Stress')
                                plt.grid()
                            else:
                                print('No force data avaialable.')
                        else: 
                            print('No force or strain data avaialable.')


                        # Show all plot
                        print("\nPress 'q' key to exit the program...")
                        plt.show()
                        plt.close('all')
                        

                    print("\nTerminated normally.")
                    return


                ###############################################################################
                # Callback function
                # It is called when the specified number of profiles are received.
                ###############################################################################
                def callback_s_a(p_header,
                                 p_height,
                                 p_lumi,
                                 luminance_enable,
                                 xpointnum,
                                 profnum,
                                 notify, user):

                    global ysize_acquired
                    global image_available
                    global z_val
                    global lumi_val

                    if (notify == 0) or (notify == 0x10000):
                        if profnum != 0:
                            if image_available is False:
                                for i in range(xpointnum * profnum):
                                    z_val[i] = p_height[i]
                                    if luminance_enable == 1:
                                        lumi_val[i] = p_lumi[i]

                                ysize_acquired = profnum
                                image_available = True
                    return


                if __name__ == '__main__':
                    main()
            except ValueError:
                    sg.popup('Please enter a valid integer.')  # Show an error message for invalid input
    
    window.close()
    
if __name__ == '__main__': 
    main()




