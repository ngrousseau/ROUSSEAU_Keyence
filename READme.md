# Developing Laser Profiling Methodology at CHESS (SUNRiSE/Fort Lewis College)

#### Undergraduate summer research project with the purpose of developing a working methodology to use a Keyence LJ-X8080 profiling laser to achieve real time strain measurements and generate 3D data structures of parts.

This project is part of an undergraduate summer research program with Cornell High Energy Synchrotron Source (CHESS). This project seeks to develop a methodology for remote measuring and modeling of parts and materials using a Keyence LJ-X8080 profiling laser. This will be achieved by taking advantage of the profiling lasers ability to take highly accurate displacement data. With this laser, parts or materials with complex morpholgies will be more accessible to dimensioning.

Additionally, a side project has been included to use the profiling laser to measure real time strain. The script written for this side project generates a stress strain curve based on user-input force data and data collected by the profiling laser. More information can be found in the Strain folder located in the PYTHON directory.

## Approach
The first step to achieving the goals of this project were to understand how to use the hardware and existing software. The LJ-X8080 profiling laser was controlled using an LJ-X8000A controller and two Keyence softwares; LJ-X Navigator and LJ-X Observer. However, the first-party Keyence softwares are only compatible with the Windows operating system and much of CHESS operates on Linux. 

A library of communication files and an LJXAwrap.py script file were acquired from Keyence to achieve communication with the profiling laser and controller. Please note the LJXAwrap script and communication library must be aqcuired from Keyence only, via the License Agreement and cannot be found here. The scripts written in this prject are not usable without the library and LJXAwrap script. Once these are properly acquired, the scripts for this project can be placed in the PYTHON folder of the communication library and be properly used.

## Relevant Information
* A Keyence LJ-X8080 profiling laser was used for this project.
* The python scripts were written to be compatible with an LJ-X8000A controller.
* The scripts were written with Python 3.9 and compiled with Spyder.
* Python modules used in these scripts include numpy, math, ctypes, sys, time, matplotlib, pandas, mpl_toolkits.mplot3d, and PySimpleGUI (install with pip and required Python 3.4+).

## User Instructions
This repository contains 3 folders which are the License folder, containing the Keyence License agreement, the images folder, which contains relevant images included in READme files and the PYTHON folder, where all the scripts and associated READme files are located.

## License Agreement
Please review the software license agreeement at the end of the README.pdf file located in the License folder of the main branch.
