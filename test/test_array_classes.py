from ec4py import EC_Datas,EC_Data

from ec4py import CV_Datas,CV_Data
from ec4py import LSV_Datas,LSV_Data

from ec4py import Step_Datas, Step_Data

from ec4py import AREA,AREA_CM
from ec4py.util import Quantity_Value_Unit as QVU
#"import inc_dec    # "The code to test
import unittest   # The test framework
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

 
#from test_ec_datas_util import pop_and_len
#from help_fx import test_quantities_add
from help_fx import pop_and_len,unithelp_quantities_add






class test_Array_Classes(unittest.TestCase):
    def test_EC_Datas(self):
        pop_and_len(self, EC_Datas(), EC_Data(),EC_Data())
        a = EC_Datas()
        a.append(EC_Data()) 
        a.append(EC_Data()) 
        unithelp_quantities_add(self, a)
        
    def test_CV_Datas(self):
        pop_and_len(self, CV_Datas(), CV_Data(),CV_Data())
        a = CV_Datas()
        a.append(CV_Data()) 
        a.append(CV_Data()) 
        unithelp_quantities_add(self, a)
        
    def test_LSV_Datas1(self):
        pop_and_len(self, LSV_Datas(), LSV_Data(),LSV_Data())
    def test_LSV_Datas2(self):
        a = LSV_Datas()
        a.append(LSV_Data()) 
        a.append(LSV_Data()) 
        unithelp_quantities_add(self, a)
        
    def test_Step_Datas(self):
        pop_and_len(self, Step_Datas(), Step_Data(),Step_Data())
        a = Step_Datas()
        a.append(Step_Data()) 
        a.append(Step_Data()) 
        unithelp_quantities_add(self, a)