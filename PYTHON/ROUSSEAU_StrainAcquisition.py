# -*- coding: 'unicode' -*-
# Copyright (c) 2021 KEYENCE CORPORATION. All rights reserved.

import LJXAwrap

import ctypes
import sys
import time


import numpy as np
import matplotlib.pyplot as plt
import PySimpleGUI as sg

##############################################################################
# sample_ImageAcquisition.py: LJ-X8000A Image acquisition sample.
#
# -First half part: Describes how to acquire images via LJXAwrap I/F.
# -Second half part: Describes how to display images using additional modules.
#
##############################################################################


##############################################################################
# Define global variables to be manipulated throughout the script.
##############################################################################

def main(): 
    force = []  # Array to store the data values 
    force2 = []
    
    # Define the layout of the GUI 
    layout = [
    [sg.Text('Enter a force value (N):'), sg.Input(key='-INPUT-')],
    [sg.Button('Add'), sg.Button('Exit')],
    [sg.Listbox(values=[], size=(40, 10), key='-LISTBOX-')]
    ]
    
    # Create the window
    window = sg.Window('Data Entry', layout)
    
    # Event loop
    while True:
        event, values = window.read() 
        
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        elif event == 'Add':
                value = values['-INPUT-']
        if value:  # Check if a value was entered
            try:
                value = int(value)  # Convert input to integer
                force.append(value)
                window['-LISTBOX-'].update(force)  # Update the listbox with the new data
                window['-INPUT-'].update('')  # Clear the input field

                
                image_available = False  # Flag to confirm the completion of image acquisition.
                ysize_acquired = 0       # Number of Y lines of acquired image.
                z_val = []               # The buffer for height image.
                lumi_val = []            # The buffer for luminance image.


                def main():

                    global image_available
                    global ysize_acquired
                    global z_val
                    global lumi_val

                    ##################################################################
                    # CHANGE THIS BLOCK TO MATCH YOUR SENSOR SETTINGS (FROM HERE)
                    ##################################################################

                    deviceId = 0                        # Set "0" if you use only 1 head.
                    ysize = 10                         # Number of measurements desired.
                    timeout_sec = 10                   # Timeout value for the acquiring image
                    use_external_batchStart = False     # 'True' if you start batch externally.

                    ethernetConfig = LJXAwrap.LJX8IF_ETHERNET_CONFIG()
                    ethernetConfig.abyIpAddress[0] = 192    # IP address
                    ethernetConfig.abyIpAddress[1] = 168
                    ethernetConfig.abyIpAddress[2] = 182
                    ethernetConfig.abyIpAddress[3] = 66
                    ethernetConfig.wPortNo = 24691          # Port No.
                    HighSpeedPortNo = 24692                 # Port No. for high-speed

                    ##################################################################
                    # CHANGE THIS BLOCK TO MATCH YOUR SENSOR SETTINGS (TO HERE)
                    ##################################################################

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
                        
                        fig = plt.figure(figsize=(4.0, 6.0))
                        plt.subplots_adjust(hspace=0.5)

                        # Height profile display
                        ax3 = fig.add_subplot(3, 1, 1)
                        sl = int(xsize * ysize_acquired / 2)  # the horizontal center profile

                        x_val_mm = [0.0] * xsize
                        z_val_mm = [0.0] * xsize
                        for i in range(xsize):
                            # Conver X data to the actual length in millimeters
                            x_val_mm[i] = (profinfo.lXStart + profinfo.lXPitch * i)/100.0  # um
                            x_val_mm[i] /= 1000.0  # mm

                            # Conver Z data to the actual length in millimeters
                            if z_val[sl + i] == 0:  # invalid value
                                z_val_mm[i] = np.nan
                            else:
                                # 'Simple array data' is offset to be unsigned 16-bit data.
                                # Decode by subtracting 32768 to get a signed value.
                                z_val_mm[i] = int(z_val[sl + i]) - 32768  # decode
                                z_val_mm[i] *= ZUnit.value / 100.0  # um
                                z_val_mm[i] /= 1000.0  # mm
                            
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

                        ax3.plot(x_val_mm, z_val_mm)

                        plt.title("Height Profile 1")
                        
                        # Create total Z array in mm (represents every line)
                        zsize = len(z_val)
                        z_val_tot_mm = [0.0] * zsize
                        for i in range(zsize):
                            # Conver Z data to the actual length in millimeters
                            if z_val[i] == 0:  # invalid value
                                z_val_tot_mm[i] = -25
                            else:
                                # 'Simple array data' is offset to be unsigned 16-bit data.
                                # Decode by subtracting 32768 to get a signed value.
                                z_val_tot_mm[i] = int(z_val[i]) - 32768  # decode
                                z_val_tot_mm[i] *= ZUnit.value / 100.0  # um
                                z_val_tot_mm[i] /= 1000.0  # mm
                        
                        # Find the max z in every line taken
                        max_values1 = []
                        max_values2 = []
                        indices1 = []
                        indices2 = []
                        lengths = []
                        
                        for i in range(0, zsize, xsize): 
                            chunk = z_val_tot_mm[i:i+xsize]
                            max_value1 = max(chunk[0:int(xsize/2)]) 
                            max_value2 = max(chunk[int(xsize/2):xsize])
                            index1 = chunk.index(max_value1)
                            index2 = chunk.index(max_value2)
                            max_values1.append(max_value1) 
                            max_values2.append(max_value2)
                            indices1.append(index1)
                            indices2.append(index2)
                            length = x_val_mm[index2]-x_val_mm[index1]
                            lengths.append(length)
                            
                        print(max_values1)
                        print (max_values2)
                        print(indices1)
                        print(indices2)
                        print(lengths)
                        
                        # Find the two max Z values on either side of the center



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
    print(force)
    
if __name__ == '__main__': 
    main()



