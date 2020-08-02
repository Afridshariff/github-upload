import scipy.signal as signal
from scipy.io.wavfile import read, write
import numpy as np
from Models.StepConversion import StepConversion
from Models.RagaDetect import RagaDetect
from logmmse import logmmse
import threading
import time
import sounddevice as sd
from tkinter import *
import numpy as np
from tkinter import *
from tkinter import ttk

key = str("C")
note_list = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
widgets = list()
widgets2 = list()
UiObj = Tk()
v = StringVar()
v2 = StringVar()
key2 = str("C")
RagaList = RagaDetect.getRagaList(1)
LearnRaga = RagaList[0]

tabControl = ttk.Notebook(UiObj) 
s = ttk.Style()
s.configure('new.TFrame', background='#2A3756')
tabDetect = ttk.Frame(tabControl, style='new.TFrame') 
tabCorrect = ttk.Frame(tabControl,style='new.TFrame') 
  
tabControl.add(tabDetect, text ='D e t e c t i o n') 
tabControl.add(tabCorrect, text ='C o r r e c t i o n')

def sel():
    global key
    global steps
    key = v.get()
    print(key)
    steps[1] = list()
    steps[2] = list()
    steps[3] = list()

def sel2():
    global key2
    global stepsLearn
    key2 = v2.get()
    print(key2)
    stepsLearn = list()

def _quit():
    global tabControl
    print(tabControl.index(tabControl.select()))
    UiObj.quit()
    UiObj.destroy()
    try:
        comp_thread.stop()
    except:
        pass
    try:
        rec_thread.stop()
    except:
        pass
    exit(0)

def getRagas():
    global RagaList
    global e
    global warning
    global dropDown
    global selectedRaga
    mela = 0
    try:
        mela = int(e.get())
        if mela < 1 or mela > 72:
            raise Exception("Invalid Melakartha number")
    except:
        warning.set("Input valid Melakartha (1 - 72)")
        return
    warning.set("")
    RagaList = RagaDetect.getRagaList(mela)
    menu = dropDown['menu']
    menu.delete(0, 'end')
    for name in set(i['Name'] for i in RagaList):
        menu.add_command(label=name, command=lambda name=name: selectedRaga.set(name))
        
def startLearn():
    global LearnRaga
    global RagaList
    global selectedRaga
    global warning2
    global raagaDisplay
    global raagaRecDisplay
    if selectedRaga.get() == "":
        warning2.set("Please select a Raga")
    else:
        warning2.set("")
    for i in RagaList:
        if i['Name'] == selectedRaga.get():
            LearnRaga = i
    raagaDisplay.set("  ".join(LearnRaga["Carnatic Notes"]))
    raagaRecDisplay.set("")
        
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

#BEGIN
##########################################################################################################################################
#   UI INITIALIZATIONS

xc=40
yc=15

keyText = StringVar()
keySelect = Label( tabDetect, textvariable=keyText, fg="#FFFFFF", bg="#2A3756", font=('Arial', 18, 'bold italic') )
keyText.set("SELECT KEY")
keySelect.place(x=150,y=yc,width=300,height=25 )
yc += 30
placer = len(note_list)
iterate = 0
for item in note_list:
    widgets.append(Radiobutton(tabDetect,bg="#2A3756", text = item, width=4, variable = v, value = item, fg="#FFFFFF",selectcolor="#0D0D0D",command=sel, font="Arial 15", activebackground="#1A2746", activeforeground="#FFFFFF"))
    widgets[iterate].place(x=xc,y=yc)
    xc += 90
    placer -= 1
    iterate += 1
    if placer < 7:
        xc = 40
        yc = 100
        placer = 12

raga = StringVar()
ragaName = Label( tabDetect, textvariable=raga, fg="#FFFFFF", bg="#2A3756", font=('Times', 20, 'bold') )
raga.set("\"Raga Name\"")
ragaName.place(x=150,y=165,width=300,height=35 )
notes = StringVar()
notesName = Label( tabDetect, textvariable=notes, fg="#FFFFFF", bg="#2A3756", font=('Times', 15, 'bold') )
notes.set("")
notesName.place(x=150,y=200,width=300,height=25 )
button = Button(master=tabDetect, text="E X I T", command=_quit, activebackground="#F26444", activeforeground = "#FFFFFF", bd = 0, bg = "#0D0D0D", fg="#FFFFFF")
button.place(x=550,y=0,width=50,height=25)


##########################################################################################################################
#CORRECTION
x2c=40
y2c=15

