#import math
import numpy as np
from io import StringIO

#import matplotlib.pyplot as plt
from pathlib import Path


from .ec_data_util import ENUM_Channel_Names
from .ec_data_base import EC_Data_Base
#from ..ec_setup import EC_Setup



def _parse_category(s:str,category:str):
   b =s.split(f"[{category}]")
   c= b[1].split("\n[")
   return c[0]

def _category_to_dict(s:str):
   lines =s.strip().splitlines()
   a= dict()
   for line in lines:
      items = line.strip().split("\t")
      if len(items)>1:
         a[items[0]]=items[1]
      else:
         a[items[0]]=None
   return a

def _parse_data_header(s:str):
   h =s.strip().split("\n",maxsplit=2)
   header =h[0].split("\t")
   d =s.split(h[0] )
   data=d[1].strip()
   #print(len(h))
   #if len(h)>1:
   #   data = h[1]
   #print("header",header)
   quantity=[]
   unit = []
   for h in header:
      q = h.split("(")
      if len(q)>1:
         u = q[1].split(")")
         unit.append(u[0])
      else:
         unit.append("")
      quantity.append(q[0])
   return data, quantity, unit


def _parse_data(s:str):
   s_dataHeader =_parse_category(s,"DATA")
   s_data, quantity, unit = _parse_data_header(s_dataHeader)
   #print("s_data\n",s_data)
   data_io = StringIO(s_data.lstrip())
   #print(s_data.lstrip())
   d=np.genfromtxt(data_io, delimiter= "\t", skip_header=0, skip_footer=0)
   rawdata=dict()
   for i,h in enumerate(quantity):
      rawdata[h]= d[:,i]
   return rawdata, quantity, unit


class EC_Data_TXT(EC_Data_Base):
   def __init__(self, path=""):
      super().__init__(self)
      if path == "":
         # print("no path")
         return
      else:
         _s_load_txt()



def load_EC_file_TDMS(ec_data:EC_Data_Base,path:Path):
   s = None
   with open(path,"r") as file:
      s = file.read()
      file.close()
   _s_load_txt(ec_data,s)
##################################################################
def _s_load_txt(ec_data:EC_Data_Base,s):

   d_info = dict()
   d_common =_category_to_dict(_parse_category(s,"COMMON"))
   d_method =_category_to_dict(_parse_category(s,"METHOD"))
   d_pot_settings =_category_to_dict(_parse_category(s,"POT_SETTINGS"))
   for cat in [d_common,d_method,d_pot_settings]:
      for key in cat.keys():
         d_info[key]= cat[key]
   #print(d_info)
   for key in d_info.keys():
      ec_data.setup_data._setup[key] = d_info[key]
   ec_data.setup_reset()

   #ec_data.setup
   ec_data.rawdata, ec_data._channelNames, ec_data._units =_parse_data(s)
   ec_data._quantities = ec_data._channelNames
   for i,x in enumerate(ec_data._channelNames):
      #print(x)
      ch_name = x.casefold()
      if ch_name == ENUM_Channel_Names.E.casefold():
         ec_data.E = ec_data.rawdata[x]
         #print("EEEE")
      elif ch_name == ENUM_Channel_Names.i.casefold():
         ec_data.i = ec_data.rawdata[x]
      elif ch_name == ENUM_Channel_Names.Time.casefold():
         ec_data.Time = ec_data.rawdata[x]
   
   return




   
                  