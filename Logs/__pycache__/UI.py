from tkinter import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np

note_list = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
widgets = list()

def sel():
        print(v.get())

UiObj = Tk()
v = StringVar()
xc=40
yc=30

var = StringVar()
keySelect = Label( UiObj, textvariable=var, fg="#FFFFFF", bg="#353545", font=('Arial', 18, 'bold italic') )
var.set("SELECT KEY")
keySelect.place(x=150,y=yc,width=300,height=25 )
xc += 20
yc += 30


s = len(note_list)
i = 0
for item in note_list:
    widgets.append(Radiobutton(UiObj,bg="#353545", text = item, variable = v, value = item, fg="#FFFFFF",selectcolor="#252535",command=sel, font="Arial 15"))
    widgets[i].place(x=xc,y=yc)
    xc += 90
    s -= 1
    i += 1
    if s < 7:
        xc = 60
        yc = 100
        s = 12

raga = StringVar()
ragaName = Label( UiObj, textvariable=raga, fg="#FFFFFF", bg="#353545", font=('Times', 20, 'bold') )
raga.set("\"M o h a n a m\"")
ragaName.place(x=150,y=180,width=300,height=25 )

notes = StringVar()
notesName = Label( UiObj, textvariable=notes, fg="#FFFFFF", bg="#353545", font=('Times', 15, 'bold') )
notes.set("S  R2  G3  P  D2  S'")
notesName.place(x=150,y=220,width=300,height=25 )

fig = Figure(figsize=(5, 4), dpi=100)
t = np.arange(0, 3, .01)
fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

canvas = FigureCanvasTkAgg(fig, master=UiObj)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().place(x=150,y=280,width=300,height=300 )

UiObj.configure(bg="#353545")
UiObj.geometry("600x600")
UiObj.title("RAGA DETECTION")
widgets[0].select()
UiObj.mainloop()