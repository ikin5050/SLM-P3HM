# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 11:40:04 2020

@author: Paul
"""

import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import  Label
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

xtmi = 510
xtma = 515
xs = 1024
ytmi = 382
ytma = 387
ys = 768



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
target,source,output=initialize(1024,768)

# creates trap between XTrapMin-XTrapMax and YTrapMin-YTrapMax on Array
def trap(xtmi,xtma,xs,ytmi,ytma,ys,array):
    for i in range(xs):
        if xtmi < i < xtma:
            for n in range(ys):
                if ytmi < n < ytma:
                    array[n][i] = 255
    return
trap(xtmi,xtma,xs,ytmi,ytma,ys,target)

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
    for i in range(50):
        B = Amplitude(source) * np.exp(1j * Phase(A))
        C = np.fft.fft2(B)
        D = Amplitude(target) * np.exp(1j * Phase(C))
        A = np.fft.ifft2(D)
    output = Phase(A)
    return output
output = GS(target,source)

#Make array into PIL Image
def mkPIL(array):
    im = Image.fromarray(np.uint8(array))
    return im

def up(mi,ma):
    mi += 1
    ma += 1
    return

def down(mi,ma):
    mi -= 1
    ma -= 1
    return

def right(mi,ma):
    mi += 1
    ma += 1
    return

def left(mi,ma):
    mi -= 1
    ma -= 1
    return
  
im = mkPIL(output)
plt.imshow(im, cmap='gray')

root = tk.Tk()

def main():
    
    app = Lower(root)
    root.mainloop()


class Lower:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        self.button1 = tk.Button(self.frame, text = 'Create window', width = 25, command = self.new_window)
        self.button1.pack()
        self.displayimg = tk.Button(self.frame, text = 'Display', width = 25, command = self.plot)
        self.displayimg.pack()
    def new_window(self):
        self.newWindow = tk.Toplevel(root)
        self.app = Display(self.newWindow)
    def plot(self): 
        fig = plt.figure(figsize=(20,15), frameon=False)
        ax = fig.add_subplot(111)
        ax.set_yticklabels([])                        
        ax.set_xticklabels([])
        plt.imshow(output, cmap='gray')
        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas.get_tk_widget().pack()
        canvas.draw()
    def Recalculate(self):
        target,source,output = initialize(xs,ys)
        trap(xtmi,xtma,xs,ytmi,ytma,ys,target)
        output = GS(target,source)
        fig = plt.figure(figsize=(20,15), frameon=False)
        ax = fig.add_subplot(111)
        ax.set_yticklabels([])                        
        ax.set_xticklabels([])
        plt.imshow(output, cmap='gray')
        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas.get_tk_widget().pack()
        canvas.draw()
    def close(self): 
        self.master.destroy()
    
# https://stackoverflow.com/questions/15999661/image-in-tkinter-window-by-clicking-on-button

class Display:
    
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.up = tk.Button(self.frame, text = 'Up', width = 25, command = up(ytmi,ytma))
        self.up.pack()
        self.down = tk.Button(self.frame, text = 'Down', width = 25, command = down(ytmi,ytma))
        self.down.pack()
        self.right = tk.Button(self.frame, text =  'Right', width = 25, command = right(xtmi,xtma))
        self.right.pack()
        self.left = tk.Button(self.frame, text = 'Left', width = 25, command = left(xtmi,xtma))
        self.left.pack()
        self.rec = tk.Button(self.frame, text = 'Recalculate', width = 25, command = Lower.Recalculate(self))
        self.rec.pack()
        self.kill = tk.Button(self.frame, text = 'Kill', width = 25, command = self.kill)
        self.kill.pack()
        
    def kill(self): 
        self.master.destroy()
 
main()