key2Text = StringVar()
key2Select = Label( tabCorrect, textvariable=key2Text, fg="#FFFFFF", bg="#2A3756", font=('Arial', 18, 'bold italic') )
key2Text.set("SELECT KEY")
key2Select.place(x=150,y=y2c,width=300,height=25 )
y2c += 30
placer = len(note_list)
iterate = 0
for item in note_list:
    widgets2.append(Radiobutton(tabCorrect,bg="#2A3756", text = item, width=4, variable = v2, value = item, fg="#FFFFFF",selectcolor="#0D0D0D",command=sel2, font="Arial 15", activebackground="#1A2746", activeforeground="#FFFFFF"))
    widgets2[iterate].place(x=x2c,y=y2c)
    x2c += 90
    placer -= 1
    iterate += 1
    if placer < 7:
        x2c = 40
        y2c = 100
        placer = 12
button2 = Button(master=tabCorrect, text="E X I T", command=_quit, activebackground="#F26444", activeforeground = "#FFFFFF", bd = 0, bg = "#0D0D0D", fg="#FFFFFF")
button2.place(x=550,y=0,width=50,height=25)

mela = StringVar()
melaName = Label( tabCorrect, textvariable=mela, fg="#FFFFFF", bg="#2A3756", font=('Arial', 15, 'bold') )
mela.set("Melakartha Number: ")
melaName.place(x=10,y=165,width=300,height=35 )
e = Entry(tabCorrect)
e.insert(END, '1')
e.place(x=300,y=155,width=100,height=35 )
warning = StringVar()
warnName = Label( tabCorrect, textvariable=warning, fg="#F26444", bg="#2A3756", font=('Arial', 12) )
warning.set("")     #("Input valid Melakartha Number")
warnName.place(x=40,y=195,width=250,height=35 )

buttonGet = Button(master=tabCorrect, text="Get Ragas", command=getRagas, activebackground="#1AA260", activeforeground = "#FFFFFF", bd = 0, bg = "#1A2746", fg="#FFFFFF")
buttonGet.place(x=420,y=155,width=100,height=35 )

raaga = StringVar()
raagaName = Label( tabCorrect, textvariable=raaga, fg="#FFFFFF", bg="#2A3756", font=('Arial', 15, 'bold') )
raaga.set("Raga: ")
raagaName.place(x=40,y=240,width=100,height=35 )

selectedRaga = StringVar()
selectedRaga.set("")
dropDown = OptionMenu(tabCorrect, selectedRaga, *set(i['Name'] for i in RagaList))
dropDown.config(fg="#FFFFFF", bg="#2A3756", activebackground='#5075CC', activeforeground='#0D0D0D')
dropDown["menu"].config(fg="#FFFFFF", bg="#2A3756", activebackground='#5075cc', activeforeground='#0D0D0D')
dropDown.place(x=300,y=240,width=100,height=35 )

warning2 = StringVar()
warn2Name = Label( tabCorrect, textvariable=warning2, fg="#F26444", bg="#2A3756", font=('Arial', 12) )
warning2.set("") #("Please select a Raga")
warn2Name.place(x=60,y=270,width=150,height=35 )

buttonLearn = Button(master=tabCorrect, text="Learn", command=startLearn, activebackground="#1AA260", activeforeground = "#FFFFFF", bd = 0, bg = "#1A2746", fg="#FFFFFF")
buttonLearn.place(x=420,y=240,width=100,height=35 )

arohan = StringVar()
arohanName = Label( tabCorrect, textvariable=arohan, fg="#FFFFFF", bg="#2A3756", font=('Arial', 15, 'bold') )
arohan.set("Swaras")
arohanName.place(x=50,y=330,width=500,height=35 )

raagaDisplay = StringVar()
raagaDisplayName = Label( tabCorrect, textvariable=raagaDisplay, fg="#1AA260", bg="#2A3756", font=('Arial', 20, 'bold') )
raagaDisplay.set("  ".join(LearnRaga["Carnatic Notes"]))
raagaDisplayName.place(x=50,y=365,width=500,height=35 )

recordedArohan = StringVar()
recordedArohanName = Label( tabCorrect, textvariable=recordedArohan, fg="#FFFFFF", bg="#2A3756", font=('Arial', 15, 'bold') )
recordedArohan.set("You are singing")
recordedArohanName.place(x=50,y=430,width=500,height=35 )

raagaRecDisplay = StringVar()
raagaRecDisplayName = Label( tabCorrect, textvariable=raagaRecDisplay, fg="#CCCCCC", bg="#2A3756", font=('Arial', 20, 'bold') )
raagaRecDisplay.set("")
raagaRecDisplayName.place(x=50,y=465,width=500,height=35 )

##########################################################################################################################################
#END

