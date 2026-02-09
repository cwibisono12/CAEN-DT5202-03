#!/usr/bin/env python3

import sys
sys.path.append("..")
from src import dt5202v2
from src import parsegen

def parse_calib(fcalib):
    calib_param = {}
    with open(fcalib, mode = 'r') as fin:
        lines = fin.readlines()
        for line in lines:
            if line.find('#') == -1:
                row = line.split()
                run_num = int(row[0])
                slope = float(row[1])
                intercept = float(row[2])
                calib_param[run_num] = [slope, intercept]

    return calib_param




if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import matplotlib.ticker as tck
    import numpy as np
    import random

    #Below is an example to generate low and high gain spectra
    #from the spectroscopy mode for a specific channel id :
    filein = sys.argv[1]
    fout_LG = sys.argv[2]
    fcalib= sys.argv[3]
    run_num = int(sys.argv[4])
    overwrite = int(sys.argv[5])
    #chan_id = int(sys.argv[3]) #ex. 4 or 5
    
    
    id_en_LG = np.ndarray(shape=(64,4096),dtype=np.int32)
   # id_en_HG = np.ndarray(shape=(64,4096),dtype=np.int32)

    for i in range(0,64):
        for j in range(0,4096):
            id_en_LG[i][j] = 0
    #        id_en_HG[i][j] = 0

    #Open the raw data:
    with open(filein, mode='rb') as fin:
        
        #Retrieve an acquisition mode:
        acq_mode,time_unit = dt5202v2.dt5202_headerfile(fin)
        
        calib_param = parse_calib(fcalib)
        slope = calib_param[run_num][0]
        intercept = calib_param[run_num][1]

        #Iterate over event data:
        while(1):
            #Retrieve event data
            temp = dt5202v2.dt5202_event(fin, acq_mode, time_unit)
            if temp ==  -1:
                break
            else:
                for i in temp.keys():
                    
                    if temp[i][1] == 1:
                        if i < 64 and temp[i][0][0] < 4096 :
                            energy = int(round((slope*(temp[i][0][0]+random.uniform(0.,1.)) + intercept),0))
                            #id_en_LG[i][temp[i][0][0]] = id_en_LG[i][temp[i][0][0]] + 1
                            if energy > 0 and energy < 4096:
                                id_en_LG[i][energy] = id_en_LG[i][energy] + 1

                   # if temp[i][1] == 2:
                    #    if i < 64 and temp[i][0][0] < 4096:
                     #       id_en_HG[i][temp[i][0][0]] = id_en_HG[i][temp[i][0][0]] + 1
                    

                    if temp[i][1] == 3:
                        if i < 64 and temp[i][0][0] < 4096:
                            energy = int(round((slope*(temp[i][0][0]+random.uniform(0.,1.))+ intercept),0))
                            if energy > 0 and energy < 4096:
                                id_en_LG[i][energy] = id_en_LG[i][energy] + 1
                        #if i< 64 and temp[i][0][1] < 4096:
                         #   id_en_HG[i][temp[i][0][1]] = id_en_HG[i][temp[i][0][1]] + 1
                    

        parsegen.matwrite(fout_LG,dimy=64, dimx=4096, arr = id_en_LG, overwrite = overwrite)
       # parsegen.matwrite(fout_HG,dimy=64, dimx=4096, arr = id_en_HG, overwrite = overwrite)


