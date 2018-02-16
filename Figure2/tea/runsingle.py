#! /usr/bin/env python

############################# BEGIN FRONTMATTER ################################ 
#                                                                              # 
#   TEA - calculates Thermochemical Equilibrium Abundances of chemical species #
#                                                                              #
#   TEA is part of the PhD dissertation work of Dr. Jasmina                    #
#   Blecic, who developed it with coding assistance from                       #
#   undergraduate M. Oliver Bowman and under the advice of                     #
#   Prof. Joseph Harrington at the University of Central Florida,              #
#   Orlando, Florida, USA.                                                     #
#                                                                              #
#   Copyright (C) 2014-2016 University of Central Florida                      #
#                                                                              #
#   This program is reproducible-research software: you can                    #
#   redistribute it and/or modify it under the terms of the                    #
#   Reproducible Research Software License as published by                     #
#   Prof. Joseph Harrington at the University of Central Florida,              #
#   either version 0.3 of the License, or (at your option) any later           #
#   version.                                                                   #
#                                                                              #
#   This program is distributed in the hope that it will be useful,            #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of             #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              #
#   Reproducible Research Software License for more details.                   #
#                                                                              #
#   You should have received a copy of the Reproducible Research               #
#   Software License along with this program.  If not, see                     #
#   <http://planets.ucf.edu/resources/reproducible/>.  The license's           #
#   preamble explains the situation, concepts, and reasons surrounding         #
#   reproducible research, and answers some common questions.                  #
#                                                                              #
#   This project was started with the support of the NASA Earth and            #
#   Space Science Fellowship Program, grant NNX12AL83H, held by                #
#   Jasmina Blecic, Principal Investigator Joseph Harrington, and the          #
#   NASA Science Mission Directorate Planetary Atmospheres Program,            #
#   grant NNX12AI69G.                                                          #
#                                                                              #
#   See the file ACKNOWLEDGING in the top-level TEA directory for              #
#   instructions on how to acknowledge TEA in publications.                    #
#                                                                              #
#   We welcome your feedback, but do not guarantee support.                    #
#   Many questions are answered in the TEA forums:                             #
#                                                                              #
#   https://physics.ucf.edu/mailman/listinfo/tea-user                          #
#   https://physics.ucf.edu/mailman/listinfo/tea-devel                         #
#                                                                              #
#   Visit our Github site:                                                     #
#                                                                              #
#   https://github.com/dzesmin/TEA/                                            #
#                                                                              #
#   Reach us directly at:                                                      #
#                                                                              #
#   Jasmina Blecic <jasmina@physics.ucf.edu>                                   #
#   Joseph Harrington <jh@physics.ucf.edu>                                     #
#                                                                              #
############################## END FRONTMATTER #################################

from readconf import *

# Setup for time/speed testing
if times:
    import time
    start = time.time()

import ntpath
import os
import shutil
import subprocess
import numpy as np
import sys

import makeheader as mh

# =============================================================================
# This program runs TEA over an input file that contains only one T-P.
# The code retrieves the input file and the current directory name given by the 
# user. It sets locations of all necessary modules and directories that 
# will be used. Then, it executes the modules in the following order:
# makeheader.py, balance,py, and iterate.py. The final results with the input
# and the configuration files are saved in the results/ directory. The config
# file, abundances file, and input file used for this run will be placed in
# inputs/ directory.
#
# This module prints on screen the code progress: the current T-P line from
# the pre-atm file, the current iteration number, and informs the user that
# minimization is done.
# Example:
#  100
# Maximum iteration reached, ending minimization.
#
# The program is executed with in-shell inputs:
# runsingle.py <SINGLETP_INPUT_FILE_PATH> <DIRECTORY_NAME>
# Example: ../TEA/tea/runsingle.py ../TEA/doc/examples/singleTP/inputs/singleTP_Example.txt Single_Example
# =============================================================================
    
# Time / speed testing
if times:
    end = time.time()
    elapsed = end - start
    print("runsingle.py imports:  " + str(elapsed))

