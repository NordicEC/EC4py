



from ..lsv.lsv_datas import LSV_Datas

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    # Gives Pylance/Pyright full autocomplete without circular imports
    from .cv_datas import CV_Datas
    _Base = CV_Datas
else:
    _Base = object

# import pandas as pd
#from .analysis_tafel import Tafel as Tafel_calc


# STYLE_POS_DL = "bo"
# STYLE_NEG_DL = "ro"

class CV_Datas_Extra(_Base):


    def set_i_at_E_to_zero(self, E:float, *args, **kwargs):
        """Set the current at a specific voltage to zero.
        
        Args:
            E (float): potential where to set the current to zero. 

        """
        for x in self.datas:
            x.set_i_at_E_to_zero(E,*args,**kwargs)

    ################################################################   

    def get_i_at_E(self, E:float, direction:str,*args, **kwargs):
        """Get the current at a specific voltage.

        Args:
            E (float): potential where to get the current. 
            dir (str): direction, "pos,neg or all"
        Returns:
            list of current at E
        """

        return [x.get_i_at_E(E,direction,*args,**kwargs) for x in self.datas]

    
        
    def get_E_of_max_i(self, E1:float,E2:float,*args,**kwargs):
        """get the potential of maximum current in a range.

        Args:
            E1 (float): _description_
            E2 (float): _description_

        Returns:
            _type_: _description_
        """
        return [cv.get_E_of_max_i(E1,E2,*args, **kwargs) for cv in self.datas]
    
    def get_E_of_min_i(self, E1:float,E2:float,*args,**kwargs):
        """get the potential of maximum current in a range.

        Args:
            E1 (float): _description_
            E2 (float): _description_

        Returns:
            _type_: _description_
        """
        return [cv.get_E_of_min_i(E1,E2,*args, **kwargs) for cv in self.datas]

    def set_active_RE(self,*args):     
        """Set active reference electrode for plotting.
        
        - RHE    - if values is not already set, use ".set_RHE()"
        
        - SHE    - if values is not already set, use ".set_RHE()"
        - None to use the exerimental 
        """
        for cv in self.datas:
            cv.set_active_RE(args)
        return

        ########################################################################################################

    def get_sweep(self,sweep:str,update_label=True):
        """_summary_

        Args:
            sweep (str): use "POS","NEG", "AVG" or "DIF" 
            update_label (bool, optional): Change the label of the current according to the sweep. Defaults to True.

        Returns:
            LSV_Datas
        """
        
        
        LSVs = LSV_Datas()
        LSVs.dir = sweep
        for cv in self.datas:
            LSVs.append(cv.get_sweep(sweep,update_label))
        return LSVs

    #########################################################################

    def export_DataFrame(self,direction,*args, **kwargs):
        LSVs=self.get_sweep(direction,False)
        LSVs.set_active_RE(args)
        LSVs.norm(*args)
        return LSVs.export_DataFrame()
    
    #########################################################################

    def export_Array(self,direction,*args, **kwargs):
        LSVs=self.get_sweep(direction,False)
        LSVs.set_active_RE(args)
        LSVs.norm(*args)
        return LSVs.export_Array()


    def norm(self,*args, **kwargs):
        """Normalise the current to certain factors. 

        Args:
            norm_to (str | tuple): _description_
        """
        
        for x in self.datas:
            x.norm(args)
        return


    




