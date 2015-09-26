import pyaudio, numpy

RATE = 44100
RECORD_DURATION = 5 # Seconds
CHUNKSIZE = 1050
NCHANNELS = 1
SAMPLES_PER_SECOND = RATE/CHUNKSIZE

# Setup stuff
p = pyaudio.PyAudio()
inStream = p.open(format=pyaudio.paInt16, channels=NCHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNKSIZE)

frames = [] # A python-list of chunks(numpy.ndarray)

print "Recording ", RECORD_DURATION, "seconds of audio"

# Start recording
for _ in range(0, int(SAMPLES_PER_SECOND * RECORD_DURATION)):
    if _ % (SAMPLES_PER_SECOND) == 0: print _ / (SAMPLES_PER_SECOND)
    data = inStream.read(CHUNKSIZE)
    frames.append(numpy.fromstring(data, dtype=numpy.int16))

numpydata = numpy.hstack(frames)


print "Recording finished, playing back.."



outStream = p.open(format = pyaudio.paInt16,  
                channels = NCHANNELS,  
                rate = RATE,
                output = True)  
outStream.write(numpydata)

'''
# Play back recording
x = 8 # seconds
#paly stream  
while x > 0:
    outStream.write(data)  
    data = f.readframes(chunk)  
    x -= 1
'''


for stream in (outStream, inStream):
	stream.stop_stream()
	stream.close()
p.terminate()