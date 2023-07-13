# LJX Python Strain Acquisition Project

## Functional python script that communicates with a Keyence LJ-X8000A controller to acquire stress and strain data of sample using a Keyence profiling laser.

This project was developed to determine if strain could be measured using a profiling laser. This script generates stress and strain data and graphs based on user input force data, cross-sectional area of the specimen being strained and the data acquired from the profiling laser. 

For this project, a Keyence profiling laser and controller were used to collect data. Since all first party software compatible with the LJ-X8000A controller (LJ-X Navigator and LJ-X Observer) are only compatible with Windows operating systems, the LJXAwrap wrapper files must be acquired from Keyence. These files allow compatibility with both Windows and Linux operating systems and contain all the necessary functions required to communicate with the LJ-X8000A controller. Please note this script is not usable without the functions from the wrapper script and associated files. Reaching out to Keyence is required to properly obtain the wrapper files.

# More information relevant to this project:
* This script uses the Python modules: LJXAwrap, ctypes, sys, time, numpy, matplotlib, and PySimpleGUI (install with pip and requires Python 3.4+)
* The script was written with Python 3.9.
* A Keyence LJ-X8080 profiling laser was used with this script.
* This script is only compatible with a LJ-X8000A controller.
* To communicate with another controller, different wrapper files may need to be obtained and this script may need to be altered.

# User Instructions
The program (ROUSSEAU_StrainAcquisition.py) is located in the "PYTHON" folder. To execute this script and acquire strain data run the script using a compiler, or type the following when in the PYTHON directory.

```

$ python3 ROUSSEAU_StrainAcquisition.py

```

After the communication is established, the user will be prompted to input force data. Please note a strain measurement will only be taken each time the user inputs a force value. 

insert image here

If only 
