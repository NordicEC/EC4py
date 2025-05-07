#from .ec_data_util import EC_Channels,ENUM_Channel_Names
from .ec_data_base import EC_Data_Base
#from ..ec_setup import EC_Setup
from nptdms import TdmsFile
from pathlib import Path


def help_get_wf_prop(rawdata, datachannel: str):
    if rawdata is not None:
        unit = str(rawdata[datachannel].properties.get("unit_string", ""))
        quantity = str(rawdata[datachannel].properties.get("Quantity", ""))
        dT = rawdata[datachannel].properties.get("wf_increment", 1)
    else:
        unit = "No channel"
        quantity = "No channel"
        dT = 1
    return unit, quantity, dT


def load_EC_file_TDMS(ec_data:EC_Data_Base,path:Path):
    try:
        tdms_file = TdmsFile.read(path)
        tdms_file.close()
        ec_data.path = str(path)
        ec_data.setup_data.fileName = Path(path).name
        # print(tdms_file.properties)
        
        _TDMS_add_META(ec_data,tdms_file)

        ec_data.rawdata = tdms_file['EC']
        ################ add channel names
        ec_data._channelNames=list()
        for ch_name in ec_data.rawdata:
                ec_data._channelNames.append(ch_name)
        ################ add channel data
        ec_data.Time = tdms_file['EC']['Time'].data
        try:
            ec_data.i = tdms_file['EC']['i'].data
        except KeyError:
            pass
        
        ec_data.E = tdms_file['EC']['E'].data
        ec_data.setup_data.name = tdms_file.properties['name']
        ec_data.setup_data.dateTime = tdms_file.properties['dateTime']
        try:
            ec_data.Z_E = tdms_file['EC']['Z_E'].data  # not all data file contains U channel
            ec_data.Phase_E = tdms_file['EC']['Phase_E'].data  # not all data file contains U channel
        except KeyError:
            pass
        try:
            ec_data.U = tdms_file['EC']['Ucell'].data  # not all data file contains U channel
        except KeyError:
            pass
        try:
            ec_data.Z_U = tdms_file['EC']['Z_cell'].data  # not all data file contains U channel
            ec_data.Phase_U = tdms_file['EC']['Phase_cell'].data  # not all data file contains U channel
        except KeyError:
            pass
        
        # [self.area, self.setup_data._area_unit] = util.extract_value_unit(self.setup["Electrode.Area"])
        # [self.rotation, self.setup_data.rotation_unit] = util.extract_value_unit(self.setup["Inst.Convection.Speed"])

    except FileNotFoundError:
        print(f"TDMS file was not found: {path}")
    except KeyError as e:
        print(f"TDMS error: {e}")


def _TDMS_add_META(ec_data:EC_Data_Base,tdms_file):
    try:
        Items = tdms_file['Setup']['Item']
        Value = tdms_file['Setup']['Value']
        for x in range(len(Items)):
            ec_data.setup_data._setup[Items[x]] = Value[x]
        ec_data.setup_reset()
    except KeyError:
        pass

