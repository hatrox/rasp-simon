#!/usr/bin/python

import RPi.GPIO as GPIO
import time
from random import randint

GPIO.setmode(GPIO.BOARD)

debug = True
startingSteps = 3
sleepTime = 1

# (switch, led)
switchLeds = [(7, 8), (11, 12), (15, 16), (21, 22)]
lives = len(switchLeds) # max number of lives. any custom value should be lower than that

for tuple in switchLeds:
	GPIO.setup(tuple[0], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(tuple[1], GPIO.OUT)

def generateRandomSteps(stepCount, steps):
	for i in range(0, stepCount):
		steps.append(randint(0, len(switchLeds) - 1))

	return steps

def playThroughSteps(steps):
	if debug:
		print "playing through steps..."

	for step in steps:
		if debug:
			print "index " + str(step)

		GPIO.output(switchLeds[step][1], True)
		time.sleep(sleepTime)
		GPIO.output(switchLeds[step][1], False)

def getUserInput():
	while True:
		for i in range(0, len(switchLeds)):
			if GPIO.input(switchLeds[i][0]):
				if debug:
					print "user inputted index " + str(i)

				return i

def wrongInput():
	if debug:
		print "detected wrong input!"

	for i in range(0, lives):
		GPIO.output(switchLeds[i][1], True)
	
	time.sleep(sleepTime / 2)

	for i in range(0, lives):
		GPIO.output(switchLeds[i][1], False)

def gameOver():
	if debug:
		print "GAME OVER"

	while True:
		for tuple in switchLeds:
			GPIO.output(tuple[1], True)

		time.sleep(sleepTime)
		
		for tuple in switchLeds:
			GPIO.output(tuple[1], True)
		
		time.sleep(sleepTime)

try:
	steps = generateRandomSteps(startingSteps, [])
	
	if debug:
		print steps

	while True:
		playThroughSteps(steps)

		#time.sleep(sleepTime)

		wrongInputFlag = False
		counter = 0
		for step in steps:
			userInputIndex = getUserInput()

			if userInputIndex == step:
				continue
			else:
				lives -= 1
				
				if lives == 0:
					gameOver()
					return # a rudimentary return, if you manage to escape the infinite loop ;)
				
				wrongInput()

				wrongInputFlag = True
				break
		
		if not wrongInput:
			generateRandomSteps(1, steps)
finally:
	GPIO.cleanup()
