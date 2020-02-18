# SLM-P3HM
Code for P3HM Holography SLM lab


GS.py contains my implementation of the Gerchberg-Saxton algorithm.
It's all split up into separate functions e.g. a function for making the grid and a function to add a trap.
All functions are run below their definition to show proper usage.


SLMDisplay.py is the main program of this project.
This file contains all the contents of the GS.py file apart from the graphing at the end.
It contains 2 classes which define the two windows used for Display and Manipulation.
Define all the variables at the top of the file with your values dependent on your SLM. When writing this I used a ODE1024 from Cambridge Correlators.
Ideally you would have 2 monitors and 1 SLM. Have the SLM mirror the display of your first monitor. The display window opens in fullscreen.
Then you can move the secondary Manipulation window to your second screen and display and manipulate the location of your trap.
I have set each of the buttons to move the trap 10 pixels in the direction. This is purely because the setup I used was minimalistic
and larger changes needed to be made to see them without proper detectors. You can change how much the trap is moved by editing the
values in the Up/right/left/down functions from 10 to your desired positive integer.
