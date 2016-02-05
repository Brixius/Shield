# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 16:01:22 2016

@author: William
"""


# MAIN
DUMMYMODE = True # False for gaze contingent display, True for dummy mode (using mouse or joystick)
LOGFILENAME = raw_input("Enter subject number: ") # logfilename, without path
LOGFILE = LOGFILENAME[:] # .txt; adding path before logfilename is optional; logs responses (NOT eye movements, these are stored in an EDF file!)
subnum = LOGFILENAME #LFN is name for pygaze and tracker logs, subnum is for the custom exp code already written before adding ET stuff.
#TRIALS = 1

# DISPLAY
SCREENNR = 0 # number of the screen used for displaying experiment
DISPTYPE = 'pygame' # either 'psychopy' or 'pygame'
DISPSIZE = (800,600) # canvas size
MOUSEVISIBLE = False # mouse visibility
BGC = (125,125,125) # backgroundcolour
FGC = (0,0,0) # foregroundcolour
FONTSIZE = 32 # font size

# INPUT
KEYLIST = None # None for all keys; list of keynames for keys of choice (e.g. ['space','9',':'] for space, 9 and ; keys)
KEYTIMEOUT = 1 # None for no timeout, or a value in milliseconds

# EYETRACKER
# general
TRACKERTYPE = 'eyelink' # either 'smi', 'eyelink' or 'dummy' (NB: if DUMMYMODE is True, trackertype will be set to dummy automatically)
#SACCVELTHRESH = 35 # degrees per second, saccade velocity threshold
#SACCACCTHRESH = 9500 # degrees per second, saccade acceleration threshold

# STIMULUS
#STIMSIZE = 100 # stimulus size (pixels)
#STIMCOL = (255,255,0) # stimulus colour
#STIMPOS = (DISPSIZE[0]/2,DISPSIZE[1]/2) # start position
#STIMREFRESH = 2500 # ms; time before stimulus is set to new position

# GAME
