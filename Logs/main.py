import scipy.signal as signal
from scipy.io.wavfile import read, write
import numpy as np
from Models.StepConversion import StepConversion
from Models.RagaDetect import RagaDetect
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from logmmse import logmmse_from_file
import threading
import time
import sounddevice as sd

#Adarsh - Inputs audio from temporary wav file
fs, _ = read(r"C:\Users\1000272222\Downloads\Recording (1).wav")
mysignal = logmmse_from_file(r'C:\Users\1000272222\Downloads\Recording (1).wav')

#Ajinkya - inputs key from user's selection in the UI
key = "C"


#BEGIN
#   RETRIVE_STEPS_FROM_WAV_FILE
nperseg = 2**14
noverlap = 2**13
f, t, Sxx = signal.spectrogram(mysignal, fs, nperseg=nperseg,noverlap=noverlap)
myfilter = (f>55) & (f<1760)
f = f[myfilter]
Sxx = Sxx[myfilter, ...]
limit = 10.0*np.log10((np.std(Sxx, dtype=np.float64)*np.mean(Sxx, dtype=np.float64))**0.5)

if limit < 20:
    #Code for nothing is playing
    print("nothing playing")
else:
    Sxx = 10.0*np.log10(Sxx)
    freqs = dict()
    for i in range(len(Sxx)):
        for j in range(len(Sxx[0])):
            Sxx[i][j] = Sxx[i][j] *int( Sxx[i][j] > limit )
            if (Sxx[i][j] > limit):
                if f[i] in freqs.keys():
                    freqs[f[i]] += 1
                else:
                    freqs[f[i]] = 1
    keys = list(freqs.keys())
    for i in keys:
        if freqs[i] < 2:
            del freqs[i]
    keys = list(freqs.keys())
    steps, _ = StepConversion.getStepConversion(list(freqs.keys()),key)
    print(steps)
#END


#BEGIN
#   RETRIVE_RAGA_FROM_STEPS
    raga = RagaDetect.getRagaBySteps(steps)
    print(raga["Name"], " - ",raga["Carnatic Notes"])
#END