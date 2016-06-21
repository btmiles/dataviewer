#toCSV

##takes data with name and associated data collumn, and outputs to .csv
import numpy as np
def toCSV(dataset, filename):
    filename = filename.split(".csv")
    filename[0]+=".csv"
    
    column_names = ""
    max_length = 0
    data_lengths = []
    data_out = []
    
    for name in dataset:
        column_names += "%s," % str(name)
        data_lengths.append(len(dataset[name]))
    max_length = np.max(data_lengths)
    data_out.append(column_names)
    
    for i in range(max_length):
        row = ""
        for name in dataset:
            if i<len(dataset[name]):
                row += "%s," % dataset[name][i]
            else:
                row += ","
        data_out.append(row)
    
    file = open(filename[0], 'w')
    for row in data_out:
        file.write(row +"\n")
    file.close()
def stringArrayToCSV(data,filename):

    filename = filename.split(".csv")
    filename[0]+=".csv"
    file = open(filename[0], 'w')
    for row in data:
        file.write(row +"\n")
    file.close()
def fromCSV(filename, clean = False): # assumes csv of first row keys then columned data below
    dictionary = {}
    rows=[]
    names = []
    data = []
    
    file = open(filename, 'r')
    firstline = file.readline()
    
    if firstline == "":
        return
    
    firstline, junk = firstline.split("\n")
    catchkeys = [x.strip() for x in firstline.split(',')]
    
    for line in file:
        catchrows = ([x.strip() for x in line.split(',')])
        rows.append(catchrows)
    rows = np.array(rows)
    file.close()
    
    for item in catchkeys: # populate names array
        if item != "":
            names.append(item)
    
    i = 0        
    for name in names: # assign to dict
        catchdata = np.array(rows[:,i])
        if clean:
            tempcol = []
            for item in catchdata:
                if item != "":
                        tempcol.append(float(item))
            catchdata = tempcol
        data.append(catchdata)
        i +=1 
    #dictionaryT = {"name":names, "data":data}
    
    #broke this on purpose
    
    for i in range(0,len(names)):
        dictionary[name[i]] = data[i] 
    return dictionary


# def main():
    # testfilename = "testtoCSV.csv"
    # names = ["harry", "barry", "larry"]
    # harrymoney = [1,2,3,4,5,6,7]
    # barrymoney = [1,2,3]
    # larrymoney = [2,9,18]
    # testdata = {names[0] : harrymoney, names[1] : barrymoney, names[2]: larrymoney}
    # toCSV(testdata, testfilename)

# def main2():
    # fromCSV("2015-09-10_14-18-17_Sample11-A_multicolour_R_optomised_x30_y10.zis_collected_maxima.csv", True)