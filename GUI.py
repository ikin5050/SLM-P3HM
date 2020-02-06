# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 15:00:49 2020

@author: Paul

https://stackoverflow.com/questions/41657449/tkinter-not-changing-image-on-button-press
https://stackoverflow.com/questions/18369936/how-to-open-pil-image-in-tkinter-on-canvas
https://www.tutorialspoint.com/python/tk_pack.htm
https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/
https://stackoverflow.com/questions/41657449/tkinter-not-changing-image-on-button-press
https://effbot.org/tkinterbook/canvas.htm
https://stackoverflow.com/questions/19838972/how-to-update-an-image-on-a-canvas/19842646
https://stackoverflow.com/questions/28861785/python-tkinter-update-image
https://datatofish.com/entry-box-tkinter/
https://stackoverflow.com/questions/16115378/tkinter-example-code-for-multiple-windows-why-wont-buttons-load-correctly
"""

import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

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

# creates trap between XTrapMin-XTrapMax and YTrapMin-YTrapMax
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

import tkinter as tk
from tkinter import  Label

root = tk.Tk()
def main():
    
    app = Manipulation(root)
    root.mainloop()


class Manipulation:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        self.button1 = tk.Button(self.frame, text = 'Create window', width = 25, command = self.new_window)
        self.button1.pack()
        self.up = tk.Button(self.frame, text = 'Up', width = 25, command = up(ytmi,ytma))
        self.up.pack()
        self.down = tk.Button(self.frame, text = 'Down', width = 25, command = down(ytmi,ytma))
        self.down.pack()
        self.right = tk.Button(self.frame, text =  'Right', width = 25, command = right(xtmi,xtma))
        self.right.pack()
        self.left = tk.Button(self.frame, text = 'Left', width = 25, command = left(xtmi,xtma))
        self.left.pack()
        self.rec = tk.Button(self.frame, text = 'Recalculate', width = 25, command = Display.Recalculate)
        self.rec.pack()
        self.kill = tk.Button(self.frame, text = 'Kill', width = 25, command = self.close)
        self.kill.pack()
        
    def new_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Display(self.newWindow)
    def close(self): 
        self.master.destroy()
        
#Displaying on wrong frame, displayed image is just whacked on top. move all buttons to second frame?

class Display:
    
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        self.displayimg = tk.Button(self.frame, text = 'Display', width = 25, command = self.showimg)
        self.displayimg.pack()
        
    def showimg(self): 
        img = ImageTk.PhotoImage(im)
        panel = Label(root, image=img)
        panel.image = img
        panel.place(x=200,y=200)
        
    def Recalculate():
        initialize(xs,ys)
        trap(xtmi,xtma,xs,ytmi,ytma,ys,target)
        output = GS(target,source)
        ima = ImageTk.PhotoImage(mkPIL(output))
        Display.change_pic(panel,ima)
        
    def change_pic(labelname,iam):
        labelname.configure(image=iam) 
        
    def close_windows(self):
        self.master.destroy()
 
main()