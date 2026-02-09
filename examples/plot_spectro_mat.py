#!/usr/bin/env python3

import sys
sys.path.append("..")
from src import dt5202v2
from src import parsegen


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import matplotlib.ticker as tck
    import numpy as np

    #Below is an example to generate low and high gain spectra
    #from the spectroscopy mode for a specific channel id :
    filein = sys.argv[1]
    fout_LG = sys.argv[2]
    fout_HG = sys.argv[3]
    overwrite = int(sys.argv[4])
    #chan_id = int(sys.argv[3]) #ex. 4 or 5
    
    
    id_en_LG = np.ndarray(shape=(64,4096),dtype=np.int32)
    id_en_HG = np.ndarray(shape=(64,4096),dtype=np.int32)

    for i in range(0,64):
        for j in range(0,4096):
            id_en_LG[i][j] = 0
            id_en_HG[i][j] = 0

    #Open the raw data:
    with open(filein, mode='rb') as fin:
        
        #Retrieve an acquisition mode:
        acq_mode,time_unit = dt5202v2.dt5202_headerfile(fin)
        

        #Iterate over event data:
        while(1):
            #Retrieve event data
            temp = dt5202v2.dt5202_event(fin, acq_mode, time_unit)
            if temp ==  -1:
                break
            else:
                for i in temp.keys():
                    
                    if temp[i][1] == 1:
                        if i < 64 and temp[i][0][0] < 4096:
                            id_en_LG[i][temp[i][0][0]] = id_en_LG[i][temp[i][0][0]] + 1

                    if temp[i][1] == 2:
                        if i < 64 and temp[i][0][0] < 4096:
                            id_en_HG[i][temp[i][0][0]] = id_en_HG[i][temp[i][0][0]] + 1
                    

                    if temp[i][1] == 3:
                        if i < 64 and temp[i][0][0] < 4096:
                            id_en_LG[i][temp[i][0][0]] = id_en_LG[i][temp[i][0][0]] + 1
                        if i< 64 and temp[i][0][1] < 4096:
                            id_en_HG[i][temp[i][0][1]] = id_en_HG[i][temp[i][0][1]] + 1
                    

        parsegen.matwrite(fout_LG,dimy=64, dimx=4096, arr = id_en_LG, overwrite = overwrite)
        parsegen.matwrite(fout_HG,dimy=64, dimx=4096, arr = id_en_HG, overwrite = overwrite)


