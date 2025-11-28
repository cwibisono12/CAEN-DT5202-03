#!/usr/bin/env python3

import sys
sys.path.append("..")
from src import dt5202ev



if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import matplotlib.ticker as tck

    #Below is an example to generate low and high gain spectra
    #from the spectroscopy mode for a specific channel id :
    filein = sys.argv[1]
    bin_number = int(sys.argv[2])
    
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
    plt.rcParams['figure.dpi'] = 200
    
    #Open the raw data:
    with open(filein, mode='rb') as fin:
        
        #Retrieve an acquisition mode:
        acq_mode,time_unit = dt5202ev.dt5202_headerfile(fin)
        
        
        LG = []
        HG = []
        #Iterate over event data:
        while(1):
            #Retrieve event data
            temp = dt5202ev.dt5202_event(fin, acq_mode, time_unit)
            if temp ==  -1:
                break
            else:
                for i in temp.keys():
                    if i == 4 and temp[4][1] == 1:
                        LG.append(temp[4][0][0])

                    if i == 4 and temp[4][1] == 2:
                        HG.append(temp[4][0][1])

                    if i == 4 and temp[4][1] == 3:
                        LG.append(temp[4][0][0])
                        HG.append(temp[4][0][1])


        fig, ax=plt.subplots(1,2)
        ax[0].hist(LG, bins=bin_number,label='PHA_LG (ADC unit)')
        ax[1].hist(HG, bins=bin_number,label='PHA_HG (ADC unit)')

        for i in range(2):
            ax[i].tick_params(direction='in',axis='both',which='major',bottom='True',left='True',top='True',right='True',length=9,width=0.75)
            ax[i].tick_params(direction='in',axis='both',which='minor',bottom='True',left='True',top='True',right='True',length=6,width=0.75)
            ax[i].xaxis.set_minor_locator(tck.AutoMinorLocator(n=5))
            ax[i].yaxis.set_minor_locator(tck.AutoMinorLocator(n=5))
            ax[i].legend()

            ax[i].set_ylabel('counts')
        ax[0].set_xlim(0,1000)
        ax[1].set_xlim(0,1000)
        ax[0].set_xlabel('PHA_LG')
        ax[1].set_xlabel('PHA_HG')
        plt.show()


