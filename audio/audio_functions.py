from multiprocessing import Process, Queue # Used for multiprocessing
import pygame
import time

import pyaudio      # Connects with Portaudio for audio device streaming
import wave         # Used to save audio to .wav files
import collections  # Used for Double ended Queue (deque) structure
from scipy import signal
import numpy
from pydub import AudioSegment

# variables
# ------------------------------------------------------------------------------------------

player = pygame.mixer

# just some variables used until the queues are working
Files = ["track1.ogg", "track2.ogg", "track3.ogg"]
fileNumber = 0
fileToPlay = Files[fileNumber]

isPlaying = False
isPaused = False


# playing functions
# ------------------------------------------------------------------------------------------
def init_player():
    if pygame.mixer.get_init() == None:
        pygame.mixer.init()

def play(fileToPlay):
    player.stop()                         # stops any track currently playing
    fileToPlay = retrieve_file_to_play()  #retrieve the file to play
    audio = player.Sound(fileToPlay)
    player.Sound.play(audio)
    isPlaying = True
    return(audio)

def pause():
    if player is not None:
        player.pause()
        isPaused = True
        
def resume():
    player.unpause()

def restart():
    play(fileToPlay)


# this isn't working yet - needs to get() next item from queue
def skip():
    nextTrack(fileNumber)
    play(fileToPlay)

def nextTrack(fileNumber):
    fileNumber += 1
    print(fileNumber)

def retrieve_file_to_play():
    return fileToPlay


# recording functions
# ----------------------------------------------------------------------------------------

def record_audio():
	
	# Define Audio characteristics
	FORMAT = pyaudio.paInt16
	CHANNELS = 1
	RATE = 48000
	CHUNK = 1024
	RECORD_SECONDS = 10
	
	# Audio Recording
	audio = pyaudio.PyAudio()
	
	# start Recording
	stream = audio.open(format=FORMAT, channels=CHANNELS,rate=RATE, input=True,frames_per_buffer=CHUNK)
	print ('recording...')
	
	data = stream.read(int(RATE/CHUNK) * CHUNK * RECORD_SECONDS)
	print ('finished recording')
	
	# stop Recording
	stream.stop_stream()
	stream.close()
	audio.terminate()
	
	# Exporting / SciPy resampling
	recording = AudioSegment(data, sample_width=2, frame_rate=RATE, channels=1)
	recording_samples = recording.get_array_of_samples()
	recording_resample = signal.resample(recording_samples, 8000)
	resamples = b''
	
	for i in range(0, len(recording_resample)):
		resamples += (int(recording_resample[i].astype(numpy.int16)).to_bytes(8, byteorder='big', signed=True))
	print(resamples)
	
	newrecording = AudioSegment(resamples, sample_width=2, frame_rate=8000, channels=1)
	newrecording.export("message.ogg", format = "ogg")
	
	print('Done export')

