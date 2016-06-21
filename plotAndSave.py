import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib
from pylab import *
from scipy.special import basic
import sys
import cPickle as pickle
from mpl_toolkits.axes_grid1 import make_axes_locatable

def load(file):
    return  pickle.load( open(file, "rb" ) )
    
def plot(data,col, clims, colbar, title,folder):
    if clims =="":
        clims = [0,0]
        clims[1] = np.max(data)
    try:
        plt.close('all')
    except:
        print "not closed"
    thistitle = title
    fig = plt.figure(thistitle, facecolor = 'white')
    ax = plt.gca()
    a = ax.imshow(data, interpolation="nearest", cmap=col)
    #plt.axis('equal')
    plt.axis('off')
    if colbar:
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        plt.colorbar(a, cax=cax,cmap=col)
    a.set_clim(clims[0],clims[1])
    plt.legend()
    fname=folder+"plots/"+title+".pdf"
    savefig(fname, bbox_inches='tight')
    #plt.show()
    
def axialplot():
    dict = load("save.p")
    array = np.zeros(dict["p1"]["area"].shape)
    i=0
    for key in dict:
        i+=1
        plot(dict[key]["area"], "gray", "", True, str(dict[key]["position"]), "axialpaper")
        array += dict[key]["area"]
    array = array / i
    print "hello"
    plot(array, "gray", "", True, "average", "axialpaper")
        
axialplot()