from constants import *
import pygame, sys, string, csv, time
from pygame.locals import *
from random import randint
from pygaze import libtime
from pygaze.libscreen import Display, Screen
from pygaze.libinput import Keyboard
from pygaze.eyetracker import EyeTracker
#from random import uniform

'''
PRIMARY GLOBAL VALUES ARE IN THE CONSTANTS.PY FILE.
TO MODIFY STAIRCASING, SCREEN SIZE, FPS, COLOURS, GO THERE.
'''

# create keyboard object
keyboard = Keyboard()
# display object
disp = Display()
# create eyelink object
eyetracker = EyeTracker(disp)
# eyelink calibration
#eyetracker.calibrate()

screen = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT)) #SUBJ NUM ENTRY CALL
pygame.display.set_caption('Shield')
#pygame.display.toggle_fullscreen

#Setting up lists for log files:
L1 = ["Subject#"]
L2 = ["Block"]
L3 = ["Trial#"]
L4 = ["Score"]
L5 = ["Speed"]
L6 = ["Hit"]
L7 = ["Direction"]
R1 = ["Subject#"]
R2 = ["Block"]
R3 = ["PTDirection"]
R4 = ["Passage"]
R5 = ["ReadingTime"]
A1 = ["Block"]
A2 = ["Answer"]

#Draws the arena the game will be played in. 
def drawArena():
    DISPLAYSURF.fill(BLACK)
    #Draw outline of arena
    pygame.draw.rect(DISPLAYSURF, WHITE, ((0,0),(WINDOWWIDTH,WINDOWHEIGHT)), LINETHICKNESS*2-1)
    

#Draws the shield
def drawHole(hole):
    #Stops shield moving too low
    if hole.bottom > WINDOWHEIGHT - LINETHICKNESS:
        hole.bottom = WINDOWHEIGHT - LINETHICKNESS
    #Stops shield moving too high
    elif hole.top < LINETHICKNESS:
        hole.top = LINETHICKNESS
    #Draws shield
    pygame.draw.rect(DISPLAYSURF, OTHCOL, hole)


#draws the ball
def drawBall(ball):
    pygame.draw.ellipse(DISPLAYSURF, WHITE, ball)

#moves the ball returns new position
def moveBall(ball, randspeed, direction):
    if direction == 1:
        ball.x += (1 + randspeed)
    elif direction == 2:
        ball.x -= (1 + randspeed)
    return ball

#Checks to see if a point has been scored returns new score
def checkPointScored(hole1, ball, score, subnum, blocknum, trialnum, randspeed, gametimer, blockend, L1, L2, L3, L4, L5, L6, L7, sUP, sDN, bspd, direction):
    #Minus 1 point for ball hitting right wall (can't go below 0)
    #1 point for getting the ball in the hole
  if (direction == 1 and ball.right >=(WINDOWWIDTH - LINETHICKNESS)) or (direction == 2 and ball.left <= LINETHICKNESS):
    eyetracker.stop_recording()
    if (direction == 1 and hole1.left <= ball.right and hole1.top < ball.top and hole1.bottom > ball.bottom) or (direction == 2 and hole1.right >= ball.left and hole1.top < ball.top and hole1.bottom > ball.bottom):
        score += 1
        sUP +=1
        hit = 1
    elif (direction == 1 and ball.right >= (WINDOWWIDTH - LINETHICKNESS)) or (direction == 2 and ball.left <= LINETHICKNESS):
        score -= 1
        sDN += 1
        if score < 0:
            score = 0
        hit = 0
    if direction == 1:
        ball.x = LINETHICKNESS + 5
    if direction == 2:
        ball.x = (WINDOWWIDTH - LINETHICKNESS - 5)
    L1 += [subnum]
    L2 += [blocknum]
    L3 += [trialnum]
    L4 += [score]
    L5 += [randspeed]
    L6 += [hit]
    L7 += [direction]
    trialnum += 1
    #randspeed = randint(0,int(score/5))
    #above = randomized speed with max based on score
    #below = constant speed based on score