# Print license
print("\n\
================= Thermal Equilibrium Abundances (TEA) =================\n\
A program to calculate species abundances under thermochemical equilibrium.\n\
\n\
Copyright (C) 2014-2016 University of Central Florida.\n\
\n\
This program is reproducible-research software.  See the Reproducible\n\
Research Software License that accompanies the code, or visit:\n\
http://planets.ucf.edu/resources/reproducible\n\
Questions? Feedback? Search our mailing list archives or post a comment:\n\
https://physics.ucf.edu/mailman/listinfo/tea-user\n\
\n\
Direct contact: \n\
Jasmina Blecic <jasmina@physics.ucf.edu>        \n\
========================================================================\n")

# Correct location_TEA name
if location_TEA[-1] != '/':
    location_TEA += '/'

if location_out[-1] != '/':
    location_out += '/'

# Retrieve user inputs file
infile  = sys.argv[1:][0]

# If input file does not exist break
try:
    f = open(infile)
except:
    raise IOError ("\n\nSingle T-P input file does not exist.\n")

# Retrieve current output directory name given by user 
desc    = sys.argv[1:][1]

# Check if output directory exists and inform user
if os.path.exists(location_out + desc):
    raw_input("  Output directory " + str(location_out + desc) + "/ already exists.\n"
              "  Press enter to continue and overwrite existing files,\n"
              "  or quit and choose another output name.\n")

# Set up locations of necessary scripts and directories of files
inputs_dir     = location_out + desc + "/inputs/"
thermo_dir     = location_TEA + "lib/gdata"
loc_balance    = location_TEA + "tea/balance.py"
loc_iterate    = location_TEA + "tea/iterate.py"
loc_headerfile = location_out + desc + "/headers/" + "header_" + desc + ".txt"
loc_outputs    = location_out + desc + "/outputs/"
loc_transient  = location_out + desc + "/outputs/" + "transient/"

# Create inputs directory
if not os.path.exists(inputs_dir): os.makedirs(inputs_dir)

# Check if config file exists in current working directory
TEA_config = 'TEA.cfg'
try:
    f = open(TEA_config)
except IOError:
    print("\nConfig file is missing. Place TEA.cfg in the working directory.\n")

# Inform user if TEA.cfg file already exists in inputs/ directory
if os.path.isfile(inputs_dir + TEA_config):
    print("  " + str(TEA_config) + " overwritten in inputs/ directory.")
# Copy TEA.cfg file to current inputs directory
shutil.copy2(TEA_config, inputs_dir + TEA_config)

# Inform user if abundances file already exists in inputs/ directory
head, abun_filename = ntpath.split(abun_file)
if os.path.isfile(inputs_dir + abun_filename):
    print("  " + str(abun_filename) + " overwritten in inputs/ directory.")
# Copy abundances file to inputs/ directory
shutil.copy2(abun_file, inputs_dir + abun_filename)

# Inform user if single T-P input file already exists in inputs/ directory
if os.path.isfile(inputs_dir + infile.split("/")[-1]):
    print("  " + str(infile.split("/")[-1]) + " overwritten in inputs/ directory.\n")
# Copy single T-P input file to inputs directory
shutil.copy2(infile, inputs_dir + infile.split("/")[-1])

# Times / speed check for pre-loop runtime
if times:
    new = time.time()
    elapsed = new - end
    print("pre-loop:           " + str(elapsed))

# Detect operating system for sub-process support
if os.name == 'nt': inshell = True    # Windows
else:               inshell = False   # OSx / Linux

# Execute main TEA loop
mh.make_singleheader(infile, desc, thermo_dir)
subprocess.call([loc_balance, loc_headerfile, desc, str(doprint)], shell=inshell)
subprocess.call([loc_iterate, loc_headerfile, desc, str(doprint)], shell=inshell)

# Save or delete headers file
if save_headers == False:
    shutil.rmtree(location_out + desc + "/headers/")

# Save or delete lagrange.py and lambdacorr.py outputs
if save_outputs:
    # Save directory for each T-P and its output files
    if not os.path.exists(loc_outputs): os.makedirs(loc_outputs)
    old_name = loc_transient
    new_name = loc_outputs + desc + "_singleTP_output" + loc_outputs[-1::]
    if os.path.exists(new_name):
        for file in os.listdir(new_name):
            os.remove(new_name + file)
        shutil.rmtree(new_name)
    os.rename(old_name, new_name)
else:
    shutil.rmtree(loc_outputs)

# Print on-screen
print("\n  Species abundances calculated.\n  Created results file.")

# Time / speed testing
if times:
    end = time.time()
    elapsed = end - start
    print("Overall run time:   " + str(elapsed) + " seconds")

