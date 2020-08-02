import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
from scipy.io.wavfile import read, write

fs, mysignal = read(r"C:\Chyavan\Raga-Detection\Project\Recording.wav")
print(mysignal.dtype)
print(mysignal.max(), mysignal.min(), list(mysignal).count(0))

plt.figure(1)
plt.title("Recording")
plt.plot(mysignal)
plt.show()

fs, mysignal = read(r"C:\Chyavan\Raga-Detection\Project\temp_file.wav")
print(mysignal.dtype)
print(mysignal.max(), mysignal.min(), list(mysignal).count(0))

plt.figure(1)
plt.title("Live")
plt.plot(mysignal)
plt.show()