
import copy
from ec4py.ec_setup import EC_Setup
from ec4py.util import Quantity_Value_Unit as QVU
from ec4py.util_graph import LEGEND
from ec4py.ec_datas_util import EC_Datas_base
#"import inc_dec    # "The code to test
import unittest   # The test framework
import numpy as np
from pathlib import Path


class test_EC_Datas_base(unittest.TestCase):

    def test_base(self):
        datas = EC_Datas_base()
        
        datas.append(float(1))
        datas.append(float(2))
        
        
    def test_append_and_len(self):
        datas = EC_Datas_base()
        datas.append(float(1))
        datas.append(float(2))
        self.assertEqual(len(datas), 2)
        self.assertEqual(datas[0], 1)
        self.assertEqual(datas[1], 2)
        datas.pop(1)
        self.assertEqual(len(datas), 1)

    def test_append_and_len_all(self):
        pop_and_len(self,EC_Datas_base(),float(1),float(2) ) 
        
    def test_quantities(self):
        datas = EC_Datas_base()
        datas.append(EC_Setup())
        datas.append(EC_Setup())
        datas[0].set_area("2 m^2" )
        datas[1].set_area("1 m^2" )
        datas[0].set_mass("3 g")
        datas[1].set_mass("2 g")
        #datas[0].set_rate("1 V /s")
        #datas[1].set_rate("2 V /s")
        test_quantities(self, datas)
         

def pop_and_len(obj, datasType,value1,value2):
    datas = datasType
    datas.append(value1)
    datas.append(value2)
    obj.assertEqual(len(datas), 2)
    obj.assertEqual(datas[0], value1)
    obj.assertEqual(datas[1], value2)
    datas.pop(1)
    obj.assertEqual(len(datas), 1)
         
def  test_quantities(obj, datasType_with_a_length):
    datas = datasType_with_a_length
    length = len(datasType_with_a_length)
    for data in datas:
        data.set_area("2 m^2" )
        data.set_area("1 m^2" )
        data.set_mass("3 g")
        data.set_mass("2 g")
    
    
    area = datas.area
    obj.assertEqual(len(area), length)    
    for a in area:
        obj.assertEqual(a.quantity, "A")
    #mass
    mass = datas.mass
    #mass
    obj.assertEqual(len(mass), length)    
    for a in mass:
        obj.assertEqual(a.quantity, "m")

if __name__ == '__main__':
    unittest.main()
