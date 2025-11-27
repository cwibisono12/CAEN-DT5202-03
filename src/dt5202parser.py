#!/usr/bin/env python3

from struct import *

def dt5202file(filename):
    '''
    Original CAEN_DT5202 Binary Data Format
    C. Wibisono
    11/14 '25
    Usage:
    To parse the .dat file coming from the Janus DAQ CAEN-DT5202
    '''

        
    with open(filename, mode='rb') as f:

        p = Struct("@I") #Unsigned Integer (4 bytes)
        q = Struct("@B") #Unsigned char (1 bytes)
        r = Struct("@H") #Unsigned short (2 bytes)
        s = Struct("@Q") #Unsigned long long (8 bytes)
        t = Struct("@f") #float (4 bytes)
        u = Struct("@d") #double (8 bytes)

        #File Header:
        data_format, = r.unpack(f.read(2))
        f.read(3)
        board_type, = r.unpack(f.read(2))
        run_num, = r.unpack(f.read(2))
        acq_mode, = q.unpack(f.read(1))
        en_channels, = r.unpack(f.read(2))
        time_unit, = q.unpack(f.read(1))
        time_conv, = t.unpack(f.read(4))
        start_acq, = s.unpack(f.read(8))

        print("data_format:",data_format,"board_type:",board_type)
        print("run_num:",run_num,"acq_mode:",acq_mode)
        print("en_channel:",en_channels,"time_unit:",time_unit)
        print("time_conv:",time_conv,"start_acq:",start_acq)


        #Data: (each list mode consists of event header and event itself)
        ev_num = 0
        
        #Spectroscopy mode:
        if acq_mode == 1:
            #for i in range(6700):
            while(1):
                #Event_Header:
                buff = f.read(2)
                if buff == b'':
                    return 1
                ev_size, = r.unpack(buff)

                buff2 = f.read(1)
                if buff2 == b'':
                    return 1
                board_id, = q.unpack(buff2)

                buff3 = f.read(8)
                if buff3 == b'':
                    return 1
                trig_timestamp, = u.unpack(buff3)

                trig_id, = s.unpack(f.read(8))
                chan_mask, = s.unpack(f.read(8))
                
                dim = int((ev_size - 27) / 6)

                #Event_Data:
                ev_num = ev_num + 1
                for k in range(dim):
                    chan_id, = q.unpack(f.read(1))
                    data_type, = q.unpack(f.read(1))
                    if data_type == 1:
                        LG_PHA, = r.unpack(f.read(2))
                    if data_type == 2:
                        HG_PHA, = r.unpack(f.read(2))
                    if data_type == 3:
                        LG_PHA, = r.unpack(f.read(2))
                        HG_PHA, = r.unpack(f.read(2))
                    
                    print("ev_num:",ev_num, "chan_id:", chan_id, "data_type:", data_type, "LG_PHA:", LG_PHA, "HG_PHA:", HG_PHA)
                



        #Timing Mode:
        if acq_mode == 2:
            while(1):
                #Event_Header:
                b_counts = 0
                buff = f.read(2)
                if buff == b'':
                    return 1
                ev_size, = r.unpack(buff)
            
                buff2 = f.read(1)
                if buff2 == b'':
                    return 1
                board_id, = q.unpack(buff2)

                buff3 = f.read(8)
                if buff3 == b'':
                    return 1
                tref, = u.unpack(buff3)

                num_hits, = r.unpack(f.read(2))
                ev_num = ev_num + 1
                print("ev_size:",ev_size,"board_id:",board_id,"tref:",tref,"num_hits:",num_hits)
                
                #Iterate for each event as many as num_hits:
                for i in range(num_hits):
                    chan_id, = q.unpack(f.read(1))
                    data_type, = q.unpack(f.read(1))
                    #b_counts = b_counts+2
                    if data_type == 16: #0x10
                        if time_unit == 0:
                            ToA, = p.unpack(f.read(4))
                        #    ToT, = r.unpack(f.read(2))
                      #  b_counts = b_counts + 6
                        if time_unit == 1:
                            ToA, = t.unpack(f.read(4))
                         #   ToT, = t.unpack(f.read(4))
                       # b_counts = b_counts + 8
                        print("ev_num:",ev_num,"chan_id:",chan_id,"data_type:",data_type,"ToA:",ToA)

                    if data_type == 32: #0x20
                        if time_unit == 0:
                            ToT, = r.unpack(f.read(2))
                        if time_unit == 1:
                            ToT, = t.unpack(f.read(4))
                        print("ev_num:",ev_num,"chan_id:",chan_id,"data_type:",data_type,"ToT:",ToT) 

                    if data_type == 48: #0x30
                        if time_unit == 0:
                            ToA, = p.unpack(f.read(4))
                            ToT, = r.unpack(f.read(2))
                        if time_unit == 1:
                            ToA, = p.unpack(f.read(4))
                            ToT, = t.unpack(f.read(4))

                        print("ev_num:",ev_num,"chan_id:",chan_id,"data_type:",data_type,"ToA:",ToA,"ToT:",ToT) 
    
            
                #flag_check = b_counts
                #flag_check_comp = ev_size - 13
                #print("flag_check:",flag_check,"flag_check_comp:",flag_check_comp)
                #if flag_check != flag_check_comp:
                 #   break
            

        #Spectro and Timing Mode:
        if acq_mode == 3:
            #for i in range(20):
            while(1):
                #Event_Header:
                buff = f.read(2)
                if buff == b'':
                    break
                ev_size, = r.unpack(buff)
                
                buff2 = f.read(1)
                if buff2 == b'':
                    break
                board_id, = q.unpack(buff2)

                buff3 = f.read(8)
                if buff3 == b'':
                    break
                trig_timestamp, = u.unpack(buff3)

                trig_id, = s.unpack(f.read(8))
                chan_mask, = s.unpack(f.read(8))

                ev_num = ev_num + 1
                #Event_Data: Need to verify this further ....
                #dim = int((ev_size - 27) / 16) #hard_coded for the LSB Mode only
                
                
                #Looks like in this mode, iteration is done with the number of channels for each board
                #Independent with the DAQ parameters.
                for i in range(64):
                    chan_id, = q.unpack(f.read(1))
                    data_type, = q.unpack(f.read(1))


                    if data_type == 1:
                        LG_PHA, = r.unpack(f.read(2))
                    
                    if data_type == 2:
                        HG_PHA, = r.unpack(f.read(2))

                    if data_type == 3:
                        LG_PHA, = r.unpack(f.read(2))
                        HG_PHA, = r.unpack(f.read(2))
                 
                    if data_type == 16: #0x10
                        if time_unit == 0:
                            ToA, = p.unpack(f.read(4))
                        if time_unit == 1:
                            ToA, = t.unpack(f.read(4))
                    if data_type == 32: #0x20
                        if time_unit == 0:
                            ToT, = r.unpack(f.read(2))
                        if time_unit == 1:
                            ToT, = t.unpack(f.read(4))

                    if data_type == 17: #0x11
                        LG_PHA, = r.unpack(f.read(2))
                        if time_unit == 0:
                            ToA, = p.unpack(f.read(4))
                        if time_unit == 1:
                            ToA, = t.unpack(f.read(4))


                    if data_type == 18: #0x12
                        HG_PHA, = r.unpack(f.read(2))
                        if time_unit == 0:
                            ToA, = p.unpack(f.read(4))
                        if time_unit == 1:
                            ToA, = t.unpack(f.read(4))

                    if data_type == 19: #0x13
                        LG_PHA, = r.unpack(f.read(2))
                        HG_PHA, = r.unpack(f.read(2))
                        if time_unit == 0:
                            ToA, = p.unpack(f.read(4))
                        if time_unit == 1:
                            ToA, = t.unpack(f.read(4))

                    if data_type == 33: #0x21
                        LG_PHA, = r.unpack(f.read(2))
                        if time_unit == 0:
                            ToT, = r.unpack(f.read(2))
                        if time_unit == 1:
                            ToT, = t.unpack(f.read(4))
                        
                    if data_type == 34: #0x22
                        HG_PHA, = r.unpack(f.read(2))
                        if time_unit == 0:
                            ToT, = r.unpack(f.read(2))
                        if time_unit == 1:
                            ToT, = t.unpack(f.read(4))

                    if data_type == 35: #0x23
                        LG_PHA, = r.unpack(f.read(2))
                        HG_PHA, = r.unpack(f.read(2))
                        if time_unit == 0:
                            ToT, = r.unpack(f.read(2))
                        if time_unit == 1:
                            ToT, = t.unpack(f.read(4))

                    if data_type == 48: #0x30
                        if time_unit == 0:
                            ToA, = p.unpack(f.read(4))
                            ToT, = r.unpack(f.read(2))
                        if time_unit == 1:
                            ToA, = t.unpack(f.read(4))
                            ToT, = t.unpack(f.read(4))

                    if data_type == 49: #0x31
                        LG_PHA, = r.unpack(f.read(2))
                        if time_unit == 0:
                            ToA, = p.unpack(f.read(4))
                            ToT, = r.unpack(f.read(2))
                        if time_unit == 1:
                            ToA, = t.unpack(f.read(4))
                            ToT, = t.unpack(f.read(4))
                    
                    if data_type == 50: #0x32
                        HG_PHA, = r.unpack(f.read(2))
                        if time_unit == 0:
                            ToA, = p.unpack(f.read(4))
                            ToT, = r.unpack(f.read(2))
                        if time_unit == 1:
                            ToA, = t.unpack(f.read(4))
                            ToT, = t.unpack(f.read(4))


                    if data_type == 51: #0x33
                        LG_PHA, = r.unpack(f.read(2))
                        HG_PHA, = r.unpack(f.read(2))
                        if time_unit == 0:
                            ToA, = p.unpack(f.read(4))
                            ToT, = r.unpack(f.read(2))
                        if time_unit == 1:
                            ToA, = t.unpack(f.read(4))
                            ToT, = t.unpack(f.read(4))

                   # else:
                    #    continue
                    #if data_type != 3: 
                    print("ev_num:",ev_num,"chan_id:",chan_id,"data_type:",data_type) 
           

        #Counting Mode:
        if acq_mode == 4:
            while(1):
                #Event_Header:
                buff = f.read(2)
                if buff == b'':
                    break
                ev_size, = r.unpack(buff)

                buff2 = f.read(1)
                if buff2 == b'':
                    break
                board_id, = q.unpack(buff2)

                buff3 = f.read(8)
                if buff3 == b'':
                    break
                trig_timestamp, = u.unpack(buff3)

                trig_id, = s.unpack(f.read(8))
                chan_mask, = s.unpack(f.read(8))

                #dim = int((ev_size - 27) / 5)
                #Event_Data:
                ev_num = ev_num + 1
                for i in range(64):
                    chan_id, = q.unpack(f.read(1))
                    counts, = p.unpack(f.read(4))

                    print("ev_num:",ev_num,"chan_id:",chan_id,"counts:",counts)

if __name__ == "__main__":
    import sys
    filein = sys.argv[1]
    dt5202file(filein)
