"""
Utility module.

"""

import math
#from scipy.signal import savgol_filter, medfilt
#from scipy import ndimage, datasets
#import matplotlib.pyplot as plt
#from fractions import Fraction
#import copy


def extract_value_unit(s:str):
    """_summary_

    Args:
        s (str): _description_

    Returns:
        value(float): the extracted value 
        unit(str): extract unit
    """
    unit =""
    value = math.nan
    try:
        list = s.strip().split(" ",1)
        value = float(list[0])
        unit = list[1]    
    finally:
        pass
    return value, unit

#######################################################################################
"""
class symbol_string:
    def __init__(self,s:str=""):
        self.symbols = s

    def __str__(self) -> str:
        return self.symbols
    
    def __add__(self, other):
        s = quantity_fix(self.symbols + other.symbols)             
        return symbol_string(s)
    
    def __pow__(self, other):
        s = quantity_fix(self.symbols,other)    
        return symbol_string(s)
"""

class symbols:
    def __init__(self,s:str=None):
        self._sym = {}
        if s:
            list_of_quantities = (s.strip()).split(" ", 100)
            if len(list_of_quantities)>0:
                k={}
                for single_quantity in list_of_quantities:
                    nyckel, exponent = get_unit_and_exponent(single_quantity)
                    val = float(k.get(nyckel, 0))  
                    k[nyckel] = val + exponent
                self._sym = k.copy()
        #print(k)
        
    def __str__(self) -> str:
        sr =""
        for key, value in self._sym.items():
            if  int(value*10) == 0:
                pass
            elif int(value*10) == 10:
                sr = sr +f' {key}'
            elif int(value) == value:
                sr = sr+ f' {key}^{value:.0f}'
            else:
                sr = sr+ f' {key}^{value:.1f}'
        return sr.strip()
    
    def __add__(self, other):
        #s = quantity_fix(self.symbols + other.symbols)             
        if isinstance(other,symbols):
            k=symbols()
            k=self._sym.copy()
            for quantity,exponent in other._sym.items():
                #print("aadd: ",quantity,quantity != "") 
                if quantity != "":
                    val = float(self._sym.get(quantity, 0))
                    k[quantity] = val + exponent
            r = symbols()
            r._sym = k.copy()
            return r
        else:
            raise TypeError("must be of the same type") 
    
    def __sub__(self,other):
        k=symbols()
        k = other*-1
        return (self+k)
    
    def __mul__(self, other):
        if isinstance(other,int) or isinstance(other,float):
            r=symbols()
            k=self._sym.copy()
            for quantity,exponent in self._sym.items():
                #print("q",quantity,quantity != "") 
                if quantity != "":
                    k[quantity] = exponent * other
            r._sym = k.copy()
            return r
        else:
            raise TypeError("must be a float or an int")
    def __eq__(self, other: object) -> bool:
        return str(self) == str(other)

########################################################################################
class Quantity_Value_Unit:
    """A class for quantity calculation.
    
    """
    def __init__(self, value: float | str =0.0 , unit="", quantity=""):
        
        if isinstance(value, str):
            v,u = extract_value_unit(value)
            q = ""
        else:
            v = value
            if isinstance(unit, symbols):
                u = str(unit).strip()
            else:
                u=unit.strip()
            if isinstance(unit, symbols):
                q = str(quantity)
            else:
                q=quantity
        self._unit =symbols(u)
        self._quantity =symbols(q)
        self.value = float(v)
        
    def __str__(self) -> str:
        return f'{self.value:.3e} {self._unit}'
    
    def __float__(self) -> float:
        return self.value
    
    def __add__(self, other: object):
        v = Quantity_Value_Unit()
        if isinstance(other,Quantity_Value_Unit):
            if self.unit == other.unit:       
                return Quantity_Value_Unit(self.value+other.value,str(self._unit), str(self._quantity))
            else:
                raise ValueError("Must have the same unit")
        else:
            raise TypeError("Must be of the same type")
        return v
    
    def __sub__(self, other: object):
        v = Quantity_Value_Unit()
        if isinstance(other,Quantity_Value_Unit):
            if self.unit == other.unit:       
                return Quantity_Value_Unit(self.value-other.value,str(self._unit), str(self._quantity))
            else:
                raise ValueError("Must have the same unit")
        else:
            raise TypeError("Must be of the same type")
        return v
    
    def __mul__(self, other):
        if isinstance(other, Quantity_Value_Unit):
            v= Quantity_Value_Unit(self.value * other.value, (self._unit + other._unit), self._quantity + other._quantity)
        else:
            v= Quantity_Value_Unit(self.value * float(other), self._unit, self._quantity)
        return v
    
    def __div__(self, other):
        if isinstance(other, Quantity_Value_Unit):
            v = Quantity_Value_Unit(self.value / other.value, self._unit - other._unit, self._quantity - other._quantity)
        else: 
            v = Quantity_Value_Unit(self.value / float(other), self._unit, self._quantity)    
        return v
    
    def __truediv__(self, other: object):
        
        if isinstance(other, Quantity_Value_Unit):
            v = Quantity_Value_Unit(self.value / other.value, self._unit - other._unit, self._quantity - other._quantity)
        else:
            v = Quantity_Value_Unit(self.value / float(other), self._unit, self._quantity) 
        return v
    
    def __pow__(self, other:int|float):
        if isinstance(other, float) or isinstance(other, int):
            return Quantity_Value_Unit( self.value ** float(other), self._unit*other, self._quantity*other)
        else:
            raise TypeError("Must be a number, i.e. float or int")
            return
        
    @property
    def unit(self):
        return str(self._unit)
    
    @property
    def quantity(self):
        return str(self._quantity)

def get_unit_and_exponent(s:str):
    aa = s.split("^",2)
    nyckel = aa[0].strip()
    sign = 1
    fac =  1.0
    if nyckel.startswith("/"):
        nyckel = nyckel[1:]
        sign = -1
    if len(aa)>1:                   #if "^" was found.
        fac = float(aa[1]) 
    return nyckel, sign*fac

    
def quantity_fix(s:str, factor:float = 1):
    list_of_quantities = s.split(" ", 100)
    k={}
    for single_quantity in list_of_quantities:
        nyckel, exponent = get_unit_and_exponent(single_quantity)
        val = float(k.get(nyckel, 0))  
        k[nyckel] = val + exponent
    prep={} 
    for key, value in k.items():
        if int(value*100) != 0:
            prep[key] = value * factor
    sr =""
    #print ("quantity_fix:",prep)  
    for key, value in prep.items():
        if int(value*10) == 10:
            sr = sr +" " + key
        elif int(value) == value:
            sr = sr+ f' {key}^{value:.0f}'
        else:
            sr = sr+ f' {key}^{value:.1f}'
    return sr.strip()

###################################
