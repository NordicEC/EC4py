from .util import extract_value_unit
from .util import Quantity_Value_Unit as QV


class ec_setup_data:
        def __init__(self):
            self._setup = {"Current Range" : "", "Control Mode" : "", "Cell Switch": 0}
            self._area= 1.0
            self._area_unit="cm^2"
            self._rotation = 0.0
            self._rotation_unit ="/min"
            self.name =""
            self._RHE = None
            self._SHE = None
            return

class EC_Setup:
    """Describes the setup.
    
    properties:
    
    - area
    - rate
    - rotation
    -loading
    """
    def __init__(self):
        #self._setup.setup = {"Current Range" : "", "Control Mode" : "", "Cell Switch": 0}
        #self._setup._area= 1.0
        #self._setup._area_unit="cm^2"
        #self._setup._rotation = 0.0
        #self._setup_rotation_unit ="/min"
        self.setup_data = ec_setup_data()
        return
    
    def setup_reset(self):
        if 'Electrode.Area' in self.setup_data._setup:
            v,u = extract_value_unit(self.setup_data._setup['Electrode.Area'])
            self.set_area(v,u)
        if 'Inst.Convection.Speed' in self.setup_data._setup:
            v,u = extract_value_unit(self.setup_data._setup['Inst.Convection.Speed'])
            self.set_rotation(v,u)
        #if 'Inst.Convection.Speed' in self.setup_data._setup:
        #    v,u = extract_value_unit(self.setup_data._setup['Inst.Convection.Speed'])
        #    self.set_rotation(v,u)
            #self.setup_data._area_unit = u
    
    
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
        """
        Returns:
            area value and unit.
        """
        return QV(self.setup_data._area,self.setup_data._area_unit,"A")
        
    @area.setter
    def area(self, value:float):
        self.setup_data._area = value
        
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
    def rotation(self, value:float):
        """set the rotation rate

        Args:
            value (float): rotation rate
        """
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
        v,u = extract_value_unit(self.setup_data._setup['Rate'])
        return QV(v,u,"v")
    ###########################################################
    
    @property
    def weight(self):
        """returns the catalyst weight in g

        Returns:
            float: weight in g
        """
        v,u = extract_value_unit(self.setup_data._setup['Electrode.Cat.Weight'])
        return QV(v,u,"m")
    
    @property
    def loading(self):
        """returns the catalyst loading in g m^-2

        Returns:
            float: loading in g m^-2
        """
        v,u = extract_value_unit(self.setup_data._setup['Electrode.Cat.Loading'])
        return QV(v,u,"m /A")
    
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

        return self.setup_data.name
    
    def set_area(self,value:float,unit:str = ""):
        self.setup_data._area = value
        if unit == "":
            pass
        else:
            self.setup._area_unit = unit
        return
        
    def set_rotation(self,value:float,unit:str = ""):
        self.setup_data._rotation = value
        if unit == "":
            pass
        else:
            self.setup_data._rotation_unit = unit
        return
    
    def set_RHE(self, V_RHE_vs_refereceElectrode):
        self.setup_data._RHE = str(V_RHE_vs_refereceElectrode)
        return
    
    def set_SHE(self, V_SHE_vs_refereceElectrode):
        self.setup_data._SHE = str(V_SHE_vs_refereceElectrode)
        return
        
    #########################################################################

    
    
    def legend(self, **kwargs)-> str:
        """_summary_

        use: legend = '?' to get a list of possible options
        Returns:
            str: legend 
        """
        s = str()
        #print(kwargs)
        if 'legend' in kwargs:
            item = kwargs['legend']
            if item == '?':
                #print(self.setup_data._setup)
                return "_"
            elif item == "name":
                return self.setup_data.name
            elif item in self.setup_data._setup:
                #print("items was found", item)
                s = self.setup_data._setup[item]
                return s
            else:
                return item
        return "_"
        
    def get_norm_factor(self, norm_to:str):
        norm_factor = QV(1)
        norm_to = str(norm_to).casefold()
        if norm_to.casefold() == "area".casefold() :
           
           norm_factor = self.area
           
        elif norm_to.casefold() == "area_cm".casefold():
            norm_factor = self.area
            if norm_factor.unit.casefold() == "m^2".casefold():
                norm_factor = norm_factor*QV(1e4,"cm^2 m^-2")

        elif norm_to.casefold() == "rate".casefold() :
           norm_factor = self.rate
           
        elif norm_to.casefold() == "sqrt_rate".casefold():
    
           norm_factor = self.rate ** 0.5
        elif norm_to.casefold() == "rot_rate".casefold() or norm_to.casefold() == "rotation".casefold() or norm_to.casefold() == "rot".casefold():
           
            norm_factor = self.rotation
          
        elif norm_to == "sqrt_rot_rate".casefold() or norm_to == "sqrt_rot".casefold() :
           
           norm_factor = self.rotation ** 0.5    
        else:
            return
        return norm_factor

    def get_pot_offset(self, shift_to:str):
        shift = str(shift_to).casefold()
        shift_value = QV(0,"V","E")
        if shift == "RHE".casefold():
            if self.setup_data._RHE is not None:
                s = self.setup_data._RHE
                v, u = extract_value_unit(s+" V")
                # print("AAAAAAAAA")
                shift_value = QV(v,"V","E vs RHE")
            else:   
                print("RHE vs reference electrode has not been defined")
            return shift_value
        if shift == "SHE".casefold():
            if self.setup_data._SHE is not None:
                s = self.setup_data._SHE
                v, u = extract_value_unit(s)
                # print("AAAAAAAAA")
                shift_value = QV(v,"V","E vs SHE")
            else:
                print("SHE vs reference electrode has not been defined")
            return shift_value
        


    