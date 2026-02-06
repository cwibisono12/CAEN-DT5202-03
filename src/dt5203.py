#!/usr/bin/env python3

from struct import *

def dt5203_headerfile(fpr):
    '''
    Original CAEN_DT5203 Binary Data Format
    C. Wibisono
    02/06 '26
    
    Usage:
    To parse the header .dat file coming from the Janus DAQ CAEN-DT5203 
    and retrieve the acquisition mode for each file.

    Parameter(s):
    fpr: file pointer object
    Return(s):
    acq_mode: (int) acquisiton mode
    time_unit: (int) time unit (0) means the least significant bit (LSB), (1) means ns
    meas_mode: (int) measurement mode (1: LEAD_ONLY, 3: LEAD_TRAIL, 5: LEAD_TOT8, 9: LEAD_TOT11)
    '''
    
    p = Struct("@I") #Unsigned Integer (4 bytes)
    q = Struct("@B") #Unsigned char (1 bytes)
    r = Struct("@H") #Unsigned short (2 bytes)
    s = Struct("@Q") #Unsigned long long (8 bytes)
    t = Struct("@f") #float (4 bytes)
    u = Struct("@d") #double (8 bytes)

    #File Header:
    data_format, = r.unpack(fpr.read(2))
    software_ver, = fpr.read(3)
    FERS_ver, = r.unpack(fpr.read(2))
    run_num, = r.unpack(fpr.read(2))
    acq_mode, = r.unpack(fpr.read(2))
    meas_mode, = q.unpack(fpr.read(1))
    time_unit, = q.unpack(fpr.read(1))
    ToA_LSB, = t.unpack(fpr.read(4))
    ToT_LSB, = t.unpack(fpr.read(4))
    tstamp_LSB, = t.unpack(fpr.read(4))
    start_run, = s.unpack(fpr.read(8))


    print("data_format:",data_format)
    print("run_num:",run_num,"acq_mode:",acq_mode)
    print("measurement_mode:",meas_mode,"time_unit:",time_unit)
    print("ToA_LSB_value:",ToA_LSB,,"ToT_LSB_value::",ToT_LSB)
    print("Timestamp_LSB_value:",tstamp_LSB)

    return acq_mode, time_unit, meas_mode


def dt5203_event(f, acq_mode, time_unit, meas_mode):
    '''
    Original CAEN_DT5203 Binary Data Format
    C. Wibisono
    02/06 '26
    
    Usage: 
    To parse the event .dat file coming from the Janus DAQ CAEN-DT5203
    and return a data object
    Parameter(s):
    f: file pointer object
    acq_mode: acquisition_mode
    time_unit: time_unit
    meas_mode: measurement mode

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

    #Common Start/Stop mode: (for relative measurement mode only)
    if acq_mode == 2 or acq_mode == 18: #2: Common Start Mode; 18: Common Stop Mode
        
        #Event_Header:
        buff = f.read(2)
        if buff == b'':
            return -1
        
        ev_size, = r.unpack(buff)
        if time_unit == 0:
            trig_tstamp, = s.unpack(f.read(8))
        if time_unit == 1:
            trig_tstamp, = u.unpack(f.read(8))

        trig_id, = s.unpack(f.read(8))
        num_hits, = r.unpack(f.read(2))
        
        #iterate over the number of hits:
        for i in range(num_hits):
            board_id, = q.unpack(f.read(1))
            chan_id, = q.unpack(f.read(1))
            
            if time_unit == 0:
                ToA, = p.unpack(f.read(4))
                if meas_mode != 1:
                    ToT, = r.unpack(f.read(2))
            if time_unit == 1:
                ToA, = t.unpack(f.read(4))
                if meas_mode != 1:
                    ToT, = t.unpack(f.read(4))

            if meas_mode != 1:
                scint[chan_id] = [[ToA, ToT], meas_mode, acq_mode]
            else:
                scint[chan_id] = [[ToA], meas_mode, acq_mode]

        return scint



    #Trigger Matching Mode: (works for all mesaurement modes)
    if acq_mode == 50: #0x32
    
        #Event_Header:
        buff = f.read(2)
        if buff == b'':
            return -1
        
        ev_size, = r.unpack(buff)
        if time_unit == 0:
            trig_tstamp, = s.unpack(f.read(8))
        if time_unit == 1:
            trig_tstamp, = u.unpack(f.read(8))

        trig_id, = s.unpack(f.read(8))
        num_hits, = r.unpack(f.read(2))
        
        for i in range(num_hits):
            board_id, = q.unpack(f.read(1))
            chan_id, = q.unpack(f.read(1))
            edge, = q.unpack(f.read(1)) #0 = the time of arrival (ToA) uses the trailing edge; 1 = ToA uses the leading edge.
            if time_unit == 0:
                ToA, = p.unpack(f.read(4))
                if meas_mode != 1:
                    ToT, = r.unpack(f.read(2))
            if time_unit == 1:
                ToA, = t.unpack(f.read(4))
                if meas_mode != 1:
                    ToT, = t.unpack(f.read(4))


            if meas_mode != 1:
                scint[chan_id] = [[ToA, ToT], meas_mode, edge, acq_mode]
            else:
                scint[chan_id] = [[ToA], edge, meas_mode, edge, acq_mode]


        return scint

    #Streaming Mode: (works for all measurement modes)
    if acq_mode == 34: #0x22
            
        #Event_Header:
        buff = f.read(2)
        if buff == b'':
            return -1
        ev_size, = r.unpack(buff)
                
        if time_unit == 0:
            trig_tstamp, = s.unpack(f.read(8))
        if time_unit == 1:
            trig_tstamp, = u.unpack(f.read(8))

        num_hits, = r.unpack(f.read(2))

        for i in range(num_hits):
            board_id, = q.unpack(f.read(1))
            chan_id, = q.unpack(f.read(1))
            edge, = q.unpack(f.read(1)) #0 = the time of arrival (ToA) uses the trailing edge; 1 = ToA uses the leading edge.
            if time_unit == 0:
                ToA, = p.unpack(f.read(4))
                if meas_mode == 1:
                    ToT, = r.unpack(f.read(2))
            if time_unit == 1:
                ToA, = t.unpack(f.read(4))
                if meas_mode == 1:
                    ToT, = t.unpack(f.read(4))


            if meas_mode == 1:
                scint[chan_id] = [[ToA, ToT], meas_mode, edge, acq_mode]
            else:
                scint[chan_id] = [[ToA], edge, meas_mode, edge, acq_mode]
            
        return scint