#    randspeed = int(score/5)
    if sUP >= UPTHRESH - randint(0,rthreshup):
        bspd +=1
        sUP = 0
        sDN = 0
    elif sDN == DNTHRESH:
        bspd -= 1
        sUP = 0
        sDN = 0
    randspeed = int(bspd)
    if randspeed < 0:
        randspeed=0
    ball.y = randint((LINETHICKNESS*3),(WINDOWHEIGHT - LINETHICKNESS*3))
    if time.clock()-gametimer >= GAMESESSDUR:
        blockend=1
    elif time.clock()-gametimer <> GAMESESSDUR:
        eyetracker.start_recording()
        eyetracker.status_msg("trial %d block %d" % (trialnum, blocknum))
        eyetracker.log("start game trial %d block %d" % (trialnum, blocknum))
    return score,randspeed,ball.x,ball.y,blocknum,trialnum,gametimer,blockend,sUP,sDN,bspd
  else: return score,randspeed,ball.x,ball.y,blocknum,trialnum,gametimer,blockend,sUP,sDN,bspd

#Displays the current score on the screen
def displayScore(score):
    resultSurf = BASICFONT.render('Score = %s' %(score), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH - 150, 25)
    DISPLAYSURF.blit(resultSurf, resultRect)

def displayTrialNum(trialnum):
    trialSurf = BASICFONT.render('Trial = %s' %(trialnum), True, WHITE)
    trialRect = trialSurf.get_rect()
    trialRect.topleft = (50, 25)
    DISPLAYSURF.blit(trialSurf, trialRect)

def displayBlockNum(blocknum):
    blockSurf = BASICFONT.render('Block = %s' %(blocknum), True, WHITE)
    blockRect = blockSurf.get_rect()
    blockRect.topleft = (250, 25)
    DISPLAYSURF.blit(blockSurf, blockRect)

#Writes log file when quit command is issued (keypress or end of experiment)
def quitwrite():
	eyetracker.close()
	csv_out = open("./Logs/" + str(subnum) + "ShieldGameLogRL.csv",'wb')
	mywriter = csv.writer(csv_out)
	for row in zip(L1, L2, L3, L4, L5, L6, L7):
		mywriter.writerow(row)
	csv_out.close()
	csv_out2 = open("./Logs/" + str(subnum) + "ShieldReadLogRL.csv",'wb')
	mywriter2 = csv.writer(csv_out2)
	for row in zip(R1, R2, R3, R4, R5):
		mywriter2.writerow(row)
	csv_out2.close()
	csv_out3 = open("./Logs/" + str(subnum) + "ShieldAnsLogRL.csv",'wb')
	mywriter3 = csv.writer(csv_out3)
	for row in zip(A1, A2):
		mywriter3.writerow(row)
	csv_out3.close()
	pygame.quit()
	sys.exit()

#updates logfile array for reading trials, called in next section (readbits)
def readlog(filename,t0,blocknum,R1,R2,R3,R4,R5):
	print time.clock() - t0, "seconds via time.clock (p1)"
	readtime=time.clock()-t0	
	R5 += [readtime]
	R1 += [subnum]
	R2 += [blocknum]
	if blocknum == 1:
		ptdir = 999
	elif blocknum <= BLOCKSTILSWITCH+1:
		ptdir = DIREC
	else:
		if DIREC == 1:
			ptdir = 2
		if DIREC == 2:
			ptdir = 1
	R3 += [ptdir]
	R4 += [filename]

def readbits(filename,t0,blocknum,R1,R2,R3,R4,R5,A1,A2):
  if filename == 'Instruc.png':
    blocknum+=1
    eyetracker.calibrate()
  img=pygame.image.load(filename)
  screen.blit(img,(0,0))
  pygame.display.flip()
  while filename != 70:
    for event in pygame.event.get():
      if event.type == QUIT:
        quitwrite()
      elif event.type == pygame.KEYDOWN:
