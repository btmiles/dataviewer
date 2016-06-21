import matplotlib.pyplot as plt
import numpy as np
#import ioFiles
import os
import ioCSV

def dictToHist(dict, title, bins): #dict should have structure {"name": [], "data" : []}
    fig = plt.figure(title)
    data = []
    for key in dict:
        print key
        a = np.array(dict[key], dtype=float)
        data.append(a)
    data=[]
    data.append(np.array(dict["a"], dtype=float))
    #data.append(np.array(dict["3"], dtype=float))
    n, bins, patches = plt.hist(data, bins, normed=0, stacked=True, color= ['b'])
    plt.ylim([0,12])
    plt.xlim([0*10**-9,35*10**-9])
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='on') # labels along the bottom edge are off
    plt.tick_params(
        axis='y',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        left='off',      # ticks along the bottom edge are off
        right='off',         # ticks along the top edge are off
        labelbottom='on') # labels along the bottom edge are off
    plt.legend()
    plt.show()

def histFromCSV():
    bins = [5.00E-09,7.50E-09,1.00E-08,1.25E-08,1.50E-08,1.75E-08,2.00E-08,2.25E-08,2.50E-08,2.75E-08,3.00E-08,3.25E-08,3.50E-08,3.75E-08,4.00E-08,4.25E-08,4.50E-08]
    #19
    bins = np.linspace(0*10**-9,4.0*10**-8,17)
    print bins
    title = "Values_for_histo2.csv"
    data = ioCSV.fromCSV(title, True)
    dictToHist(data,"Maxima",bins)

def strip_values():
    bins = 8#28, 19, 20, 22
    title = "20nmAFMdata.csv"
    data = ioCSV.fromCSV(title, True)
    cleaned = {}
    for key in data:
        array=[]
        for item in data[key]:
            if float(item) != 0.0:# and  float(item) >= 7.8*10**-9:
                array.append(float(item))
        cleaned[key] = array
    dictToHist(cleaned,"Maxima",bins)

def main():
    suggestedfile = ""
    wildcardsCSV = [("CSV Files", "*.csv"),("All files", "*.*")]
    directory = os.getcwd()
    #ioFiles.whichFile(wildcardsCSV, suggestedfile, directory)

strip_values()
