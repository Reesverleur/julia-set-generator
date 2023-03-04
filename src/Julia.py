import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from numba import jit
import math
import time

# Creates complex grid
def complexgrid(ix,iy):
    z = np.zeros(ix.size*iy.size,dtype=complex)
    for y in range(iy.size):
        for x in range(ix.size):
            z[y+x*iy.size]=complex(ix[x],iy[y])
    return z

# Iterates each point until divergence or max iterations (optimized with Numba)
@jit
def julia_iter(z,c,max_iter,z_max):
    if max_iter <=0:
        return
    for x in range (max_iter):
        z = np.square(z)+c
        if abs(z)>z_max:
            return z, x+1
    return z,x+1


def julia(c, parameter=False, label = '',zabs_max = 10, nit_max = 100, im_width = 1500, im_height = 1500,xmin = -2, xmax = 2, ymin = -2, ymax = 2):
    # Time the function
    time0 = time.time()
    # Set up the complex grid in z
    ix = np.linspace(xmin,xmax,im_width)
    iy = np.linspace(ymin,ymax,im_height)
    z = complexgrid(ix,iy)
    
    # If generating a parameter space, iterate on a different variable
    if parameter:
        output = [julia_iter(c,x,nit_max,zabs_max)[1] for x in z]
    else:
        output = [julia_iter(x,c,nit_max,zabs_max)[1] for x in z]
        
    ratio = [x/nit_max for x in output]
    
    julia = np.reshape(ratio,(im_height,im_width),order='F')
    # Generate figure
    fig, ax = plt.subplots(figsize=(im_width*1.35/96,im_height*1.35/96),dpi = 96)
    ax.imshow(-julia, interpolation='nearest', cmap=cm.bone)
    ax.axis('off')
    ax.margins(x=0)
    ax.margins(y=0)
    # Save figures with somewhat arbitrary names
    if parameter:
        plt.savefig(f"{label}Mandelbrot_{c}.jpg",dpi = 96,bbox_inches='tight')
    else:
         plt.savefig(f"{label}Julia_{c}.jpg",dpi = 96,bbox_inches='tight')   
    plt.gca().invert_yaxis()
    plt.show()
    time1 = time.time()-time0
    if parameter:
        print(f'z_0 = {c}')
    else:
        print(f'c = {c}')
    print(f'Time = {time1} seconds')
    
# A simple function to generate a string of letters for when outputs should be alphabetized
def label(value,maximum):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    length = math.ceil(np.log(maximum)/np.log(26))
    string = ''
    for n in range(length):
        char = alphabet[value//(26**(length-(n+1)))]
        value = value-((value//(26**(length-(n+1)))))*26**(length-(n+1))
        string+=char
    return string
    
if __name__=='__main__':
    # When run this will trace the parameter around a circle of radius 0.815 and generate 1800 frames at 1080p resolution (this takes a long time and will hopefully be improved later)
    frames = 1800
    for t in range(frames+1):
        lab = label(t,frames+1)
        julia(complex(0.8150681*np.cos(t*2*np.pi/frames),0.8150681*np.sin(t*2*np.pi/frames)),parameter = False,label = lab,nit_max=500, im_width=1920,im_height=1080,xmin=-3,xmax=3,ymin=-3*9/16,ymax=3*9/16)