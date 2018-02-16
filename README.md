# RRC-Tsai-2017-ApJS-VULCAN
TEA compendium for Tsai et al. (2017), "VULCAN: An Open-source, Validated Chemical Kinetics Python Code for Exoplanetary Atmospheres" 


This is the compendium of using the thermochemical equilibrium code, TEA ([Blecic et al. (2015)](https://arxiv.org/abs/1505.06392)) to benchmark the chemical kinetics results in Tsai et al.2017,
as shown in Figure 2. 

The "run" directory contains two folders "T800" and "T2500" for the two isothermal atmospheres at 800 K and 2500 K.
The temperature and pressure input files are in the "input" folders.

To produce the outputs for comparison, run TEA with the corresponding atm files, and then run VULCAN at the same isothermal atmospheres with no eddy diffusion.
The output files have been prerun and stored in the "results" folders in "T800" and "T2500".  

The script plotTEA_vulcan is added to reproduce Figure 2. To read the outputs and make the plot, run ../tea/plotTEA_vulcan.py <names of species seperated by ",">
For example, under the /run directory in TEA, run the following:

../tea/plotTEA_vulcan.py H2O,CO,CO2,CH3,CH4,C2H2,H,OH,HCO,H2CO


More deteails about using TEA can be found on https://github.com/dzesmin/TEA
 