
import copy
from ec4py.ec_setup import EC_Setup
from ec4py.util import Quantity_Value_Unit as QVU
from ec4py.util_graph import LEGEND
from ec4py.ec_util import EC_Data_Base
from ec4py.ec_util.ec_data_txt import _parse_data,_parse_data_header,_parse_category,_category_to_dict
from ec4py.ec_util.ec_data_txt import _s_load_txt
#"import inc_dec    # "The code to test
import unittest   # The test framework
import numpy as np
from pathlib import Path


txt_CV_Data = """[COMMON]
	PROG	EC4 App
	DATE	2025-05-03
	TIME	15:46:26 (GMT +02:00)
[POT_SETTINGS]
	IRANGE	0
	MODE	pot
	CELL_SW	0
[METHOD]
	EC Tech	Ramp
	NAME	Linear Sweep Voltammetry
	Start	0.500 V
	v1	1.000 V
	v2	0.000 V
	Rate	100.0 mV/s
	Ramp	1
[DATA]
Index	Time(s)	E(V)	i(A)
0	0	1	1
1	0.1	1	1
2	0.2	2	3"""



class test_EC_Data_TXT(unittest.TestCase):

    def test__parse_category(self):
        txt_COMMON = """
        [COMMON]
            PROG	EC4 App
            DATE	2025-05-03
            TIME	15:46:26 (GMT +02:00)
        [AAAA]"""
        d_common =_parse_category(txt_COMMON,"COMMON")
        self.assertEqual(len(d_common),107)
       
       

    def test__category_to_dict(self):
        txt_COMMON = """[COMMON]
            PROG	EC4 App
            DATE	2025-05-03
            TIME	15:46:26 (GMT +02:00)
        \n[AAAA]"""
        d_common =_category_to_dict(_parse_category(txt_COMMON,"COMMON"))
        prog = d_common.get("PROG",None)
        print(d_common)
        self.assertEqual(len(d_common),3)
        self.assertEqual(prog,"EC4 App")
        self.assertEqual(d_common["DATE"],"2025-05-03")
        self.assertEqual(d_common["TIME"],"15:46:26 (GMT +02:00)")
       
    def test__parse_data_header(self):
        s_dataHeader =_parse_category(txt_CV_Data,"DATA")
        data,quantity,unit =_parse_data_header(s_dataHeader)
        exp_quantity = ["Index","Time","E","i"]
        self.assertListEqual(quantity, exp_quantity)
        exp_unit = ["","s","V","A"]
        self.assertListEqual(unit, exp_unit)
 
    def test_parse_data(self):
        print(txt_CV_Data)
        data,quantity,unit =_parse_data(txt_CV_Data)
        exp_quantity = ["Index","Time","E","i"]
        self.assertListEqual(quantity, exp_quantity)
        exp_unit = ["","s","V","A"]
        self.assertListEqual(unit, exp_unit)
        self.assertTrue(np.allclose(data["Index"], [0.0,1,2],  atol=1e-10, rtol=1e-10))
        self.assertTrue(np.allclose(data["Time"], [0.0,.1,.2],  atol=1e-10, rtol=1e-10))
        self.assertTrue(np.allclose(data["E"], [1,1,2],  atol=1e-10, rtol=1e-10))
        self.assertTrue(np.allclose(data["i"], [1,1,3], atol=1e-10, rtol=1e-10))

    def test_LoadTXT_CV_all(self):
        obj = EC_Data_Base()
        _s_load_txt(obj,txt_CV_Data)

        self.assertTrue(np.allclose(obj.Time, [0.0,.1,.2],  atol=1e-10, rtol=1e-10))
        self.assertTrue(np.allclose(obj.E, [1,1,2],  atol=1e-10, rtol=1e-10))
        self.assertTrue(np.allclose(obj.i, [1,1,3],  atol=1e-10, rtol=1e-10))
        #self.assertTrue(np.allclose(obj.rawdata, [1,1,3],  atol=1e-10, rtol=1e-10))
        

  

if __name__ == '__main__':
    unittest.main()
