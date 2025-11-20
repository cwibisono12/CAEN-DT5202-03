#!/usr/bin/env python3


import matplotlib.pyplot as plt
import matplotlib.ticker as tck


def readScanThfile(filein):
    with open(filein, mode='r') as f:
        Th = []
        Cps = []
        while(1):
            line = f.readline()
            if line == '':
                break

            if line.find('#') == -1:
                row = line.split(' ')

                val = row[0]
                val2 = row[1]
                val3 = int(row[2])
                val4 = int(float(row[3]))
                print(val3,val4)
                Th.append(val3)
                Cps.append(val4)
                
    return Th, Cps


def plot_Thresh():
    
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
    plt.rcParams['figure.dpi'] = 200
   
    fig, ax = plt.subplots()
    ax.tick_params(direction='in',axis='both',which='major',bottom='True',left='True',top='True',right='True',length=9,width=0.75)
    ax.tick_params(direction='in',axis='both',which='minor',bottom='True',left='True',top='True',right='True',length=6,width=0.75)
    ax.xaxis.set_minor_locator(tck.AutoMinorLocator(n=5))
    ax.yaxis.set_minor_locator(tck.AutoMinorLocator(n=5))
    
    Th1, Cps1 = readScanThfile('~/CAEN_DT5202_data/DCR_2/ScanTh_20.txt')
    Th2, Cps2 = readScanThfile('~/CAEN_DT5202_data/DCR_2/ScanTh_24.txt')
    Th3, Cps3 = readScanThfile('~/CAEN_DT5202_data/DCR_2/ScanTh_26.txt')
    Th4, Cps4 = readScanThfile('~/CAEN_DT5202_data/DCR_2/ScanTh_28.txt')
    Th5, Cps5 = readScanThfile('~/CAEN_DT5202_data/DCR_2/ScanTh_30r.txt')
    Th6, Cps6 = readScanThfile('~/CAEN_DT5202_data/DCR_2/ScanTh_32.txt')
    Th7, Cps7 = readScanThfile('~/CAEN_DT5202_data/DCR_2/ScanTh_35.txt')
    ax.plot(Th1, Cps1, linewidth = 0.85, drawstyle='steps-mid',label='V = 20V')
    ax.plot(Th2, Cps2, linewidth = 0.85, drawstyle='steps-mid',label='V = 24V')
    ax.plot(Th3, Cps3, linewidth = 0.85, drawstyle='steps-mid',label='V = 26V')
    ax.plot(Th4, Cps4, linewidth = 0.85, drawstyle='steps-mid',label='V = 28V')
    ax.plot(Th5, Cps5, linewidth = 0.85, drawstyle='steps-mid',label='V = 30V')
    ax.plot(Th6, Cps6, linewidth = 0.85, drawstyle='steps-mid',label='V = 32V')
    ax.plot(Th7, Cps7, linewidth = 0.85, drawstyle='steps-mid',label='V = 35V')
    ax.set_xlim(150,500)
    ax.set_ylim(bottom = 1)
    ax.legend()
    ax.set_yscale('log')
    ax.set_xlabel('Threshold')
    ax.set_ylabel('Cps')
    plt.show()


if __name__ == "__main__":
    #import sys
    #fin = sys.argv[1]
    #readScanThfile(fin)

    plot_Thresh()