xsignal = None
fsampling = 44100
steps = dict()
steps[1] = list()
steps[2] = list()
steps[3] = list()
stepsLearn = list()

class RecordThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = False

    def start(self):
        self.running = True
        threading.Thread.start(self)
    
    def stop(self):
        self.running = False
        print("Record thread terminated")

    def run(self):
        while self.running:
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
        self.running = False
    
    def start(self):
        self.running = True
        threading.Thread.start(self)
    
    def stop(self):
        self.running = False
        print("Computation thread terminated")
    
    def run(self):
        while self.running:
            global fsampling
            global xsignal
            global key
            global notes
            global raga
            global tabControl
            global raagaRecDisplay
            global stepsLearn
            #BEGIN
            #   RETRIVE_STEPS_FROM_WAV_FILE
            fs = fsampling
            compute_signal = logmmse(xsignal, fs)
            nperseg = 2**14     #16K            ---------------------------------------------
            noverlap = 2**12    #4K
            f, t, Sxx = signal.spectrogram(compute_signal, fs, nperseg=nperseg,noverlap=noverlap, return_onesided=True)
            compute_filter = (f>55) & (f<1760)
            f = f[compute_filter]
            Sxx = Sxx[compute_filter, ...]
            limit = 10.0*np.log10((np.std(Sxx, dtype=np.float64) + np.mean(Sxx, dtype=np.float64))/2) + 3
            if limit < 40:
                if tabControl.index(tabControl.select()) == 0:
                    if len(steps[3]) > 0:
                        note= list(set(steps[3]))
                        [ragaDict, real, deviation] = RagaDetect.getRagaBySteps(sorted(note))
                        # print(notes)
                        # print(ragaDict["Name"], " - ", ragaDict["Carnatic Notes"])
                        raga.set("\"{}\"".format(ragaDict["Name"]))
                        notes.set("  ".join(ragaDict["Carnatic Notes"]))
                else:
                    if len(stepsLearn) > 0:
                        notes3 = list(set(stepsLearn))
                        swaraString = StepConversion.ConvertStepsToSwaras(notes3, LearnRaga["Carnatic Notes"])
                        raagaRecDisplay.set(swaraString)
                        #MODIFY
                    else:
                        raagaRecDisplay.set("")
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
                    if tabControl.index(tabControl.select()) == 0:
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
                        results2 = list(RagaDetect.getRagaBySteps(sorted(notes2)))    #returns [raga, real, deviation2]
                        
                        if results2[1] == True:
                            # print(notes2)
                            # print(results2[0]["Name"], " - ", results2[0]["Carnatic Notes"])
                            raga.set("\"{}\"".format(results2[0]["Name"]))
                            notes.set("  ".join(results2[0]["Carnatic Notes"]))

                        elif results1[1] == True:
                            # print(notes1)
                            # print(results1[0]["Name"], " - ", results1[0]["Carnatic Notes"])
                            raga.set("\"{}\"".format(results1[0]["Name"]))
                            notes.set("  ".join(results1[0]["Carnatic Notes"]))
            
                        else:
                            if results2[2] < results1[2]:
                                # print(notes2)
                                # print(results2[0]["Name"], " - ", results2[0]["Carnatic Notes"])
                                raga.set("\"{}\"".format(results2[0]["Name"]))
                                notes.set("  ".join(results2[0]["Carnatic Notes"]))
                            
                            elif not set(steps[3]).issubset(steps[2]):    
                                # print(notes1)
                                # print(results1[0]["Name"], " - ", results1[0]["Carnatic Notes"])
                                raga.set("\"{}\"".format(results2[0]["Name"]))
                                notes.set("  ".join(results2[0]["Carnatic Notes"]))
                            else:
                                steps[3] = steps[2]
                                steps[2] = steps[1]
                                steps[1] = temp
                    else:
                        stepsLearn, _ = StepConversion.getStepConversion(list(freqs.keys()),key2)
                        stepsLearn = RemoveSingleElement(stepsLearn)
                        notes3 = list(set(stepsLearn))
                        swaraString = StepConversion.ConvertStepsToSwaras(notes3, LearnRaga["Carnatic Notes"])
                        raagaRecDisplay.set(swaraString)
            #END
            time.sleep(6)

rec_thread = RecordThread()
comp_thread = ComputeThread()
rec_thread.start()
time.sleep(7)
comp_thread.start()
UiObj.configure(bg="#2A3756")
UiObj.geometry("600x600")
UiObj.title("RAGA DETECTION AND CORRECTION")
tabControl.pack(expand = 1, fill ="both")
widgets[0].select()
widgets2[0].select()
UiObj.mainloop()