#!/usr/bin/env python3

from struct import *

def dt5202_headerfile(fpr):
    '''
    Original CAEN_DT5202 Binary Data Format
    C. Wibisono
    11/20 '25
    
    Usage:
    To parse the header .dat file coming from the Janus DAQ CAEN-DT5202 
    and retrieve the acquisition mode for each file.

    Parameter(s):
    fpr: file pointer object
    Return(s):
    acq_mode: (int) acquisiton mode
    time_unit: (int) time unit (0) means LSB, (1) means ns
    '''
    
    p = Struct("@I") #Unsigned Integer (4 bytes)
    q = Struct("@B") #Unsigned char (1 bytes)
    r = Struct("@H") #Unsigned short (2 bytes)
    s = Struct("@Q") #Unsigned long long (8 bytes)
    t = Struct("@f") #float (4 bytes)
    u = Struct("@d") #double (8 bytes)

    #File Header:
    data_format, = r.unpack(fpr.read(2))
    fpr.read(3)
    board_type, = r.unpack(fpr.read(2))
    run_num, = r.unpack(fpr.read(2))
    acq_mode, = q.unpack(fpr.read(1))
    en_channels, = r.unpack(fpr.read(2))
    time_unit, = q.unpack(fpr.read(1))
    time_conv, = t.unpack(fpr.read(4))
    start_acq, = s.unpack(fpr.read(8))

    print("data_format:",data_format,"board_type:",board_type)
    print("run_num:",run_num,"acq_mode:",acq_mode)
    print("en_channel:",en_channels,"time_unit:",time_unit)
    print("time_conv:",time_conv,"start_acq:",start_acq)
    
    return acq_mode, time_unit


