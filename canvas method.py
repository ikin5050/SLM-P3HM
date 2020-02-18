import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


""" 
See if can draw new window on exteral screen
https://stackoverflow.com/questions/26286660/how-to-make-a-window-fullscreen-in-a-secondary-display-with-tkinter
"""

#Define the target, source and output arrays. Source has to be completely white otherwise it kills everything
def initialize(x,y):
    xarr = np.zeros(x)
    yarr = np.zeros(y)
    target = np.meshgrid(xarr,yarr)
    target = target[0]
    source = np.meshgrid(xarr,yarr)
    source = source[0]
    output = np.meshgrid(xarr,yarr)
    output = output[0]
    for i in range(x):
        for n in range(y):
            source[n][i] = 1
    return target, source, output

# creates trap between XTrapMin-XTrapMax and YTrapMin-YTrapMax on Array
def trap(xtmi,xtma,xs,ytmi,ytma,ys,array):
    for i in range(xs):
        if xtmi < i < xtma:
            for n in range(ys):
                if ytmi < n < ytma:
                    array[n][i] = 255
    return

#Returns the amplitude of a complex number
def Amplitude(x):
    if isinstance(x, complex):
        return np.sqrt(x.real**2+x.imag**2)
    else:
        return np.abs(x)

#Returns the phase of a complex number
def Phase(z):
        return np.angle(z)

#Main GS algorithm implementation using numpy FFT package
#performs the GS algorithm to obtain a phase distribution for the plane, Source
#such that its Fourier transform would have the amplitude distribution of the plane, Target.
def GS(target,source):
    A = np.fft.ifft2(target)
    for i in range(5):
        B = Amplitude(source) * np.exp(1j * Phase(A))
        C = np.fft.fft2(B)
        D = Amplitude(target) * np.exp(1j * Phase(C))
        A = np.fft.ifft2(D)
    output = Phase(A)
    return output

#Make array into PIL Image
def mkPIL(array):
    im = Image.fromarray(np.uint8(array))
    return im

def up():
    global ytmi
    global ytma
    ytmi -= 10
    ytma -= 10
    return 

def down():
    global ytmi
    global ytma
    ytmi += 10
    ytma += 10
    return

def right():
    global xtmi
    global xtma
    xtmi += 10
    xtma += 10
    return

def left():
    global xtmi
    global xtma
    xtmi -= 10
    xtma -= 10
    return
  
xtmi = 125
xtma = 130
xs = 1024
ytmi = 0
ytma = 5
ys = 768


root = tk.Tk()
root.attributes('-fullscreen', True)
def main():
    app = Lower(root)
    root.mainloop()

class Lower:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master).pack()
        self.displayimg = tk.Button(self.frame, text = 'Display', width = 25, command = self.plot)
        self.displayimg.pack()
        self.makewidg()
        print(root.winfo_screenwidth(),root.winfo_screenheight())
    def makewidg(self):
        self.fig = plt.figure(figsize=(100,100), frameon=False)  #changing figsize doesnt cange the size of the plot display
        self.fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
        self.fig.tight_layout()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_yticklabels([])                        
        self.ax.set_xticklabels([])
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(expand=True)
        self.canvas.figure.tight_layout()
        self.canvas.draw()
        self.new_window()
    def new_window(self):
        self.newWindow = tk.Toplevel()
        self.app = Display(self.newWindow)
    def plot(self): 
        global xtmi, xtma, xs, ytmi, ytma, ys, i
        target,source,output=initialize(xs,ys)
        trap(xtmi,xtma,xs,ytmi,ytma,ys,target)
        output = GS(target,source)
        self.ax.imshow(output, cmap='gray')
        self.ax.set_yticklabels([])                        
        self.ax.set_xticklabels([])
        self.canvas.draw()
        self.ax.clear()
        
    def kill(self): 
        root.destroy()
    
class Display:
    
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        self.up = tk.Button(self.frame, text = 'Up', width = 25, command = up)
        self.up.pack()
        self.down = tk.Button(self.frame, text = 'Down', width = 25, command = down)
        self.down.pack()
        self.right = tk.Button(self.frame, text =  'Right', width = 25, command = right)
        self.right.pack()
        self.left = tk.Button(self.frame, text = 'Left', width = 25, command = left)
        self.left.pack()
        self.kill = tk.Button(self.frame, text = 'Kill', width = 25, command = self.kill)
        self.kill.pack()
    def kill(self): 
        root.destroy()
main()