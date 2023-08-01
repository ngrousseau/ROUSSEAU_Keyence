# -*- coding: utf-8 -*-

import PySimpleGUI as sg # Install pysimplegui with pip
import math
import numpy as np


def main():
    
    #####################################################
    # CHANGE THIS BLOCK TO MATCH STAGE LIMITS (FROM HERE)
    #####################################################
    
    # Motor Limits in X, Y, Z (mm)
    [x_min,x_max] = [1,149]
    [y_min,y_max] = [1,149]
    [z_min,z_max] = [0,49]
    
    # Motor steps/mm
    x_steps = 1
    y_steps = 1
    phi_steps = 1
    
    # Stage dimensions in the direction of the x and y motors (mm)
    [stage_x,stage_y] = [150,100]
    
    # Distance from the center of rotation to the laser (mm)
    center_dist = 170
    
    # Does the stage rotate clockwise (0) or counterclockwise (1)
    stage_rot = 0
    

    # WHEN THE ANGLE OF THE STAGE EQUALS 0 DEGREES
    
    # What motor moves the stage towards the laser? X (0) or Y (1)
    motor_parallel = 0
    
    # For the motor that moves the stage towards the laser, is the direction
    # towards the laser negative (0) or positive (1)
    motor_parallel_0 = 1
    
    

    # WHEN THE ANGLE OF THE STAGE EQUALS 90 DEGREES
    
    # For the motor that moves the stage towards the laser, is the direction
    # towards the laser negative (0) or positive (1)
    motor_parallel_90 = 1
    
    ###################################################
    # CHANGE THIS BLOCK TO MATCH STAGE LIMITS (TO HERE)
    ###################################################
    
    
    ######################################################################
    # General User Interface (GUI) to define basic properties of the part.
    ######################################################################
    layout = [
        [sg.Text('Select the shape:')],
        [sg.Button('Circle', key='-CIRCLE-'), sg.Button('Square', key='-SQUARE-')],
        [sg.Text('Diameter (mm):'), sg.Input(key='-DIAMETER-')],
        [sg.Text('Length (mm):'), sg.Input(key='-LENGTH-')],
        [sg.Text('Width (mm):'), sg.Input(key='-WIDTH-')],
        [sg.Text('Height (mm):'), sg.Input(key='-HEIGHT-')],
        [sg.Button('Submit')]
    ]

    # Create the window
    window = sg.Window('Shape Input', layout)

    # Event loop for GUI inputs
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break
        elif event == '-CIRCLE-':
            window['-DIAMETER-'].update(disabled=False)
            window['-LENGTH-'].update(disabled=True, value='0')
            window['-WIDTH-'].update(disabled=True, value='0')
        elif event == '-SQUARE-':
            window['-DIAMETER-'].update(disabled=True, value='0')
            window['-LENGTH-'].update(disabled=False)
            window['-WIDTH-'].update(disabled=False)

        elif event == 'Submit':
            shape = 'Circle' if float(values['-DIAMETER-']) > 0 else 'Square'
            diameter = float(values['-DIAMETER-']) if shape == 'Circle' else None
            length = float(values['-LENGTH-']) if shape == 'Square' else None
            width = float(values['-WIDTH-']) if shape == 'Square' else None
            height = float(values['-HEIGHT-'])
            break
    window.close()
    
    
    ###########################################
    # ASSOCIATE DIMENSIONS AND PRINT ANY ERRORS
    ###########################################
    if height > 40 + z_max :
        print('PART OR OBJECT IS TOO TALL')
        if __name__ == '__main__':
            main()
    
    
    if length:
        if length > width:
            if stage_y > stage_x:
                if stage_x - 190 > width or stage_y - 190 > length:
                    print('PART OR OBJECT NOT IN RANGE OF LASER, PLEASE USE SMALLER STAGE')
                    if __name__ == '__main__':
                        main()
                if center_dist + np.average([x_min,x_max]) - width < 60 or center_dist + np.average([y_min,y_max]) - length < 60:
                    print('PART OR OBJECT TO CLOSE TO LASER')
                    if __name__ == '__main__':
                        main()
                if motor_parallel == 0:
                    part_parallel = width
                else:
                    part_parallel = length
            else:
                if stage_x - 190 > length or stage_y - 190 > width:
                    print('PART OR OBJECT NOT IN RANGE OF LASER, PLEASE USE SMALLER STAGE')
                    if __name__ == '__main__':
                        main()
                if center_dist + np.average([x_min,x_max]) - length < 60 or center_dist + np.average([y_min,y_max]) - width < 60:
                    print('PART OR OBJECT TO CLOSE TO LASER')
                    if __name__ == '__main__':
                        main()
                if motor_parallel == 0:
                    part_parallel = length
                else:
                    part_parallel = width
        else:
            if stage_y > stage_x:
                if stage_x - 190 > length or stage_y - 190 > width:
                    print('PART OR OBJECT NOT IN RANGE OF LASER, PLEASE USE SMALLER STAGE')
                    if __name__ == '__main__':
                        main()
                if center_dist + np.average([x_min,x_max]) - length < 60 or center_dist + np.average([y_min,y_max]) - width < 60:
                    print('PART OR OBJECT TO CLOSE TO LASER')
                    if __name__ == '__main__':
                        main()
                if motor_parallel == 0:
                    part_parallel = length
                else:
                    part_parallel = width
            else:
                if stage_x - 190 > width or stage_y - 190 > length:
                    print('PART OR OBJECT NOT IN RANGE OF LASER, PLEASE USE SMALLER STAGE')
                    if __name__ == '__main__':
                        main()
                if center_dist + np.average([x_min,x_max]) - width < 60 or center_dist + np.average([y_min,y_max]) - length < 60:
                    print('PART OR OBJECT TO CLOSE TO LASER')
                    if __name__ == '__main__':
                        main()
                if motor_parallel == 0:
                    part_parallel = width
                else:
                    part_parallel = length
                    
        if part_parallel == width:
            part_perp = length
        else:
            part_perp = width
    
    
    # Define the center point and limits of the motors and stage.
    if motor_parallel == 0:
        center_perp = np.average([y_min,y_max])
        center_parallel = np.average([x_min,x_max])
        stage_perp = stage_y
        perp_limits = [y_min,y_max]
        stage_parallel = stage_x
        parallel_limits = [x_min,x_max]
    else:
        center_perp = np.average([x_min,x_max])
        center_parallel = np.average([y_min,y_max])
        stage_perp = stage_x
        perp_limits = [x_min,x_max]
        stage_parallel = stage_y
        parallel_limits = [y_min,y_max]
    
    
    #####################################################
    # WHEN THE ANGLE OF THE STAGE EQUALS 0 OR 180 DEGREES
    #####################################################
    
    if length:
    
        # Motor position when the part is 60 mm away. 
        factor_parallel = center_dist -  part_parallel/2 - 60
        safety_factor_parallel = center_dist -  stage_parallel/2 - 5
        if motor_parallel_0 == 0:
            if center_parallel - safety_factor_parallel > parallel_limits[0]:
                parallel_limits[0] = center_parallel - safety_factor_parallel
                
            if center_parallel - factor_parallel < parallel_limits[0]:
                parallel_60_0 = parallel_limits[0]
            else:
                parallel_60_0 = center_parallel - factor_parallel
            
            if center_parallel + safety_factor_parallel < parallel_limits[1]:
                parallel_limits[1] = center_parallel + safety_factor_parallel
                
            if center_parallel + factor_parallel > parallel_limits[1]:
                parallel_60_180 = parallel_limits[1]
            else:
                parallel_60_180 = center_parallel + factor_parallel  
        else:
            if center_parallel - safety_factor_parallel > parallel_limits[0]:
                parallel_limits[0] = center_parallel - safety_factor_parallel
                
            if center_parallel - factor_parallel < parallel_limits[0]:
                parallel_60_180 = parallel_limits[0]
            else:
                parallel_60_180 = center_parallel - factor_parallel
            
            if center_parallel + safety_factor_parallel < parallel_limits[1]:
                parallel_limits[1]= center_parallel + safety_factor_parallel
                
            if center_parallel + factor_parallel > parallel_limits[1]:
                parallel_60_0 = parallel_limits[1]
            else:
                parallel_60_0 = center_parallel + factor_parallel    
    
    
        ######################################################
        # WHEN THE ANGLE OF THE STAGE EQUALS 90 OR 270 DEGREES
        ######################################################
    
        # Motor position when the part is 60 mm away. 
        factor_perp = center_dist -  part_perp/2 - 60
        safety_factor_perp = center_dist - stage_perp/2 - 5
        if motor_parallel_90 == 0:
            if center_perp - safety_factor_perp > perp_limits[0]:
                perp_limits[0] = center_perp - safety_factor_perp
                
            if center_perp - factor_perp < perp_limits[0]:
                perp_60_90 = perp_limits[0]
            else:
                perp_60_90 = center_perp - factor_perp
                
            if center_perp + safety_factor_perp < perp_limits[1]:
                perp_limits[1] = center_perp + safety_factor_perp
                
            if center_perp + factor_perp > perp_limits[1]:
                perp_60_270 = perp_limits[1]
            else:
                perp_60_270 = center_perp + factor_perp
        else:
            if center_perp - safety_factor_perp > perp_limits[0]:
                perp_limits[0] = center_perp - safety_factor_perp
            
            if center_perp - factor_perp < perp_limits[0]:
                perp_60_270 = perp_limits[0]
            else:
                perp_60_270 = center_perp - factor_perp
            
            if center_perp + safety_factor_perp < perp_limits[1]:
                perp_limits[1] = center_perp + safety_factor_perp
            
            if center_perp + factor_perp > perp_limits[1]:
                perp_60_90 = perp_limits[1]
            else:
                perp_60_90 = center_perp + factor_perp
        
        
        #####################
        # ASSIGNING VARIABLES
        #####################
        
        if motor_parallel == 0: # If motor going towards laser is X
            [motor_x1_0,motor_x2_0] = [parallel_60_0,parallel_60_0] 
            [motor_y1_90,motor_y2_90] = [perp_60_90,perp_60_90]
            [motor_x1_180,motor_x2_180] = [parallel_60_180,parallel_60_180] 
            [motor_y1_270,motor_y2_270] = [perp_60_270,perp_60_270]
        
            if motor_parallel_0 == 0: # If the motor towards laser is negative 
                if motor_parallel_90 == 0: # If the other motor at 90 is neg
                    [motor_y1_0,motor_y2_0] = [y_min,y_max]
                    [motor_x1_90,motor_x2_90] = [x_max,x_min] 
                else: # Other motor at 90 is positive
                    [motor_y1_0,motor_y2_0] = [y_max,y_min]
                    [motor_x1_90,motor_x2_90] = [x_max,x_min] 
            else: # Motor towards laser is positive
                if motor_parallel_90 == 0: 
                    [motor_y1_0,motor_y2_0] = [y_min,y_max]
                    [motor_x1_90,motor_x2_90] = [x_min,x_max] 
                else:
                    [motor_y1_0,motor_y2_0] = [y_max,y_min]
                    [motor_x1_90,motor_x2_90] = [x_min,x_max]  
                    
            [motor_y1_180,motor_y2_180] = [motor_y2_0,motor_y1_0]
            [motor_x1_270,motor_x2_270] = [motor_x2_90,motor_x1_90]
        
        else:
            [motor_y1_0,motor_y2_0] = [parallel_60_0,parallel_60_0]
            [motor_x1_90,motor_x2_90] = [perp_60_90,perp_60_90] 
            [motor_y1_180,motor_y2_180] = [parallel_60_180,parallel_60_180]
            [motor_x1_270,motor_x2_270] = [perp_60_270,perp_60_270] 
        
            if motor_parallel_0 == 0: # If the motor towards laser is negative 
                if motor_parallel_90 == 0: # If the other motor at 90 is neg
                    [motor_x1_0,motor_x2_0] = [x_min,x_max]
                    [motor_y1_90,motor_y2_90] = [y_max,y_min] 
                else: # Other motor at 90 is positive
                    [motor_x1_0,motor_x2_0] = [x_max,x_min]
                    [motor_y1_90,motor_y2_90] = [y_max,y_min] 
            else: # Motor towards laser is positive
                if motor_parallel_90 == 0: 
                    [motor_x1_0,motor_x2_0] = [x_min,x_max]
                    [motor_y1_90,motor_y2_90] = [y_min,y_max] 
                else:
                    [motor_x1_0,motor_x2_0] = [x_max,x_min]
                    [motor_y1_90,motor_y2_90] = [y_min,y_max]  
                    
            [motor_x1_180,motor_x2_180] = [motor_x2_0,motor_x1_0]
            [motor_y1_270,motor_y2_270] = [motor_y2_90,motor_y1_90]
    
        
    ############################################################
    # Writing SPEC Commands to a Text File Based on User Inputs.
    ############################################################
   
    g = open('SPEC_SIZE.txt','w')
    
    f = open('SPEC.txt','w')
    f.write('1 ' + "{:.6f}".format(np.average([x_min,x_max])) + ' ' +  "{:.6f}".format(np.average([y_min,y_max])) + ' ' + str(z_max) + ' 0.000000 0' + ' ' +  str(stage_rot) + '\n')
    count = 1
    
    if shape == 'Circle':
        if diameter <= 40:
            if height <= 40:
                
                # Height and diameter are less than 40 mm and the shape is
                # a circle.
                for i in range(phi_steps*360):
                    count = count + 1
                    f.write(str(count) + ' ' +  "{:.6f}".format(np.average([x_min,x_max])) + ' ' +  "{:.6f}".format(np.average([y_min,y_max])) + ' ' + str(z_max) + ' ' + "{:.6f}".format((i+1)/phi_steps) + ' ' + '1' + ' ' +  str(stage_rot) + '\n')
                count = count + 1
                f.write(str(count) + ' ' +  "{:.6f}".format(np.average([x_min,x_max])) + ' ' +  "{:.6f}".format(np.average([y_min,y_max])) + ' ' + str(z_max) + ' 0.000000 0' + ' ' +  str(stage_rot) + '\n')
                g.write('1 ' + str(count) + '\n' + '2 ' + str(count))
            
            else:
                # The diameter is less than 40 mm, the height is more than 40
                # mm and the shape is a circle
                height_chunk = math.ceil(height/40)
                for j in range(height_chunk):
                    if z_max-40*j < z_min:
                        z_factor = 0
                    else:
                        z_factor = z_max-40*j
                    for i in range(phi_steps*360):
                        count = count + 1
                        f.write(str(count) + ' ' +  "{:.6f}".format(np.average([x_min,x_max])) + ' ' +  "{:.6f}".format(np.average([y_min,y_max])) + ' ' + str(z_factor) + ' ' +  "{:.6f}".format((i+1)/phi_steps) + ' ' + '1' + ' ' + str(stage_rot) + '\n')
                    if z_max-40*(j+1) > z_max-40*height_chunk:
                        z_factor = z_max-40*(j+1)
                        if z_factor < z_min:
                            z_factor = z_min
                        count = count + 1
                        f.write(str(count) + ' ' +  "{:.6f}".format(np.average([x_min,x_max])) + ' ' +  "{:.6f}".format(np.average([y_min,y_max])) + ' ' + str(z_factor) + ' 0.000000 0' + ' ' + str(stage_rot) + '\n')
                    else:
                        count = count + 1
                        f.write(str(count) + ' ' +  "{:.6f}".format(np.average([x_min,x_max])) + ' ' +  "{:.6f}".format(np.average([y_min,y_max])) + ' ' + str(z_max) + ' 0.000000 0' + ' ' + str(stage_rot) + '\n')
                    g.write('1 ' + str(count) + '\n' + '2 ' + str(count))
                
        else:
            if height <= 40:
                # Height is less than 40 mm, the diameter is more than 
                # 40 mm and the shape is a circle.
                for i in range(phi_steps*360):
                    count = count + 1
                    f.write(str(count) + ' ' +  "{:.6f}".format(np.average([x_min,x_max])) + ' ' +  "{:.6f}".format(np.average([y_min,y_max])) + ' ' + str(z_max) + ' ' +  "{:.6f}".format((i+1)/phi_steps) + ' ' + '1' + ' ' + str(stage_rot) + '\n')
                count = count + 1
                f.write(str(count) + ' ' +  "{:.6f}".format(np.average([x_min,x_max])) + ' ' +  "{:.6f}".format(np.average([y_min,y_max])) + ' ' + str(z_max) + ' 0.000000 0' + ' ' + str(stage_rot) + '\n')
                g.write('1 ' + str(count) + '\n' + '2 ' + str(count))
                
            else:
                # The diameter and height are greater than 40 mm and the shape 
                # is a circle
                height_chunk = math.ceil(height/40)
                for j in range(height_chunk):
                    if z_max-40*j < z_min:
                        z_factor = 0
                    else:
                        z_factor = z_max-40*j
                    for i in range(phi_steps*360):
                        count = count + 1
                        f.write(str(count) + ' ' +  "{:.6f}".format(np.average([x_min,x_max])) + ' ' +  "{:.6f}".format(np.average([y_min,y_max])) + ' ' + str(z_factor) + ' ' +  "{:.6f}".format((i+1)/phi_steps) + ' ' + '1' + ' ' + str(stage_rot) + '\n')
                    if z_max-40*(j+1) > z_max-40*height_chunk:
                        z_factor = z_max-40*(j+1)
                        if z_factor < z_min:
                            z_factor = z_min
                        count = count + 1
                        f.write(str(count) + ' ' +  "{:.6f}".format(np.average([x_min,x_max])) + ' ' +  "{:.6f}".format(np.average([y_min,y_max])) + ' ' + str(z_factor) + ' 0.000000 0' + ' ' + str(stage_rot) + '\n')
                    else:
                        count = count + 1
                        f.write(str(count) + ' ' +  "{:.6f}".format(np.average([x_min,x_max])) + ' ' +  "{:.6f}".format(np.average([y_min,y_max])) + ' ' + str(z_max) + ' 0.000000 0' + ' ' + str(stage_rot) + '\n')
                    g.write('1 ' + str(count) + '\n' + '2 ' + str(count))
                    
    else:
        if height <= 40:
            # Height is less than 40 mm and the shape is a square.
            count = count + 1
            f.write(str(count) + ' ' +  "{:.6f}".format(motor_x1_0) + ' ' +  "{:.6f}".format(motor_y1_0) + ' ' + str(z_max) + ' 0.000000' + ' ' + '1' + ' ' + str(stage_rot) + '\n')
            if motor_x1_0 == motor_x2_0:
                for i in range(y_steps*((abs(motor_y2_0-motor_y1_0)))):
                    count = count + 1
                    f.write(str(count) + ' ' +  "{:.6f}".format(motor_x2_0) + ' ' +  "{:.6f}".format(motor_y1_0-(i+1)*(motor_y1_0-motor_y2_0)/(y_steps*((abs(motor_y2_0-motor_y1_0))))) + ' ' + str(z_max) + ' 0.000000' + ' ' + '1' + ' ' + str(stage_rot) + '\n')
            else:
                for i in range(x_steps*((abs(motor_x2_0-motor_x1_0)))):
                    count = count + 1
                    f.write(str(count) + ' ' +  "{:.6f}".format(motor_x1_0-(i+1)*(motor_x1_0-motor_x2_0)/(x_steps*((abs(motor_x2_0-motor_x1_0))))) + ' ' +  "{:.6f}".format(motor_y2_0) + ' ' + str(z_max) + ' 0.000000' + ' ' + '1' + ' ' + str(stage_rot) + '\n')
            
            count = count + 1
            f.write(str(count) + ' ' +  "{:.6f}".format(np.average([x_min,x_max])) + ' ' +  "{:.6f}".format(np.average([y_min,y_max])) + ' ' + str(z_max) + ' 0.000000 0' + ' ' + str(stage_rot) + '\n')
            count = count + 1
            f.write(str(count) + ' ' +  "{:.6f}".format(np.average([x_min,x_max])) + ' ' +  "{:.6f}".format(np.average([y_min,y_max])) + ' ' + str(z_max) + ' 90.000000 0' + ' ' + str(stage_rot) + '\n')
            
            count = count + 1
            f.write(str(count) + ' ' +  "{:.6f}".format(motor_x1_90) + ' ' +  "{:.6f}".format(motor_y1_90) + ' ' + str(z_max) + ' 90.000000' + ' ' + '1' + ' ' + str(stage_rot) + '\n')
            if motor_x1_90 == motor_x2_90:
                for i in range(y_steps*((abs(motor_y2_90-motor_y1_90)))):
                    count = count + 1
                    f.write(str(count) + ' ' +  "{:.6f}".format(motor_x2_90) + ' ' +  "{:.6f}".format(motor_y1_90-(i+1)*(motor_y1_90-motor_y2_90)/(y_steps*((abs(motor_y2_90-motor_y1_90))))) + ' ' + str(z_max) + ' 90.000000' + ' ' + '1' + ' ' + str(stage_rot) + '\n')
            else:
                for i in range(x_steps*((abs(motor_x2_90-motor_x1_90)))):
                    count = count + 1
                    f.write(str(count) + ' ' +  "{:.6f}".format(motor_x1_90-(i+1)*(motor_x1_90-motor_x2_90)/(x_steps*((abs(motor_x2_90-motor_x1_90))))) + ' ' +  "{:.6f}".format(motor_y2_90) + ' ' + str(z_max) + ' 90.000000' + ' ' + '1' + ' ' + str(stage_rot) + '\n')
            
            count = count + 1
            f.write(str(count) + ' ' +  "{:.6f}".format(np.average([x_min,x_max])) + ' ' +  "{:.6f}".format(np.average([y_min,y_max])) + ' ' + str(z_max) + ' 90.000000 0' + ' ' + str(stage_rot) + '\n')
            count = count + 1
            f.write(str(count) + ' ' +  "{:.6f}".format(np.average([x_min,x_max])) + ' ' +  "{:.6f}".format(np.average([y_min,y_max])) + ' ' + str(z_max) + ' ' + '180.000000 0' + ' ' + str(stage_rot) + '\n')
            
            count = count + 1
            f.write(str(count) + ' ' +  "{:.6f}".format(motor_x1_180) + ' ' +  "{:.6f}".format(motor_y1_180) + ' ' + str(z_max) + ' ' + '180.000000' + ' ' + '1' + ' ' + str(stage_rot) + '\n')
            if motor_x1_180 == motor_x2_180:
                for i in range(y_steps*((abs(motor_y2_180-motor_y1_180)))):
                    count = count + 1
                    f.write(str(count) + ' ' +  "{:.6f}".format(motor_x2_180) + ' ' +  "{:.6f}".format(motor_y1_180-(i+1)*(motor_y1_180-motor_y2_180)/(y_steps*((abs(motor_y2_180-motor_y1_180))))) + ' ' + str(z_max) + ' ' + '180.000000' + ' ' + '1' + ' ' + str(stage_rot) + '\n')
            else:
                for i in range(x_steps*((abs(motor_x2_180-motor_x1_180)))):
                    count = count + 1
                    f.write(str(count) + ' ' +  "{:.6f}".format(motor_x1_180-(i+1)*(motor_x1_180-motor_x2_180)/(x_steps*((abs(motor_x2_180-motor_x1_180))))) + ' ' +  "{:.6f}".format(motor_y2_180) + ' ' + str(z_max) + ' ' + '180.000000' + ' ' + '1' + ' ' + str(stage_rot) + '\n')
            
            count = count + 1
            f.write(str(count) + ' ' +  "{:.6f}".format(np.average([x_min,x_max])) + ' ' +  "{:.6f}".format(np.average([y_min,y_max])) + ' ' + str(z_max) + ' ' + '180.000000 0' + ' ' + str(stage_rot) + '\n')
            count = count + 1
            f.write(str(count) + ' ' +  "{:.6f}".format(np.average([x_min,x_max])) + ' ' +  "{:.6f}".format(np.average([y_min,y_max])) + ' ' + str(z_max) + ' 270.000000 0' + ' ' + str(stage_rot) + '\n')            
            
            count = count + 1
            f.write(str(count) + ' ' +  "{:.6f}".format(motor_x1_270) + ' ' +  "{:.6f}".format(motor_y1_270) + ' ' + str(z_max) + ' 270.000000' + ' ' + '1' + ' ' + str(stage_rot) + '\n')
            if motor_x1_270 == motor_x2_270:
                for i in range(y_steps*((abs(motor_y2_270-motor_y1_270)))):
                    count = count + 1
                    f.write(str(count) + ' ' +  "{:.6f}".format(motor_x2_270) + ' ' +  "{:.6f}".format(motor_y1_270-(i+1)*(motor_y1_270-motor_y2_270)/(y_steps*((abs(motor_y2_270-motor_y1_270))))) + ' ' + str(z_max) + ' 270.000000' + ' ' + '1' + ' ' + str(stage_rot) + '\n')
            else:
                for i in range(x_steps*((abs(motor_x2_270-motor_x1_270)))):
                    count = count + 1
                    f.write(str(count) + ' ' +  "{:.6f}".format(motor_x1_270-(i+1)*(motor_x1_270-motor_x2_270)/(x_steps*((abs(motor_x2_270-motor_x1_270))))) + ' ' +  "{:.6f}".format(motor_y2_270) + ' ' + str(z_max) + ' 270.000000' + ' ' + '1' + ' ' + str(stage_rot) + '\n')
            
            count = count + 1
            f.write(str(count) + ' ' +  "{:.6f}".format(np.average([x_min,x_max])) + ' ' +  "{:.6f}".format(np.average([y_min,y_max])) + ' ' + str(z_max) + ' 270.000000 0' + ' ' + str(stage_rot) + '\n')
            count = count + 1
            f.write(str(count) + ' ' +  "{:.6f}".format(np.average([x_min,x_max])) + ' ' +  "{:.6f}".format(np.average([y_min,y_max])) + ' ' + str(z_max) + ' 0.000000 0' + ' ' + str(stage_rot) + '\n')
            g.write('1 ' + str(count) + '\n' + '2 ' + str(count))
            
        else:
            # The height is more than 40 mm and the shape is a square.
            height_chunk = math.ceil(height/40)
            for j in range(height_chunk):
                if z_max-40*j < z_min:
                    z_factor = 0
                else:
                    z_factor = z_max-40*j
                count = count + 1
                f.write(str(count) + ' ' +  "{:.6f}".format(motor_x1_0) + ' ' +  "{:.6f}".format(motor_y1_0) + ' ' + str(z_factor) + ' 0.000000' + ' ' + '1' + ' ' + str(stage_rot) + '\n')
                if motor_x1_0 == motor_x2_0:
                    for i in range(y_steps*((abs(motor_y2_0-motor_y1_0)))):
                        count = count + 1
                        f.write(str(count) + ' ' +  "{:.6f}".format(motor_x2_0) +  "{:.6f}".format(motor_y1_0-(i+1)*(motor_y1_0-motor_y2_0)/(y_steps*((abs(motor_y2_0-motor_y1_0))))) + ' ' + str(z_factor) + ' 0.000000' + ' ' + '1' + ' ' + str(stage_rot) + '\n')
                else:
                    for i in range(x_steps*((abs(motor_x2_0-motor_x1_0)))):
                        count = count + 1
                        f.write(str(count) + ' ' + str(motor_x1_0-(i+1)*(motor_x1_0-motor_x2_0)/(x_steps*((abs(motor_x2_0-motor_x1_0))))) + ' ' +  "{:.6f}".format(motor_y2_0) + ' ' + str(z_factor) + ' 0.000000' + ' ' + '1' + ' ' + str(stage_rot) + '\n')
                
                count = count + 1
                f.write(str(count) + ' ' +  "{:.6f}".format(np.average([x_min,x_max])) + ' ' +  "{:.6f}".format(np.average([y_min,y_max])) + ' ' + str(z_factor) + ' 0.000000 0' + ' ' + str(stage_rot) + '\n')
                count = count + 1
                f.write(str(count) + ' ' +  "{:.6f}".format(np.average([x_min,x_max])) + ' ' +  "{:.6f}".format(np.average([y_min,y_max])) + ' ' + str(z_factor) + ' 90.000000 0' + ' ' + str(stage_rot) + '\n')
                
                count = count + 1
                f.write(str(count) + ' ' +  "{:.6f}".format(motor_x1_90) + ' ' +  "{:.6f}".format(motor_y1_90) + ' ' + str(z_factor) + ' 90.000000' + ' ' + '1' + ' ' + str(stage_rot) + '\n')
                if motor_x1_90 == motor_x2_90:
                    for i in range(y_steps*((abs(motor_y2_90-motor_y1_90)))):
                        count = count + 1
                        f.write(str(count) + ' ' +  "{:.6f}".format(motor_x2_90) + ' ' +  "{:.6f}".format(motor_y1_90-(i+1)*(motor_y1_90-motor_y2_90)/(y_steps*((abs(motor_y2_90-motor_y1_90))))) + ' ' + str(z_factor) + ' 90.000000' + ' ' + '1' + ' ' + str(stage_rot) + '\n')
                else:
                    for i in range(x_steps*((abs(motor_x2_90-motor_x1_90)))):
                        count = count + 1
                        f.write(str(count) + ' ' +  "{:.6f}".format(motor_x1_90-(i+1)*(motor_x1_90-motor_x2_90)/(x_steps*((abs(motor_x2_90-motor_x1_90))))) + ' ' +  "{:.6f}".format(motor_y2_90) + ' ' + str(z_factor) + ' 90.000000' + ' ' + '1' + ' ' + str(stage_rot) + '\n')
                
                count = count + 1
                f.write(str(count) + ' ' +  "{:.6f}".format(np.average([x_min,x_max])) + ' ' +  "{:.6f}".format(np.average([y_min,y_max])) + ' ' + str(z_factor) + ' 90.000000 0' + ' ' + str(stage_rot) + '\n')
                count = count + 1
                f.write(str(count) + ' ' +  "{:.6f}".format(np.average([x_min,x_max])) + ' ' +  "{:.6f}".format(np.average([y_min,y_max])) + ' ' + str(z_factor) + ' ' + '180.000000 0' + ' ' + str(stage_rot) + '\n')
                
                count = count + 1
                f.write(str(count) + ' ' +  "{:.6f}".format(motor_x1_180) + ' ' +  "{:.6f}".format(motor_y1_180) + ' ' + str(z_factor) + ' ' + '180.000000' + ' ' + '1' + ' ' + str(stage_rot) + '\n')
                if motor_x1_180 == motor_x2_180:
                    for i in range(y_steps*((abs(motor_y2_180-motor_y1_180)))):
                        count = count + 1
                        f.write(str(count) + ' ' +  "{:.6f}".format(motor_x2_180) + ' ' +  "{:.6f}".format(motor_y1_180-(i+1)*(motor_y1_180-motor_y2_180)/(y_steps*((abs(motor_y2_180-motor_y1_180))))) + ' ' + str(z_factor) + ' ' + '180.000000' + ' ' + '1' + ' ' + str(stage_rot) + '\n')
                else:
                    for i in range(x_steps*((abs(motor_x2_180-motor_x1_180)))):
                        count = count + 1
                        f.write(str(count) + ' ' +  "{:.6f}".format(motor_x1_180-(i+1)*(motor_x1_180-motor_x2_180)/(x_steps*((abs(motor_x2_180-motor_x1_180))))) + ' ' +  "{:.6f}".format(motor_y2_180) + ' ' + str(z_factor) + ' ' + '180.000000' + ' ' + '1' + ' ' + str(stage_rot) + '\n')
                
                count = count + 1
                f.write(str(count) + ' ' +  "{:.6f}".format(np.average([x_min,x_max])) + ' ' +  "{:.6f}".format(np.average([y_min,y_max])) + ' ' + str(z_factor) + ' ' + '180.000000 0' + ' ' + str(stage_rot) + '\n')
                count = count + 1
                f.write(str(count) + ' ' +  "{:.6f}".format(np.average([x_min,x_max])) + ' ' +  "{:.6f}".format(np.average([y_min,y_max])) + ' ' + str(z_factor) + ' 270.000000 0' + ' ' + str(stage_rot) + '\n')            
                
                count = count + 1
                f.write(str(count) + ' ' +  "{:.6f}".format(motor_x1_270) + ' ' +  "{:.6f}".format(motor_y1_270) + ' ' + str(z_factor*j) + ' 270.000000' + ' ' + '1' + ' ' + str(stage_rot) + '\n')
                if motor_x1_270 == motor_x2_270:
                    for i in range(y_steps*((abs(motor_y2_270-motor_y1_270)))):
                        count = count + 1
                        f.write(str(count) + ' ' +  "{:.6f}".format(motor_x2_270) + ' ' +  "{:.6f}".format(motor_y1_270-(i+1)*(motor_y1_270-motor_y2_270)/(y_steps*((abs(motor_y2_270-motor_y1_270))))) + ' ' + str(z_factor) + ' 270.000000' + ' ' + '1' + ' ' + str(stage_rot) + '\n')
                else:
                    for i in range(x_steps*((abs(motor_x2_270-motor_x1_270)))):
                        count = count + 1
                        f.write(str(count) + ' ' +  "{:.6f}".format(motor_x1_270-(i+1)*(motor_x1_270-motor_x2_270)/(x_steps*((abs(motor_x2_270-motor_x1_270))))) + ' ' +  "{:.6f}".format(motor_y2_270) + ' ' + str(z_factor) + ' 270.000000' + ' ' + '1' + ' ' + str(stage_rot) + '\n')
                
                count = count + 1
                f.write(str(count) + ' ' +  "{:.6f}".format(np.average([x_min,x_max])) + ' ' +  "{:.6f}".format(np.average([y_min,y_max])) + ' ' + str(z_factor) + ' 270.000000 0' + ' ' + str(stage_rot) + '\n')
                count = count + 1
                f.write(str(count) + ' ' +  "{:.6f}".format(np.average([x_min,x_max])) + ' ' +  "{:.6f}".format(np.average([y_min,y_max])) + ' ' + str(z_factor) + ' 0.000000 0' + ' ' + str(stage_rot) + '\n')
            g.write('1 ' + str(count) + '\n' + '2 ' + str(count))
                

if __name__ == '__main__':
    main()