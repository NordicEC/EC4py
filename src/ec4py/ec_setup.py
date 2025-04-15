from .util import extract_value_unit
from .util import Quantity_Value_Unit as QV
import numpy as np
from .util_graph import LEGEND,update_legend
# from .util_graph import Legend as legend_class
import copy

RHE = "RHE"
SHE = "SHE"
AREA = "area"
AREA_CM = "area_cm"
RATE = "rate"
SQRT_RATE = "sqrt_rate"
ROT = "rotation"
SQRT_ROT = "sqrt_rot"
MASS = "mass"
WEIGHT = "mass"
LOADING ="loading"

class ec_setup_data:
        def __init__(self):
            self.name =""
            self.fileName=""
            self._setup = {"Current Range" : "", "Control Mode" : "", "Cell Switch": 0}
            self._area= 1.0
            self._area_unit="m^2"
            self._rotation = 0.0
            self._rotation_unit ="/min"
            self._rate_V_s = 1
            #self._loading = None
            #self._loading_unit ="g/m^2"
            self._Weight = None
            self._Weight_unit ="g"
            self._RHE = None
            self._SHE = None
            self._RE = ""
            self._currentElectrode = 0
            self._MWE_CH = ""
            self.dateTime = np.datetime64('2020-01-01 00:00:01')
            self._batch = None
            self._Serial = None
            self._Support = None
            self._Electrode = None
            self._Serial = None
            self._Support = None
            self._Loading = None
            return

        def get_area(self):
            area = QV(self._area,self._area_unit)
            area.set_quantity("A")
            return area
            
        def get_mass(self):
            if self._Weight is not None:
                self._Weight.set_quantity("m")
            return   self._Weight 
        
        def get_loading(self):
            if self._Loading is not None:
                self._Loading.set_quantity("L")
            return self._Loading

        def setACTIVE_RE(self,ref):
            if ref is RHE:
                self._currentElectrode = 1
            elif ref is SHE:
                self._currentElectrode = 2
            else:
                self._currentElectrode = 0
            # print(ref, self._currentElectrode)
            
        def getACTIVE_RE(self):
            """
            Returns:
                str: the selected reference electrode.
            """
            active_reference_electrode = ""
            if self._currentElectrode == 1:
                active_reference_electrode = RHE
            elif self._currentElectrode == 2:
                active_reference_electrode = SHE
            else:
                active_reference_electrode = self._RE
            return active_reference_electrode
        
        def reset_SWE(self):
                self._Batch = self._setup.get('Electrode.Cat.Batch',"")
                self._Serial = self._setup.get('Electrode.Cat.Serial',"")
                self._Support = self._setup.get('Electrode.Cat.Support',"")
                self._Substrate = self._setup.get('Electrode.Cat.Substrate',"")
                self._Electrode = self._setup.get('Electrode.ExElectrode',"")
                self._Loading = QV(self._setup.get('Electrode.Cat.Loading',""))
                self._Weight = QV(self._setup.get('Electrode.Cat.Weight',""))
                self._totWeight = self._setup.get('Electrode.Cat.totWeight',"")
                self._totWeight = self._setup.get('Electrode.Cat.totWeight',"")
                self._cat_w_ratio = self._setup.get('Electrode.Cat.w%',"")

        def select_MWE_CH(self,ch_number:int):
            if self._setup.get('AddOn',False):
                self._MWE_CH = int(ch_number)
                
                self._batch = self._setup.get('MWE_{ch_number}.Batch',"")
                self._Serial = self._setup.get('MWE_{ch_number}.Serial',"")
                self._Support = self._setup.get('MWE_{ch_number}.Support',"")
                self._Electrode = self._setup.get('MWE_{ch_number}.Electrode',"")
                self._Loading = QV(self._setup.get('MWE_{ch_number}.Loading',""))
                        

