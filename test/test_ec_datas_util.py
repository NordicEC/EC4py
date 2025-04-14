
import copy
from ec4py.ec_setup import EC_Setup
from ec4py.util import Quantity_Value_Unit as QVU
from ec4py.util_graph import LEGEND
from ec4py.ec_datas_util import EC_Datas_base
from ec4py.cv_datas import CV_Datas
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

def pop_and_len(self, datasType,value1,value2):
        datas = datasType
        datas.append(value1)
        datas.append(value2)
        self.assertEqual(len(datas), 2)
        self.assertEqual(datas[0], value1)
        self.assertEqual(datas[1], value2)
        datas.pop(1)
        self.assertEqual(len(datas), 1)

if __name__ == '__main__':
    unittest.main()