def dt5202_event(f, acq_mode, time_unit):
    '''
    Original CAEN_DT5202 Binary Data Format
    C. Wibisono
    11/20 '25
    
    Usage: 
    To parse the event .dat file coming from the Janus DAQ CAEN-DT5202
    and return a data object
    Parameter(s):
    f: file pointer object
    acq_mode: acquisition_mode
    time_unit: time_unit

    Return:
    scint: (dict) data object dictionary
    '''

    p = Struct("@I") #Unsigned Integer (4 bytes)
    q = Struct("@B") #Unsigned char (1 bytes)
    r = Struct("@H") #Unsigned short (2 bytes)
    s = Struct("@Q") #Unsigned long long (8 bytes)
    t = Struct("@f") #float (4 bytes)
    u = Struct("@d") #double (8 bytes)

    #Data: (each list mode consists of event header and event itself)
    ev_num = 0
        
    scint = {}
    #Spectroscopy mode:
    if acq_mode == 1:
        
        #Event_Header:
        buff = f.read(2)
        if buff == b'':
            return -1
        
        ev_size, = r.unpack(buff)

        buff2 = f.read(1)
        if buff2 == b'':
            return -1
        board_id, = q.unpack(buff2)

        buff3 = f.read(8)
        if buff3 == b'':
            return -1
        trig_timestamp, = u.unpack(buff3)

        trig_id, = s.unpack(f.read(8))
        chan_mask, = s.unpack(f.read(8))
                
        #dim = int((ev_size - 27) / 6)
        dim = ev_size - 27
        
        #Event_Data:
        ev_num = ev_num + 1
        #for k in range(dim):
        while(1):
            if dim == 0:
                break
            buff_chan_id = f.read(1)
            if buff_chan_id == b'':
                return -1
            chan_id, = q.unpack(buff_chan_id)
            buff_data_type = f.read(1)
            if buff_data_type == b'':
                return -1
            data_type, = q.unpack(buff_data_type)
            if data_type == 1:
                LG_PHA, = r.unpack(f.read(2))
                scint[chan_id] = [[LG_PHA], data_type] 
                dim = dim - 4
            if data_type == 2:
                HG_PHA, = r.unpack(f.read(2))
                scint[chan_id] = [[HG_PHA], data_type] 
                dim = dim - 4
            if data_type == 3:
                LG_PHA, = r.unpack(f.read(2))
                HG_PHA, = r.unpack(f.read(2))
                scint[chan_id] = [[LG_PHA, HG_PHA], data_type]    
                dim = dim - 6
            #print("ev_num:",ev_num, "chan_id:", chan_id, "data_type:", data_type, "LG_PHA:", LG_PHA, "HG_PHA:", HG_PHA)

        return scint



    #Timing Mode:
    if acq_mode == 2:
    
        #Event_Header:
        b_counts = 0
        buff = f.read(2)
        if buff == b'':
            return -1
        ev_size, = r.unpack(buff)
            
        buff2 = f.read(1)
        if buff2 == b'':
            return -1
        board_id, = q.unpack(buff2)

        buff3 = f.read(8)
        if buff3 == b'':
            return -1
        tref, = u.unpack(buff3)

        num_hits, = r.unpack(f.read(2))
        ev_num = ev_num + 1
        #print("ev_size:",ev_size,"board_id:",board_id,"tref:",tref,"num_hits:",num_hits)
                
        #Iterate for each event as many as num_hits:
        for i in range(num_hits):
            chan_id, = q.unpack(f.read(1))
            data_type, = q.unpack(f.read(1))
            #b_counts = b_counts+2
            if data_type == 16: #0x10
                if time_unit == 0:
                    ToA, = p.unpack(f.read(4))
                    #ToT, = r.unpack(f.read(2))
                    #  b_counts = b_counts + 6
                if time_unit == 1:
                    ToA, = t.unpack(f.read(4))
                    #ToT, = t.unpack(f.read(4))
                    #   b_counts = b_counts + 8
                scint[chan_id] = [[ToA],data_type]

            if data_type == 32: #0x20
                if time_unit == 0:
                    ToT, = r.unpack(f.read(2))
                if time_unit == 1:
                    ToT, = t.unpack(f.read(4))
                scint[chan_id] = [[ToT],data_type]

            if data_type == 48: #0x30
                if time_unit == 0:
                    ToA, = p.unpack(f.read(4))
                    ToT, = r.unpack(f.read(2))
                if time_unit == 1:
                    ToA, = t.unpack(f.read(4))
                    ToT, = t.unpack(f.read(4))

                scint[chan_id] = [[ToA, ToT],data_type]
            #print("ev_num:",ev_num,"chan_id:",chan_id,"data_type:",data_type,"ToA:",ToA,"ToT:",ToT) 
    
            
       # flag_check = b_counts
       # flag_check_comp = ev_size - 13
        #print("flag_check:",flag_check,"flag_check_comp:",flag_check_comp)
       # if flag_check != flag_check_comp:
        #    return -1
        
        return scint

    #Spectro and Timing Mode:
    if acq_mode == 3:
            
        #Event_Header:
        buff = f.read(2)
        if buff == b'':
            return -1
        ev_size, = r.unpack(buff)
                
        buff2 = f.read(1)
        if buff2 == b'':
            return -1
        board_id, = q.unpack(buff2)

        buff3 = f.read(8)
        if buff3 == b'':
            return -1
        trig_timestamp, = u.unpack(buff3)

        trig_id, = s.unpack(f.read(8))
        chan_mask, = s.unpack(f.read(8))

        #Event_Data: Need to verify this further ....
        #dim = (ev_size - 27) / 16 #hard_coded for the LSB Mode only
        for i in range(64):
            chan_id, = q.unpack(f.read(1))
            data_type, = q.unpack(f.read(1))
            if data_type == 1:
                LG_PHA, = r.unpack(f.read(2))    
                scint[chan_id] = [[LG_PHA], data_type]
            
            if data_type == 2:
                HG_PHA, = r.unpack(f.read(2))
                scint[chan_id] = [[HG_PHA], data_type]
                
            if data_type == 3:
                LG_PHA, = r.unpack(f.read(2))
                HG_PHA, = r.unpack(f.read(2))
                scint[chan_id] = [[LG_PHA, HG_PHA], data_type]
                
            if data_type == 16: #0x10
                if time_unit == 0:
                    ToA, = p.unpack(f.read(4))               
                if time_unit == 1:
                    ToA, = t.unpack(f.read(4))
                scint[chan_id] = [[ToA], data_type]
                
            if data_type == 32: #0x20
                if time_unit == 0:
                    ToT, = r.unpack(f.read(2))
                if time_unit == 1:
                    ToT, = t.unpack(f.read(4))
                scint[chan_id] = [[ToT], data_type]
                
            if data_type == 17: #0x11
                LG_PHA, = r.unpack(f.read(2))
                if time_unit == 0:
                    ToA, = p.unpack(f.read(4))
                if time_unit == 1:
                    ToA, = t.unpack(f.read(4))
                scint[chan_id] = [[LG_PHA, ToA], data_type]

            if data_type == 18: #0x12
                HG_PHA, = r.unpack(f.read(2))
                if time_unit == 0:
                    ToA, = p.unpack(f.read(4))
                if time_unit == 1:
                    ToA, = t.unpack(f.read(4))
                scint[chan_id] = [[HG_PHA, ToA], data_type]
                
                  
            if data_type == 19: #0x13
                LG_PHA, = r.unpack(f.read(2))
                HG_PHA, = r.unpack(f.read(2))
                if time_unit == 0:
                    ToA, = p.unpack(f.read(4))
                if time_unit == 1:
                    ToA, = t.unpack(f.read(4))
                scint[chan_id] = [[LG_PHA, HG_PHA, ToA], data_type]
                   
            if data_type == 33: #0x21
                LG_PHA, = r.unpack(f.read(2))
                if time_unit == 0:
                    ToT, = r.unpack(f.read(2))
                if time_unit == 1:
                    ToT, = t.unpack(f.read(4))
                scint[chan_id] = [[LG_PHA, ToT], data_type]

            
            if data_type == 34: #0x22
                HG_PHA, = r.unpack(f.read(2))
                if time_unit == 0:
                    ToT, = r.unpack(f.read(2))
                if time_unit == 1:
                    ToT, = t.unpack(f.read(4))
                scint[chan_id] = [[HG_PHA, ToT], data_type]
            
           
            if data_type == 35: #0x23
                LG_PHA, = r.unpack(f.read(2))
                HG_PHA, = r.unpack(f.read(2))
                if time_unit == 0:
                    ToT, = r.unpack(f.read(2))
                if time_unit == 1:
                    ToT, = t.unpack(f.read(4))
                scint[chan_id] = [[LG_PHA, HG_PHA, ToT], data_type]     

            if data_type == 48: #0x30
                if time_unit == 0:
                    ToA, = p.unpack(f.read(4))
                    ToT, = r.unpack(f.read(2))
                if time_unit == 1:
                    ToA, = t.unpack(f.read(4))
                    ToT, = t.unpack(f.read(4))
                scint[chan_id] = [[ToA, ToT], data_type]
            
            if data_type == 49: #0x31
                LG_PHA, = r.unpack(f.read(2))
                if time_unit == 0:
                    ToA, = p.unpack(f.read(4))
                    ToT, = r.unpack(f.read(2))
                if time_unit == 1:
                    ToA, = t.unpack(f.read(4))
                    ToT, = t.unpack(f.read(4))
                scint[chan_id] = [[LG_PHA, ToA, ToT], data_type]
            
            if data_type == 50: #0x32
                HG_PHA, = r.unpack(f.read(2))
                if time_unit == 0:
                    ToA, = p.unpack(f.read(4))
                    ToT, = r.unpack(f.read(2))
                if time_unit == 1:
                    ToA, = t.unpack(f.read(4))
                    ToT, = t.unpack(f.read(4))
                scint[chan_id] = [[HG_PHA, ToA, ToT], data_type]
            
            if data_type == 51: #0x33
                LG_PHA, = r.unpack(f.read(2))
                HG_PHA, = r.unpack(f.read(2))
                if time_unit == 0:
                    ToA, = p.unpack(f.read(4))
                    ToT, = r.unpack(f.read(2))
                if time_unit == 1:
                    ToA, = t.unpack(f.read(4))
                    ToT, = t.unpack(f.read(4))
                scint[chan_id] = [[LG_PHA, HG_PHA, ToA, ToT], data_type]

        return scint

    #Counting Mode:
    if acq_mode == 4:
                
        #Event_Header:
        buff = f.read(2)
        if buff == b'':
            return -1
        ev_size, = r.unpack(buff)

        buff2 = f.read(1)
        if buff2 == b'':
            return -1
        board_id, = q.unpack(buff2)

        buff3 = f.read(8)
        if buff3 == b'':
            return -1
        trig_timestamp, = u.unpack(buff3)

        trig_id, = s.unpack(f.read(8))
        chan_mask, = s.unpack(f.read(8))

        #dim = (ev_size - 27) / 5
                    
        #Event_Data:
        for i in range(64):
            chan_id, = q.unpack(f.read(1))
            counts, = p.unpack(f.read(4))

            scint[chan_id] = counts

        return scint


if __name__ == "__main__":
    import sys
    import matplotlib.pyplot as plt
    import matplotlib.ticker as tck

    #Below is the example of the use of module above:
    filein = sys.argv[1]
    
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
    plt.rcParams['figure.dpi'] = 200
    
    #Open the raw data:
    with open(filein, mode='rb') as fin:
        
        #Retrieve an acquisition mode:
        acq_mode,time_unit = dt5202_headerfile(fin)
        
        
        ToA = []
        ToT = []
        #Iterate over event data:
        while(1):
            #Retrieve event data
            temp = dt5202_event(fin, acq_mode, time_unit)
            if temp ==  -1:
                break
            else:
                if temp[4][1] == 16:
                    ToA.append(temp[4][0][0])
                if temp[4][1] == 32:
                    ToT.append(temp[4][0][0])
                if temp[4][1] == 48:
                    ToA.append(temp[4][0][0])
                    ToT.append(temp[4][0][1])


        fig, ax=plt.subplots(1,2)
        ax[0].hist(ToA, bins=200,label='ToA')
        ax[1].hist(ToT, bins=200,label='ToT')

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