class EC_Setup:
    """Describes the setup.
    
    properties:
    
    - area
    - rate
    - rotation
    -loading
    """
    def __init__(self,*args, **kwargs):
        #self._setup.setup = {"Current Range" : "", "Control Mode" : "", "Cell Switch": 0}
        #self._setup._area= 1.0
        #self._setup._area_unit="cm^2"
        #self._setup._rotation = 0.0
        #self._setup_rotation_unit ="/min"
        self.setup_data = ec_setup_data()
        return
    
    def __str__(self):
        """Get the name of the data file.
        """
        return f"{self.setup_data.name}"
    
    
          
    def setup_reset(self):
        if 'Electrode.Area' in self.setup_data._setup:
            v,u = extract_value_unit(self.setup_data._setup['Electrode.Area'])
            self.set_area(v,u)
        if 'Inst.Convection.Speed' in self.setup_data._setup:
            v,u = extract_value_unit(self.setup_data._setup['Inst.Convection.Speed'])
            self.set_rotation(v,u)
        if 'RHE' in self.setup_data._setup:
            self.setup_data._RHE = self.setup_data._setup['RHE']
        if 'SHE' in self.setup_data._setup:
            self.setup_data._SHE = self.setup_data._setup['SHE']
        if 'Ref.Electrode' in self.setup_data._setup:
            self.setup_data._RE = self.setup_data._setup['Ref.Electrode']
            
        self.setup_data.reset_SWE()
    
    
    def copy(self):
        """Creates a copy of self object.

        Returns:
            Copy of the current object.
        """
        return copy.deepcopy(self)
    
    def copy_from(self, source):
        """Imports a copy of EC_Setup from source.

        Args:
            source (EC_Setup): Source.
        """
        self.setup_data = copy.deepcopy(source.setup_data)
    
    
    @property 
    def setup(self):
        """setup meta data

        Returns:
            dict[]: list of key words
        """
        return self.setup_data._setup
        
    @setup.setter
    def setup(self, value):
        self.setup_data._setup = value
    
    ############################################
    ##AREA        
    @property 
    def area(self):
        """Area:
            value (float | str): area value as a number, or a string with the unit.

        Returns:
            area value and unit.
        """
        return self.setup_data.get_area()
        #QV(self.setup_data._area,self.setup_data._area_unit,"A")
        
    @area.setter
    def area(self, value:float| str):
        """setting the area

        Args:
            value (float | str): area value as a number, or a string with the unit.
        """
        raise DeprecationWarning("area is deprecated, use set_area() instead")
        #print("use the function set_area() instead")
    
    def set_area(self,value:float,unit:str = "m^2"):
        """sets the area

        Args:
            value (float): area value as a number
            unit (str, optional): unit of the area. Defaults to "m^2".
        """
        
        self.setup_data._area = QV(value,unit)
        #if unit == "":
        #    pass
        #else:
        #    self.setup_data._area_unit = unit
        return self.setup_data.get_area()
        
    @property 
    def area_unit(self):
        return self.setup_data._area_unit
        
    @area_unit.setter
    def area_unit(self, value:str):
        self.setup_data._area_unit = value

