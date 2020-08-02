import scipy.signal as signal
from scipy.io.wavfile import read, write
import numpy as np
from Models.StepConversion import StepConversion
from Models.RagaDetect import RagaDetect
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from logmmse import logmmse
import threading
import time
import sounddevice as sd
from os import path
dir_path = path.dirname(path.realpath(__file__))
filePath = dir_path + r"\temp_file.wav"
np.seterr(all='warn', divide = 'raise')

xsignal = None
fsampling = 44100
steps = dict()
steps[1] = list()
steps[2] = list()
steps[3] = list()

def RemoveSingleElement(l):
    if len(l)<=1:
        return []
    tempItem = l[0]
    count = 0
    indexes = list()
    for i in range(1, len(l)):
        if l[i] == tempItem:
            count += 1
        else:
            if count < 1:
                indexes.append(i-1)
            tempItem = l[i]
            count = 0
                
    if count == 0:
        indexes.append(i)
    x = 0
    for i in indexes:
        del l[i-x]
        x += 1
    return l

class RecordThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        while True:
            global xsignal
            global fsampling
            fs = fsampling  # Sample rate
            seconds = 6  # Duration of recording
            rec = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype=np.int16)
            sd.wait()  # Wait until recording is finished
            xsignal = np.array(rec, dtype=np.int16)
            xsignal.shape = (1, len(xsignal))
            xsignal = xsignal[0]
        
class ComputeThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        while True:
            global fsampling
            global xsignal
            fs = fsampling
            compute_signal = logmmse(xsignal, fs)
            key = "E"
            
            #BEGIN
            #   RETRIVE_STEPS_FROM_WAV_FILE
            nperseg = 2**14
            noverlap = 2**12
            f, t, Sxx = signal.spectrogram(compute_signal, fs, nperseg=nperseg,noverlap=noverlap, return_onesided=True)
            compute_filter = (f>55) & (f<1760)
            f = f[compute_filter]
            Sxx = Sxx[compute_filter, ...]
            limit = 10.0*np.log10((np.std(Sxx, dtype=np.float64) + np.mean(Sxx, dtype=np.float64))/2) + 3
            print(limit)
            if limit < 40:
                if len(steps[3]) > 0:
                    notes = list(set(steps[3]))
                    print(notes)
                    [raga, real, deviation] = RagaDetect.getRagaBySteps(sorted(notes))
                    print(raga["Name"], " - ", raga["Carnatic Notes"])
            else:
                for i in range(len(Sxx)):
                    for j in range(len(Sxx[0])):
                        if Sxx[i][j] != 0:
                            Sxx[i][j] = 10.0*np.log10(Sxx[i][j])
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
                if len(keys) > 0:
                    temp = steps[1]
                    steps[1] = steps[2]
                    steps[2] = steps[3]
                    steps[3], _ = StepConversion.getStepConversion(list(freqs.keys()),key)
                    steps[3] = RemoveSingleElement(steps[3])
                    notes1 = list(set(steps[3]))
                    results1 = list(RagaDetect.getRagaBySteps(sorted(notes1)))
                    
                    step = steps[1] + steps[2] + steps[3]
                    deleter = set()
                    for i in range(12):
                        if 0 < step.count(i) < 4:
                            deleter |= {i}
                    notes2 = list(set(steps[3]) - deleter)
                    results2 = list(RagaDetect.getRagaBySteps(sorted(notes2)))
                    #[raga, real, deviation2]
                    
                    if results2[1] == True:
                        print(notes2)
                        print(results2[0]["Name"], " - ", results2[0]["Carnatic Notes"])

                    elif results1[1] == True:
                        print(notes1)
                        print(results1[0]["Name"], " - ", results1[0]["Carnatic Notes"])
           
                    else:
                        if results2[2] < results1[2]:
                            print(notes2)
                            print(results2[0]["Name"], " - ", results2[0]["Carnatic Notes"])
                        
                        elif not set(steps[3]).issubset(steps[2]):    
                            print(notes1)
                            print(results1[0]["Name"], " - ", results1[0]["Carnatic Notes"])
                        else:
                            steps[3] = steps[2]
                            steps[2] = steps[1]
                            steps[1] = temp
            #END
            time.sleep(6)
            

rec_thread = RecordThread()
comp_thread = ComputeThread()

rec_thread.start()
time.sleep(7)
comp_thread.start()