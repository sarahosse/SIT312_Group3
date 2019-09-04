import pygame

# list of files to play
Files = ["Message1.wav", "Message2.wav", "Message3.wav", "Message4.wav", "Message5.wav"]
# length of times - how to update this as files get updated?
FileTimes = [149, 213, 17, 53, 89]

fileToRetrieve = 0    # which file from queue to play
playTime = 0          # how long track has been playing for

# time left on track (to display on screen)
timeLeft = FileTimes[fileToRetrieve] - playTime

# initialise player
pygame.mixer.init()

# function for skipping to the next track
def nextTrack():
	fileToRetrieve++

# function for playing track
def playTrack():

	# play specified file from specific location
	pygame.mixer.music.load(Files[fileToRetrieve])

	# begin playing file
	pygame.mixer.music.play()
	print "Audio file playing"
	
	checkUserInput()

# continuously checks user input while audio file is playing
def checkUserInput():

	# returns true when stream is playing track (including while paused)
	while (pygame.mixer.music.get_busy() == True):
		
		# get playtime for display on screen
		playTime = pygame.mixer.music.get_pos()
		
		# pause playback
		if (paused = True):
			pygame.mixer.music.pause()
			
		# resume playing
		if (resume == True):
			pygame.mixer.music.unpause()
		
		# skip to next track
		if (skip == True):
			nextTrack()
			# this stops currently playing stream and loads next one
			pygame.mixer.music.load(Files[fileToRetrieve])
		
		# restart track
		if (restart == True):
			# restarts the track already playing
			pygame.mixer.music.play()

	print "Audio file finished"