#####################################################
## ROTATION
    @property
    def rotation(self):
        return QV(self.setup_data._rotation,self.setup_data._rotation_unit,"\u03C9") #using GREEK SMALL LETTER OMEGA

    @rotation.setter
    def rotation(self, value:float|str):
        """set the rotation rate

        Args:
            value (float): rotation rate
        """
        if isinstance(value,str):
            val = QV(value)
            self.setup_data._rotation = val.value
            self.setup_data._rotation_unit = val.unit
        else:
            self.setup_data._rotation = value

    @property
    def rotation_unit(self):
        return self.setup_data._rotation_unit

    @rotation_unit.setter
    def rotation_unit(self, value:str):
        """set the rotation rate

        Args:
            value (str): rotation unit
        """
        self.setup_data._rotation_unit = value
    #####################################################
    ###RATE
    @property
    def rate(self):
        """returns the sweep rate in V/s

        Returns:
            float: sweep rate in V/s
        """
        r = self.setup_data._setup.get('Rate',None)
        
        if r is None:
            value = self.setup_data._rate_V_s
            unit = "V /s"
        else:
            value,unit = extract_value_unit(self.setup_data._setup['Rate'])
            unit = "V /s"
        return QV(value,unit,"v")
    ###########################################################
    
    @property
    def weight(self):
        """returns the catalyst weight in g

        Returns:
            float: weight in g
        """
        #v,u = extract_value_unit(self.setup_data._setup['Electrode.Cat.Weight'])
        #return QV(v,u,"m")
        return self.setup_data.get_mass()
    @property
    def mass(self):
        """same as weight function.
        """
        return self.setup_data.get_mass()
    #####################################################
    ###loading
    @property
    def loading(self):
        """returns the catalyst loading in g m^-2

        Returns:
            float: loading in g m^-2
        """
        if self.setup_data._Loading is None:
           print("Loading has not been defined for {self.setup_data.name}")
           return None
        else:
            return self.setup_data.get_loading() 
        #QV(self.setup_data._Loading)
        #v,u = extract_value_unit(self.setup_data._setup['Electrode.Cat.Loading'])
        #return QV(v,u,"m /A")
    
    @property
    def temp0(self):
        """returns the catalyst loading in g m^-2

        Returns:
            float: loading in g m^-2
        """
        v,u = extract_value_unit(self.setup_data._setup['Temp_0'])
        return QV(v,u,"T")
    
    @property
    def pressure(self):
        """returns the pressure."""
        v,u = extract_value_unit(self.setup_data._setup['Pressure'])
        return QV(v,u,"p")
    
    @property
    def name(self):
        """returns dataset name"""

        return str(self.setup_data.name)
    
    def set_area(self,value:float,unit:str = ""):
        self.setup_data._area = value
        if unit == "":
            pass
        else:
            self.setup_data._area_unit = unit
        return
        
    def set_rotation(self,value:float,unit:str = ""):
        self.setup_data._rotation = value
        if unit == "":
            pass
        else:
            self.setup_data._rotation_unit = unit
        return
    
    def set_mass(self,value:float,unit:str = "g"):
        """sets the weight and calculates the loading."""
        return self.set_weight(value,unit)
    
    def set_weight(self,value:float,unit:str = "g"):
        """sets the weight and calculates the loading.

        Args:
            value (float): _description_
            unit (str, optional): _description_. Defaults to "g".
        """
        self.setup_data._Weight = QV(value,unit)
        self.setup_data._Loading = self.setup_data.get_mass() / self.setup_data.get_area()
        #if unit == "":
        #    pass
        #else:
        #    self.setup_data._Weight_unit = unit
        #return
    
    def set_loading(self,value:float,unit:str = "g m^-2"):
        """sets the loading and weight.

        Args:
            value (float): _description_
            unit (str, optional): _description_. Defaults to "".
        """
        self.setup_data._Loading = QV(value,unit,"L")
        self.setup_data._Weight = self.setup_data.get_loading() * self.setup_data.get_area()
    
    #########################################################################
    def set_RHE(self, V_RHE_vs_refereceElectrode):
        self.setup_data._RHE = str(V_RHE_vs_refereceElectrode)
        return
    
    def set_SHE(self, V_SHE_vs_refereceElectrode):
        self.setup_data._SHE = str(V_SHE_vs_refereceElectrode)
        return
    
    
    @property
    def RE(self)-> str:
        """Set the name of the reference electrode

        Returns:
            str: name of reference electrode
        """
        return str(self.setup_data._RE)
    
    @RE.setter
    def RE(self, reference_electrode_name:str):
        self.set_RE(reference_electrode_name)
        
    def set_RE(self, reference_electrode_name:str):
        self.setup_data._RE =str(reference_electrode_name)
        return
        
    #########################################################################

    
    @property
    def is_MWE(self) -> bool:
        return self.setup_data._setup.get('AddOn',False)
    
    
    def legend(self, *args, **kwargs)-> str:
        """_summary_

        use: legend = '?' to get a list of possible options
        Returns:
            str: legend 
        """
        s = str()
        #print(kwargs)
        """
        for arg in args:
            if isinstance(arg,legend_class):
                kwargs["legend"]=str(arg).replace("legend_","")
            if isinstance(arg,str):
                if arg.startswith("legend"):
                    kwargs["legend"]=str(arg).replace("legend_","")
        """
        kwargs = update_legend(*args,**kwargs)
        
        if 'legend' in kwargs:
            item = kwargs.get('legend',"").casefold()
            if item == '?':
                #print(self.setup_data._setup)
                return "_"
            elif item == "name".casefold():
                # print("NAME", self.setup_data.name,"LEGNEIGNSSSS")
                return self.setup_data.name
            elif item == RATE.casefold()or item == LEGEND.RATE.casefold():
                txt = f"{self.rate.value:.3f}"
                left_padding = txt.rjust(5) # ('{: <5}'.format(txt))
                return f"{left_padding} {self.rate.unit}"
            elif item == "rot_rate".casefold() or item == "rotation".casefold() or item == "rot".casefold() or item == LEGEND.ROT.casefold():
                txt = f"{self.rotation.value:.0f}"
                left_padding = txt.rjust(5) #('{: <5}'.format(txt))
                return f"{left_padding} {self.rotation.unit}"
            elif item.casefold() == "area".casefold():
                return str(self.area)
            elif item.casefold() =="date".casefold() or item == LEGEND.DATE.casefold():
                return  np.datetime_as_string(self.setup_data.dateTime, unit='D')
            elif item.casefold() =="time".casefold():
                return  np.datetime_as_string(self.setup_data.dateTime, unit='D')
            elif item.casefold() =="MWE".casefold():
                if self.is_MWE:
                    return  str(self.setup_data._MWE_CH)
                else:
                    return "not a MWE"
            elif item in self.setup_data._setup:
                print("items was found", item)
                s = self.setup_data._setup[item]
                return s
            else:
                return item
        return "_"
    
    def get_norm_factors(self, norm_to:str|tuple|list):
        norm_factor = QV(1,)
        if isinstance(norm_to, tuple):
            for arg in norm_to:
                x = self.get_norm_factor(arg)
                if x is not None:   
                    norm_factor = norm_factor * (x)
        else:        
            norm_factor = self.get_norm_factor(norm_to)
        return norm_factor
    
    def get_norm_factor(self, norm_to:str):
        """Get normalization factor
        Args:norm_to (str): 
            - "area", "area_cm", 
            - "rate", "sqrt_rate", 
            - "rotation", "sqrt_rotation" 

        Returns:
            _type_: _description_
        """
        norm_factor = QV(1)
        norm_to = str(norm_to).casefold()
        if norm_to == "area".casefold() or norm_to == AREA.casefold() :
            norm_factor = self.area
            if norm_factor.unit.casefold() == "cm^2".casefold():
                norm_factor = norm_factor*QV(1e-4,"m^2 cm^-2")
        elif norm_to  == "area_cm".casefold() or norm_to == AREA_CM.casefold() :
            norm_factor = self.area
            if norm_factor.unit.casefold() == "m^2".casefold():
                norm_factor = norm_factor*QV(1e4,"cm^2 m^-2")

        elif norm_to  == "rate".casefold() or norm_to  == RATE.casefold():
            norm_factor = self.rate

        elif norm_to  == "sqrt_rate".casefold() or norm_to  == SQRT_RATE.casefold():
    
           norm_factor = self.rate ** 0.5
        elif norm_to == "rot_rate".casefold() or norm_to == "rotation".casefold() or norm_to  == "rot".casefold() or norm_to  == ROT.casefold():

            norm_factor = self.rotation
    
        elif norm_to == "sqrt_rot_rate".casefold() or norm_to == "sqrt_rotation".casefold()or norm_to == SQRT_ROT.casefold() :

           norm_factor = self.rotation ** 0.5    
        
        elif norm_to == MASS.casefold() or norm_to == "weight".casefold()or norm_to == WEIGHT.casefold() :
           norm_factor = self.mass  
           
        elif norm_to == LOADING.casefold():
           norm_factor = self.loading  
        else:
            return
        return norm_factor

    def get_pot_offset(self, shift_to:str):
        shift = str(shift_to).casefold()
        shift_value = QV(0,"V","E")
        if shift == RHE.casefold():
            if self.setup_data._RHE is not None:
                s = self.setup_data._RHE
                v, u = extract_value_unit(s+" V")
                # print("AAAAAAAAA")
                shift_value = QV(v,"V","E vs RHE")
            else:   
                print("RHE vs reference electrode has not been defined")
            return shift_value
        elif shift == "SHE".casefold():
            if self.setup_data._SHE is not None:
                s = self.setup_data._SHE
                v, u = extract_value_unit(s)
                # print("AAAAAAAAA")
                shift_value = QV(v,"V","E vs SHE")
            else:
                print("SHE vs reference electrode has not been defined")
        elif shift == "RE".casefold():
            shift_value = QV(0,"V","E vs "+ self.setup_data._RE)
            return shift_value
        else:
            return None

    def set_active_RE(self,shift_to:str|tuple):
        end_norm_factor = None
        
        if isinstance(shift_to, tuple):

            for item in shift_to:
                shift_factor = self.get_pot_offset(item)
                if shift_factor:
                    self.setup_data.setACTIVE_RE(item)
                    end_norm_factor=  shift_factor
                    break
        elif shift_to is None:
            self.setup_data.setACTIVE_RE("")
            pass
        else:
            shift_factor = self.get_pot_offset(shift_to)
            #print(norm_factor)
            if shift_factor:
                self.setup_data.setACTIVE_RE(shift_to)
                end_norm_factor = shift_factor
        return end_norm_factor
        


    