import wave, array, math, time, argparse, sys
import numpy, pywt
from scipy import signal
import pdb
import matplotlib.pyplot as plt
import pyaudio
import bpm_detector

SAMPLE_RATE = 44100
RECORD_DURATION = 10 # Seconds
CHUNKSIZE = 1050
NCHANNELS = 1
SAMPLES_PER_SECOND = SAMPLE_RATE/CHUNKSIZE
SAMPLE_DURATION = 5



# Setup stuff
p = pyaudio.PyAudio()
inStream = p.open(format=pyaudio.paInt16, channels=NCHANNELS, rate=SAMPLE_RATE, input=True, frames_per_buffer=CHUNKSIZE)

frames = [] # A python-list of chunks(numpy.ndarray)

print "Recording ", RECORD_DURATION, "seconds of audio"

# Start recording
for _ in range(0, int(SAMPLES_PER_SECOND * RECORD_DURATION)):
    if _ % (SAMPLES_PER_SECOND) == 0: print _ / (SAMPLES_PER_SECOND)
    data = inStream.read(CHUNKSIZE)
    frames.append(numpy.fromstring(data, dtype=numpy.int16))

numpydata = numpy.hstack(frames)


print "Recording finished, analysing"



def read_wav(data):

    #open file, get metadata for audio
    try:
        wf = data
    except IOError, e:
        print e
        return

    #nsamps = wf.getnframes();
    nsamps = len(data)
    assert(nsamps > 0);

    #fs = wf.getframerate()
    fs = SAMPLE_RATE
    assert(fs > 0)

    # read entire file and make into an array
    #samps = list(array.array('i',wf.readframes(nsamps)))
    samps = data
    #print 'Read', nsamps,'samples from', filename
    try:
        assert(nsamps == len(samps))
    except AssertionError, e:
        print  nsamps, "not equal to", len(samps)
    
    return samps, SAMPLE_RATE

samps,fs = read_wav(numpydata)




data = []
correl=[]
bpm = 0
nsamps = len(samps)
window_samps = int(SAMPLE_DURATION*SAMPLE_RATE)
samps_ndx = 0;  #first sample in window_ndx 
max_window_ndx = nsamps / window_samps;
bpms = numpy.zeros(max_window_ndx)

#iterate through all windows
for window_ndx in xrange(1,max_window_ndx):

    #get a new set of samples
    data = samps[samps_ndx:samps_ndx+window_samps]
    if not ((len(data) % window_samps) == 0):
        raise AssertionError( str(len(data) ) ) 
    
    bpm, correl_temp = bpm_detector.bpm_detector(data,fs)
    #print bpm
    #assert False
    if bpm == []:
        continue
    bpms[window_ndx] = bpm
    correl = correl_temp
    
    #iterate at the end of the loop
    samps_ndx = samps_ndx+window_samps;

bpm = numpy.median(bpms)
print 'Completed.  Estimated Beats Per Minute:', bpm

n = range(0,len(correl))
plt.plot(n,correl); 
plt.show(True); #plot non-blocking
time.sleep(10);
plt.close();