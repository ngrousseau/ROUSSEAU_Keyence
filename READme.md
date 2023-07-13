# LJX Python Strain Acquisition Project

## Functional python script that communicates with a Keyence LJ-X8000A controller to acquire stress and strain data of sample using a Keyence profiling laser.

This project was developed to determine if strain could be measured using a profiling laser. Since the existing software compatible with the LJ-X8000A controller (LJ-X Navigator and LJ-X Observer) are only compatible with Windows operating systems, the LJXAwrap wrapper files must be acquired from Keyence. These files allow compatibility with both Windows and Linux operating systems and contain all the necessary functions required to communicate with the LJ-X8000A controller. Please note this script is not usable without the functions from the wrapper script and associated files.

# More information relevant to this project:
* This script uses the Python modules: LJXAwrap, ctypes, sys, time, numpy, matplotlib, and PySimpleGUI (install with pip and requires Python 3.4+)
* The script was written with Python 3.9.
* A Keyence LJ-X8080 profiling laser was used with this script.
