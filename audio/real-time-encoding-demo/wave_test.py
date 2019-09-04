import pyaudio      # Connects with Portaudio for audio device streaming
import wave         # Used to save audio to .wav files
import collections  # Used for Double ended Queue (deque) structure
import numpy

from scipy import signal
from pydub import AudioSegment

#import msvcrt       # Used for non-blocking keyboard event
#import librosa


# Define Audio characteristics
# ----------------------------
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
CHUNK = 1024
RECORD_SECONDS = 2

# have some function for pulling long/lat
#longLat = { 0, 0}
#UserID = 12345


# Audio Recording
# ----------------------------
audio = pyaudio.PyAudio()
 
# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,rate=RATE, input=True,frames_per_buffer=CHUNK)
print ('recording...')

data = stream.read(int(RATE/CHUNK) * CHUNK * RECORD_SECONDS)

# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()
print ('finished recording')
 
 
# Exporting / resampling
# ----------------------------

# we can add some metadata to the recording
# recording.export("raw.mp3", format="mp3", tags={'LongLat': longLat, 'User': 12345, 'Priority': 'High!'})

# Pydub addition - will export raw audio - data - into specified formats.
recording = AudioSegment(data, sample_width=2, frame_rate=RATE, channels=1)
recording.export("raw.wave", format="wav")     # Raw audio at 161KB per 10 seconds
recording.export("raw.flac", format = "flac")  # ~50% reduction in file size; 91KB per 10 seconds
recording.export("raw.mp3", format = "mp3")
recording.export("raw.ogg", format = "ogg")
recording_samples = recording.get_array_of_samples()
recording_resample = signal.resample(recording_samples, 8000)

# SciPy Resampling
resamples = b''
for i in range(0, len(recording_resample)):
    resamples += (int(recording_resample[i].astype(numpy.int16)/32).to_bytes(4, byteorder='big', signed=True))
#print(resamples)

newrecording = AudioSegment(resamples, sample_width=2, frame_rate=8000, channels=1)
newrecording.export("resample.wav", format="wav")     # Raw audio at 161KB per 10 seconds
newrecording.export("resample.flac", format = "flac")  # ~50% reduction in file size; 91KB per 10 seconds
newrecording.export("resample.mp3", format = "mp3")
newrecording.export("resample.ogg", format = "ogg")
#newrecording.export(AAC_OUTPUT_FILENAME, format = "aac")   # Currently produces an error - unresolved github issue

# Desktop conversion results in 53KB; ~70% reduction
# C:\ > ffmpeg -i file.wav -codec:a aac file.aac 

print('Done export')

# ----------------------------------------------------------------------------------------
