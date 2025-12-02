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

    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
    plt.rcParams['figure.dpi'] = 200
    
    #Open the raw data:
    with open(filein, mode='rb') as fin:
        
        #Retrieve an acquisition mode:
        acq_mode,time_unit = dt5202ev.dt5202_headerfile(fin)
         
        
        ToA4 = []
        ToT4 = []
        ToA5 = []
        ToT5 = []
        #Iterate over event data:
        while(1):
            #Retrieve event data
            temp = dt5202ev.dt5202_event(fin, acq_mode, time_unit)
            if temp ==  -1:
                break
            else:
                for i in temp.keys():
                    if (temp[i][1] == 16 or temp[i][1] == 48) and i == 4:
                        ToA4.append(temp[i][0][0])

                    if (temp[i][1] == 17 or temp[i][1] == 18 or temp[i][1] == 49 or temp[i][1] == 50)  and i == 4:
                        ToA4.append(temp[i][0][1])

                    if (temp[i][1] == 19 or temp[i][1] == 51) and i == 4:
                        ToA4.append(temp[i][0][2])

                    if temp[i][1] == 32 and i == 4:
                        ToT4.append(temp[i][0][0])

                    if (temp[i][1] == 33 or temp[i][1] == 34 or temp[i][1] == 48) and i == 4:
                        ToT4.append(temp[i][0][1])

                    if (temp[i][1] == 35 or temp[i][1] == 49 or temp[i] == 50) and i == 4:
                        ToT4.append(temp[i][0][2])

                    if temp[i][1] == 51 and i == 4:
                        ToT4.append(temp[i][0][3])

                    if (temp[i][1] == 16 or temp[i][1] == 48) and i == 5:
                        ToA5.append(temp[i][0][0])

                    if (temp[i][1] == 17 or temp[i][1] == 18 or temp[i][1] == 49 or temp[i][1] == 50)  and i == 5:
                        ToA5.append(temp[i][0][1])

                    if (temp[i][1] == 19 or temp[i][1] == 51) and i == 5:
                        ToA5.append(temp[i][0][2])

                    if temp[i][1] == 32 and i == 5:
                        ToT5.append(temp[i][0][0])

                    if (temp[i][1] == 33 or temp[i][1] == 34 or temp[i][1] == 48) and i == 5:
                        ToT5.append(temp[i][0][1])

                    if (temp[i][1] == 35 or temp[i][1] == 49 or temp[i] == 50) and i == 5:
                        ToT5.append(temp[i][0][2])

                    if temp[i][1] == 51 and i == 5:
                        ToT5.append(temp[i][0][3])

        fig, ax=plt.subplots(2,2)
        ax[0,0].hist(ToA4, bins=1000,label='ToA_chan4')
        ax[0,1].hist(ToT4, bins=bin_number,label='ToT_chan4')
        ax[1,0].hist(ToA5, bins=1000,label='ToA_chan5')
        ax[1,1].hist(ToT5, bins=bin_number,label='ToT_chan5')

        for i in range(2):
            ax[0,i].tick_params(direction='in',axis='both',which='major',bottom='True',left='True',top='True',right='True',length=9,width=0.75)
            ax[0,i].tick_params(direction='in',axis='both',which='minor',bottom='True',left='True',top='True',right='True',length=6,width=0.75)
            ax[0,i].xaxis.set_minor_locator(tck.AutoMinorLocator(n=5))
            ax[0,i].yaxis.set_minor_locator(tck.AutoMinorLocator(n=5))
            ax[0,i].legend()

            ax[1,i].tick_params(direction='in',axis='both',which='major',bottom='True',left='True',top='True',right='True',length=9,width=0.75)
            ax[1,i].tick_params(direction='in',axis='both',which='minor',bottom='True',left='True',top='True',right='True',length=6,width=0.75)
            ax[1,i].xaxis.set_minor_locator(tck.AutoMinorLocator(n=5))
            ax[1,i].yaxis.set_minor_locator(tck.AutoMinorLocator(n=5))
            ax[1,i].legend()

        
        ax[0,0].set_ylabel('counts')
        ax[1,0].set_ylabel('counts')
        ax[0,0].set_xlim(0,200)
        ax[1,0].set_xlim(0,200)
        ax[0,1].set_xlim(0,200)
        ax[1,1].set_xlim(0,200)
        
        ax[1,0].set_xlabel('Time of Arrival (LSB)')
        ax[1,1].set_xlabel('Time over Threshold (LSB)')
        plt.show()