#        for final version, consider having an "if filename isnumber<lastnumber), filename = filename+1"
#            else if filename = "lastnumber", filename = "lastscreen", etc.  Will likely save space for
#            the final product (reading passage screens, question screens).
#        filename, t0, t1 = readbits(filename, t0, t1)
        if filename == 'Instruc.png':
            global passage
            passage=1
            filename = "B" + str(blocknum) + "P" + str(passage) + ".png"
            img=pygame.image.load(filename)
            screen.blit(img,(0,0))
            t0=time.clock()
            print('key pressed, filename = %s' %(filename))
            # start eye tracking
            eyetracker.start_recording()
            eyetracker.status_msg("trial %s" % filename)
            eyetracker.log("start_image %s" % filename)
            pygame.display.flip()
            return filename,t0,blocknum
        elif filename[:1] == 'B':
            # stop eye tracking from previous reading trial
            eyetracker.stop_recording()
            readlog(filename,t0,blocknum,R1,R2,R3,R4,R5)
            passage += 1
            if passage == 4:
                filename = "Q" + str(blocknum) + ".png"
                print('key pressed, starting question(s)')
            else:
                filename = "B" + str(blocknum) + "P" + str(passage) + ".png"
                print('key pressed, filename = %s' %(filename))
            img=pygame.image.load(filename)
            screen.blit(img,(0,0))
            t0=time.clock()
            # start eye tracking
            eyetracker.start_recording()
            eyetracker.status_msg("trial %s" % filename)
            eyetracker.log("start_image %s" % filename)
            pygame.display.flip()
            return filename,t0,blocknum
        elif filename[:1] == "Q" and event.key == ord('1') or event.key == ord('2') or event.key == ord('3') or event.key == ord('4'):
            qans = event.key - 48 #1 = 49, 4 = 52
            A1 += [blocknum]
            A2 += [qans]
            filename='70'
#            img=pygame.image.load(filename)
#            screen.blit(img,(0,0))
#            t0=time.clock()
#            pygame.display.flip()
            print('%s key pressed, end reading portion' %(qans))
            return filename,t0,blocknum
        else: return filename,t0,blocknum
    if filename=='70':
      return filename,t0,blocknum

#######ATTEMPT TO HAVE A COUNTDOWN BEFORE START OF FIRST TRIAL#######
def gameStartCountdown(starttimer, tcountdown, blockend, blocknum, filename):
	if tcountdown == 70:
#		print 'Setting tcountdown to current time plus 6 seconds.'
		tcountdown = time.clock()+6
	elif starttimer > 0:
#		print 'starttimer is %s' %(starttimer)
		starttimer = int(tcountdown-time.clock())
#		print 'tcountdown is %s' %(tcountdown)
#		print 'new starttimer is %s' %(starttimer)
		startSurf = BASICFONT.render('%s' %(starttimer), True, WHITE)
		startRect = startSurf.get_rect()
		startRect.center = (WINDOWWIDTH/2,WINDOWHEIGHT/2)
		DISPLAYSURF.blit(startSurf, startRect)
		pygame.display.update()
		return starttimer,tcountdown,blockend,blocknum,filename
	elif starttimer <= 0:
#		print 'starttime less than or equal to zero'
		starttimer = 5
		tcountdown = 70
		blockend = 0
		gametimer = time.clock()
#		blocknum += 1
		filename="Instruc.png"
		gamebits(gametimer,blockend,blocknum,filename)
		return starttimer,tcountdown,blockend,blocknum,filename
	else:
		blockend=0
		tcountdown=70
		starttimer = 5		
		return starttimer,tcountdown,blockend,blocknum,filename
	return starttimer,tcountdown,blockend,blocknum,filename

#Main function
def gamebits(gametimer,blockend,blocknum,filename):
    direction = DIREC
    if blocknum > BLOCKSTILSWITCH:
        if DIREC == 1:
            direction = 2
        if DIREC == 2:
            direction = 1
    #Initiate variable and set starting positions
    #any future changes made within rectangles
