# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 12:01:15 2020

@author: Paul
"""
#Target is what youre aiming to get 
#Source is whats displayed on SLM (intermediate)
#Out is the calculated

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

x = 1024
y = 768
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
trap(510,515,1024,382,387,768,target)

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
def GS(target,source,o):
    A = np.fft.ifft2(target)
    for i in range(50):
        B = Amplitude(source) * np.exp(1j * Phase(A))
        C = np.fft.fft2(B)
        D = Amplitude(target) * np.exp(1j * Phase(C))
        A = np.fft.ifft2(D)
    output = Phase(A)
    for i in range(x):
        for n in range(y):
            if output[n][i] > o:
                output[n][i] = o
    return output
output = GS(target,source,0)

#Make array into PIL Image
def mkPIL(array):
    im = Image.fromarray(np.uint8(array))
    return im


im = mkPIL(output)
plt.imshow(im, cmap='gray')


fig = plt.figure(figsize=(20,15), frameon=False)
ax = fig.add_subplot(111)
ax.set_yticklabels([])                        
ax.set_xticklabels([])
plt.imshow(target, cmap='gray')
plt.show()



fig = plt.figure(figsize=(20,15), frameon=False)
ax = fig.add_subplot(111)
ax.set_yticklabels([])                        
ax.set_xticklabels([])
plt.imshow(output, cmap='gray')
plt.show()
