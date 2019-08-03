#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 11:16:05 2019

@author: snaily
"""

import tkinter as tk
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import tkinter.filedialog


def draw(event, x, y, flags, param):
	global btn_down
	if event == cv2.EVENT_LBUTTONDBLCLK: 
		btn_down = True
		cv2.circle(src,(x,y), 2, (255,0,0), -1)
		if len(pts)>0:
			cv2.line(src, pts[-1], (x, y), (0,0,0), 2)
		cv2.imshow('Source',src)
		param=(x,y)
		pts.append(param)
	
	return

def get_center(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK and len(c)<2:
        cv2.circle(dst,(x,y), 1, (0,0,0), -1)
        cv2.imshow('Destination',dst)
        param=(x,y)
        c.append(param)

root = tk.Tk()
# source image
File = tkinter.filedialog.askopenfilename(parent=root, 
                                          initialdir="C:/",
                                          title='Choose an source image.')
source = Image.open(File)
src = np.array(source)

# destination image
File = tkinter.filedialog.askopenfilename(parent=root, 
                                          initialdir="C:/",
                                          title='Choose an source image.')
dest = Image.open(File)
dst = np.array(dest)

# get the co-ordinates
pts=list()
cv2.namedWindow('Source')
cv2.imshow('Source',src)
pts.append(cv2.setMouseCallback('Source', draw))
del pts[0]
cv2.waitKey(0)

# This is where the CENTER of the airplane will be placed
cv2.namedWindow('Destination')
cv2.imshow('Destination',dst)
c=list()
c.append(cv2.setMouseCallback('Destination', get_center))
cv2.waitKey(0)
del c[0]
print(c)
center = c[0]

# create mask around the given co-ordinates
src_mask = np.zeros(src.shape, src.dtype)
poly = np.array(pts, np.int32)
cv2.fillPoly(src_mask, [poly], (255, 255, 255))

 
# Clone seamlessly.
output1 = cv2.seamlessClone(src, dst, src_mask, center, cv2.NORMAL_CLONE)
output2 = cv2.seamlessClone(src, dst, src_mask, center, cv2.MIXED_CLONE)
cv2.waitKey(0)
cv2.destroyAllWindows()

h,w,c = dst.shape
# create canvas that can fit the image
canvas = tk.Canvas(root, width=w, height=h)
canvas.pack()
# use PIL to convert Numpy ndarray to a PhotoImage
# add a photo image to the canvas
photo = ImageTk.PhotoImage(image=Image.fromarray(output1))
canvas.create_image(0,0,image=photo, anchor=tk.NW)
root.mainloop()

#cv2.imshow('dst',dst)
op1 = cv2.cvtColor(output1,cv2.COLOR_RGB2BGR)
op2 = cv2.cvtColor(output2,cv2.COLOR_RGB2BGR)
cv2.imshow('normal',op1)
cv2.imshow('mixed',op2)

plt.subplot(221),plt.imshow(src),plt.title('Source')
plt.subplot(222),plt.imshow(dst),plt.title('Destination')
plt.subplot(223),plt.imshow(output1),plt.title('Normal')
plt.subplot(224),plt.imshow(output2),plt.title('Mixed')

plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()