#!/usr/bin/env python3

import sys
sys.path.append("..")
from src import dt5202ev



if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import matplotlib.ticker as tck

    #Below is an example to generate the Time of Arrival and Time over Threshold spectra
    #in the least significant bit from the spectroscopy and timing mode for a specific channel id :
    filein = sys.argv[1]
    bin_number = int(sys.argv[2]) #ex. 200
    chan_id = int(sys.argv[3]) #ex. 4 or 5

    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
    plt.rcParams['figure.dpi'] = 200
    
    #Open the raw data:
    with open(filein, mode='rb') as fin:
        
        #Retrieve an acquisition mode:
        acq_mode,time_unit = dt5202ev.dt5202_headerfile(fin)
         
        
        ToA = []
        ToT = []
        #Iterate over event data:
        while(1):
            #Retrieve event data
            temp = dt5202ev.dt5202_event(fin, acq_mode, time_unit)
            if temp ==  -1:
                break
            else:
                for i in temp.keys():
                    if temp[i][1] == 16 and i == chan_id:
                        ToA.append(temp[i][0][0])

                    if (temp[i][1] == 17 or temp[i][1] == 18 or temp[i][1] == 49 or temp[i][1] == 50)  and i == chan_id:
                        ToA.append(temp[i][0][1])

                    if temp[i][1] == 19 and i == chan_id:
                        ToA.append(temp[i][0][2])

                    if temp[i][1] == 32 and i == chan_id:
                        ToT.append(temp[i][0][0])

                    if (temp[i][1] == 33 or temp[i][1] == 34) and i == chan_id:
                        ToT.append(temp[i][0][1])

                    if (temp[i][1] == 35 or temp[i][1] == 49 or temp[i] == 50) and i == chan_id:
                        ToT.append(temp[i][0][2])

                    if temp[i][1] == 48 and i == chan_id:
                        ToA.append(temp[i][0][0])
                        ToT.append(temp[i][0][1])

                    if temp[i][1] == 51 and i == chan_id:
                        ToA.append(temp[i][0][2])
                        ToT.append(temp[i][0][3])

        fig, ax=plt.subplots(1,2)
        ax[0].hist(ToA, bins=bin_number,label='ToA')
        ax[1].hist(ToT, bins=bin_number,label='ToT')

        for i in range(2):
            ax[i].tick_params(direction='in',axis='both',which='major',bottom='True',left='True',top='True',right='True',length=9,width=0.75)
            ax[i].tick_params(direction='in',axis='both',which='minor',bottom='True',left='True',top='True',right='True',length=6,width=0.75)
            ax[i].xaxis.set_minor_locator(tck.AutoMinorLocator(n=5))
            ax[i].yaxis.set_minor_locator(tck.AutoMinorLocator(n=5))
            ax[i].legend()

            ax[i].set_ylabel('counts')
        ax[0].set_xlim(0,4096)
        ax[1].set_xlim(0,200)
        ax[0].set_xlabel('Time of Arrival (LSB)')
        ax[1].set_xlabel('Time over Threshold (LSB)')
        plt.show()


