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
DIREC = int(raw_input("Enter 1 to start with left to right, 2 for right to left: ")) #Sets starting direction for game trials.
STARTSPEED = int(raw_input("Enter starting speed: ")) #Sets pixels over 1 for ball to move per tick.  Should probably change to only allow number as input but meh.

# Number of frames per second
# Change this value to speed up or slow down your game
# See if can modify the update (when ball location actually changes) with
# another variable to get finer degrees of speed variation.  E.G. on tick,
# if tickcount >= speedmod, do_update.
FPS = 200

#Global Variables to be used through our program

WINDOWWIDTH = 800
WINDOWHEIGHT = 600
LINETHICKNESS = 10
HOLESIZE = 60 #size of shield, orig 50
GAMESESSDUR = 10 #duration of game block in seconds
BLOCKSTILQUIT = 4 #Number of blocks to run (reading task and game task)
BLOCKSTILSWITCH = 2 #Blocks to run before changing direction (set to same as BLOCKSTILQUIT for no direction switching)
#subnum = raw_input("Enter subject number: ")

# Set up the colours
BLACK     = (0  ,0  ,0  )
WHITE     = (255,255,255)
OTHCOL = (100,100,100)

#Staircase constants:
UPTHRESH = 2 #consecutive hits to increase ball speed.
rthreshup = 0 #max randomized alteration for UPTHRESH (0 = always UPTHRESH, 1 = UPTHRESH or UPTHRESH - 1)
DNTHRESH = 1 #consecutive misses to decrease ball speed.
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
