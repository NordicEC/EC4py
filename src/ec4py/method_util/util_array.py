""" 
utility array
"""
from __future__ import annotations
#import math
#import numpy as np
#from scipy import integrate
#from scipy.signal import savgol_filter 

#import copy

from ..ec_setup import EC_Setup
#from ..util import extract_value_unit     
from ..util import Quantity_Value_Unit as QV

#from ..util_graph import plot_options,quantity_plot_fix, make_plot_2x,make_plot_1x, ANALYSE_PLOT, DATA_PLOT,NO_PLOT


import copy


class EC_Array_class:
    """
    Class for handling arrays of data. 
    
    This class is used to handle arrays of data and perform operations on them.
    """
    def __init__(self, *args, **kwargs):
        self.datas= []
        #print('AAAA')
        
        
    def __len__(self):
        return len(self.datas)
    
    def __getitem__(self, index_or_str:slice|int|list[str]|str):
        index = -1

        if isinstance(index_or_str, slice):
            step = 1
            start = 0
            stop = len(self.datas)
            if index_or_str.step:
                step =  index_or_str.step
            if index_or_str.start:
                start = index_or_str.start
            if index_or_str.stop:
                stop = index_or_str.stop  
            new_self= self.copy() 

            new_self.datas =  [self.datas[i] for i in range(start, stop, step)  ]
            return new_self
        elif isinstance(index_or_str,list):
            d =[]
            for x in index_or_str:
                if isinstance(x,int):
                    i =int(x)
                    d.append(self.datas[i])
                elif isinstance(x,str):
                    s = str(index_or_str)
                    for i, data in enumerate(self.datas):
                        if hasattr(data, "setup_data"):
                            if str(data.setup_data.fileName).casefold() == s.casefold():  
                                d.append(data)
                            break

                else:
                    pass
            new_self= self.copy() 
            new_self.datas = d
            return new_self

        elif isinstance(index_or_str,str):
            sindex = index_or_str
            for value, data in enumerate(self.datas):
                if str(data.setup_data.fileName).casefold() == sindex.casefold():
                    index = value
            return self.datas[index]
        else:
            index = int(index_or_str)
            

        return self.datas[index]    
    
    def __setitem__(self, index, value):    
        self.datas[index] = value   
        
    def __delitem__(self, index):
        del self.datas[index]   
        
    def __iter__(self):
        return iter(self.datas)
    
    def __contains__(self, item):
        return item in self.datas   
    
    def __str__(self):
        return "string rep of class to be made"
    
    def __repr__(self):
        delimiter = "','"
        r =delimiter.join([x.setup_data.fileName for x in self.datas])
        return f"{self.__class__.__name__}([{r}])"
    
    def pop(self,index):
        """_summary_
        Remove and return item at index (default last).

        Raises IndexError if list is empty or index is out of range
        """
        self.datas.pop(index)

    def _append(self, item):
        """_summary_
        Append an item to the array.
        """
        if isinstance(item, EC_Array_class):
            for x in item.datas:
                self.datas.append(x)
        elif isinstance(item, EC_Setup):
            self.datas.append(item)
        else:
            raise TypeError('type not supported')
    
        
    def append(self, item):
        """_summary_
        Append an item to the array.
        """
        self.datas.append(item)

    def copy(self):
        '''Creates a deep copy of self.'''
        return copy.deepcopy(self)
    
    @property
    def rate(self):
        rate:list[QV]=[]
        for x in self.datas:
            if hasattr(x,'rate'):
                rate.append(x.rate)
            else:
                rate.append(QV(float('nan')))
        return rate

    @property
    def rotation(self):
        rotation:list[QV]=[]
        for x in self.datas:
            if hasattr(x,'rotation'):
                rotation.append(x.rotation)
            else:
                rotation.append(QV(float('nan')))
        return rotation


        
        



