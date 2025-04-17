import numpy as np

from .ec_data_util import EC_Channels
from .ec_data   import EC_Data


def get_Impedance(ec_data:EC_Data,sel_channels:EC_Channels):
    data_E,q,u,dt_x = ec_data.get_channel(sel_channels.Voltage)
    data_Z,q,u,dt_Z = ec_data.get_channel(sel_channels.Impedance)
    data_phase,q,u,dt_p = ec_data.get_channel(sel_channels.Phase)

    if(len(data_E)!=len(data_Z)):
        data_t,q,u,dt_t = ec_data.get_channel("Time")
        data_t_z =dt_Z*np.array(range(len(data_Z)))
        data_Z = np.interp(data_t, data_t_z, data_Z)
        data_phase = np.interp(data_t, data_t_z, data_phase)

    return data_Z, data_phase


def get_data_for_convert(ec_data:EC_Data,sel_channels:EC_Channels,*args, **kwargs):
    
    ir_comp = False
    try:
        data_E,q,u,dt_x = ec_data.get_channel(sel_channels.Voltage)
        data_i,q,u,dt_y = ec_data.get_channel(sel_channels.Current)
    except NameError as e:
        print(e)
        raise NameError(e)
        return
    
    try:
        comp = kwargs.get("IRCORR",None)
        if comp is not None:
            s_comp=str(comp).casefold()
            #vertex =find_vertex(data_E)
            if  s_comp == "Z".casefold():
                #data_Z,q,u,dt_Z = ec_data.get_channel(sel_channels.Impedance)
                data_Z,_ = get_Impedance(ec_data,sel_channels)
              
                data_IR = data_i*data_Z
                ir_comp =True
                r_comp=[np.min(data_Z),np.max(data_Z)]
            elif  s_comp == "R".casefold():
                data_Z,q,u,dt_Z = ec_data.get_channel(sel_channels.Impedance)
                data_phase,q,u,dt_p = ec_data.get_channel(sel_channels.Phase)
                if(len(data_E)!=len(data_Z)):
                    data_t,q,u,dt_t = ec_data.get_channel("Time")
                    data_t_z =dt_Z*np.array(range(len(data_Z)))
                    data_Z = np.interp(data_t, data_t_z, data_Z)
                    data_phase = np.interp(data_t, data_t_z, data_phase)
                R = data_Z*np.cos(data_phase)
                data_E = data_E - data_i*R
                ir_comp =True
                r_comp=[np.min(R),np.max(R)]
            elif s_comp == "Rmed".casefold():
                data_Z,q,u,dt_Z = ec_data.get_channel(sel_channels.Impedance)
                data_phase,q,u,dt_p = ec_data.get_channel(sel_channels.Phase)
                r_comp = np.median(data_Z*np.cos(data_phase))
                print("Rmed",r_comp)
                data_E = data_E - data_i*r_comp
                ir_comp =True
            elif s_comp == "Zmed".casefold():
                data_Z,q,u,dt_Z = ec_data.get_channel(sel_channels.Impedance)
                r_comp = np.median(data_Z)
                data_E = data_E - data_i*r_comp
                ir_comp =True
                

            else:
                try:
                    Rsol = float(comp)
                    if Rsol > 0:
                        ir_comp =True
                        r_comp = Rsol
                        data_E = data_E - data_i*r_comp
                except ValueError as e:
                    print(e)
                    raise ValueError("Invalid value for IRCORR")
                    return
            