#    ballX = 400
    if direction == 1:
        ballX = LINETHICKNESS + 5
    if direction == 2:
        ballX = (WINDOWWIDTH - LINETHICKNESS - 5)
    ballY = randint((LINETHICKNESS*3),(WINDOWHEIGHT - LINETHICKNESS*3))#WINDOWHEIGHT/2 - LINETHICKNESS/2
    playerOnePosition = (WINDOWHEIGHT - HOLESIZE) /2
#need to set initial vars score and randspeed
    score = 0
    randspeed = STARTSPEED 
    sUP = 0
    sDN = 0
    bspd = STARTSPEED
#For all blocks after the initial, the following will carry over score and
#ball speed by setting the vars to the last recorded value in their respective
#log lists (X[-1] = last entry in list X).
    if blocknum > 1:
        score = L4[-1]
        randspeed = L5[-1]
        bspd = L5[-1]
    trialnum = 1


    #Creates Rectangles for ball and paddles.
    if direction == 1:
        hole1 = pygame.Rect((WINDOWWIDTH - LINETHICKNESS), playerOnePosition, LINETHICKNESS,HOLESIZE)
    if direction == 2:
        hole1 = pygame.Rect(0, playerOnePosition, LINETHICKNESS,HOLESIZE)
    #Why is the left border 1 pixel wider than the right border?
    ball = pygame.Rect(ballX, ballY, LINETHICKNESS, LINETHICKNESS)
    pygame.mouse.set_pos(hole1.x, hole1.y) #stops annoying graphic "jump" of shield on first trial of any block if mouse was not at same height as hole.
    #Draws the starting position of the Arena
    drawArena()
    drawHole(hole1)
    drawBall(ball)

    pygame.mouse.set_visible(0) # make cursor invisible
    eyetracker.start_recording()
    eyetracker.status_msg("trial 1 start")
    eyetracker.log("start game trial 1, block %d" % blocknum)

#    while gametimer != 99999:
    while blockend == 0:
 #   while True:
 #     if time.clock()-gametimer < 60: #main game loop
        for event in pygame.event.get():
            if event.type == QUIT or gametimer == 0:
                quitwrite()
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    quitwrite()
            # mouse movement commands
            if event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                hole1.y = mousey
        if blockend == 1:
#            blocknum += 1
            filename="Instruc.png"
            return gametimer,blockend,blocknum,filename


        drawArena()
        drawHole(hole1)
        drawBall(ball)

        ball = moveBall(ball, randspeed, direction)
        score, randspeed, ball.x, ball.y, blocknum, trialnum, gametimer, blockend, sUP, sDN, bspd = checkPointScored(hole1, ball, score, subnum, blocknum, trialnum, randspeed, gametimer, blockend, L1, L2, L3, L4, L5, L6, L7, sUP, sDN, bspd, direction)
#        randspeed, ball.x, ball.y, blocknum, trialnum, gametimer, blockend = checkHitWall(ball, score, randspeed, blocknum, trialnum, gametimer, blockend)

        displayScore(score)
        displayTrialNum(trialnum)
        displayBlockNum(blocknum)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def main():
    pygame.init()
    pygame.mouse.set_visible(0) # make cursor invisible
    pygame.display.set_caption('Shield')
    blocknum=0

    t0=0
    filename = 'Instruc.png'
    global direction
    global DISPLAYSURF
    ##Font information
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE = 20
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    global FPSCLOCK
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT), pygame.FULLSCREEN)
    starttimer = 5
    global tcountdown
    tcountdown = 70
    blockend = 0
    drawArena()

    while True: #main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                quitwrite()
#            elif event.type == pygame.KEYDOWN:
#                filename, t0, t1 = readbits(filename, t0, t1)

        if blocknum > BLOCKSTILQUIT and filename == '70':
            quitwrite()
        if filename != '70':
            filename,t0,blocknum = readbits(filename, t0, blocknum, R1, R2, R3, R4, R5, A1, A2)
        elif filename == '70':
            drawArena()
            starttimer, tcountdown, blockend, blocknum, filename= gameStartCountdown(starttimer, tcountdown, blockend, blocknum, filename)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()
