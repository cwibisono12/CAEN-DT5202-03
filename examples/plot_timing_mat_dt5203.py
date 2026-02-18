#!/usr/bin/env python3

import sys
sys.path.append("..")
from src import dt5203
from src import parsegen


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import matplotlib.ticker as tck
    import numpy as np

    #Below is an example to generate ToA and ToT matrices from the 
    #Common Start/Stop Mode in the CAEN-DT5203
    filein = sys.argv[1]
    fout_ToA = sys.argv[2]
    fout_ToT = sys.argv[3]
    overwrite = int(sys.argv[4])
    #chan_id = int(sys.argv[3]) #ex. 4 or 5
    
    
    id_ToA = np.ndarray(shape=(64,4096),dtype=np.int32)
    id_ToT = np.ndarray(shape=(64,4096),dtype=np.int32)

    for i in range(0,64):
        for j in range(0,4096):
            id_ToA[i][j] = 0
            id_ToT[i][j] = 0

    #Open the raw data:
    with open(filein, mode='rb') as fin:
        
        #Retrieve an acquisition mode:
        acq_mode,time_unit = dt5203.dt5203_headerfile(fin)
        

        #Iterate over event data:
        while(1):
            #Retrieve event data
            acq_mode, temp = dt5203.dt5203_event(fin, acq_mode, time_unit)
            if temp ==  -1:
                break
            else:
                for i in temp.keys():
                    if temp[i][1] != 1:
                        if i < 64 and temp[i][0][0] < 4096:
                            id_ToA[i][temp[i][0][0]] = id_ToA[i][temp[i][0][0]] + 1
                        if i < 64 and temp[i][0][1] < 4096:
                            id_ToT[i][temp[i][0][1]] = id_ToT[i][temp[i][0][1]] + 1

                    if temp[i][1] == 1:
                        if i < 64 and temp[i][0][0] < 4096:
                            id_ToA[i][temp[i][0][0]] = id_ToA[i][temp[i][0][0]] + 1
                    


        parsegen.matwrite(fout_ToA,dimy=64, dimx=4096, arr = id_ToA, overwrite = overwrite)
        parsegen.matwrite(fout_ToT,dimy=64, dimx=4096, arr = id_ToT, overwrite = overwrite)


