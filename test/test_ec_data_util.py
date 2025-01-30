
import copy
from ec4py.ec_setup import EC_Setup
from ec4py.util import Quantity_Value_Unit as QVU
from ec4py.util_graph import LEGEND
from ec4py.ec_data_util import EC_Channels
#"import inc_dec    # "The code to test
import unittest   # The test framework
import numpy as np
from pathlib import Path

class test_EC_Channels(unittest.TestCase):

    def test_default_channel(self):
        ch = EC_Channels()
        
        self.assertEqual(ch.Voltage, "E")
        self.assertEqual(ch.Current, "i")
        self.assertEqual(ch.Impedance, "Z_E")
        self.assertEqual(ch.Phase, "Phase_E")
        
    def test_set_i_channels(self):
        channel="AA"
        ch = EC_Channels(i=channel)
        self.assertEqual(ch.Current, channel)
        self.assertEqual(ch.Voltage, "E")
        self.assertEqual(ch.Impedance, "Z_E")
        self.assertEqual(ch.Phase, "Phase_E")
        
    def test_set_E_channels(self):
        channel="AA"
        ch = EC_Channels(E=channel)
        self.assertEqual(ch.Current, "i")
        self.assertEqual(ch.Voltage, channel)
        self.assertEqual(ch.Impedance, "Z_E")
        self.assertEqual(ch.Phase, "Phase_E")

    def test_MWE_channels(self):
        channel_num=4
        ch = EC_Channels(str(f"i{channel_num}"))
        
        self.assertEqual(ch.Voltage, "E")
        self.assertEqual(ch.Current, str(f"i{channel_num}"))
        self.assertEqual(ch.Impedance,str(f"Z{channel_num}"))
        self.assertEqual(ch.Phase, str(f"Phase{channel_num}"))
 
    def test_MultiPOT(self):
        channel_num=4
        ch = EC_Channels(f"P{channel_num}")
        
        self.assertEqual(ch.Voltage, str(f"P{channel_num}_E"))
        self.assertEqual(ch.Current, str(f"P{channel_num}_i"))
        self.assertEqual(ch.Impedance,str(f"P{channel_num}_Z"))
        self.assertEqual(ch.Phase, str(f"P{channel_num}_Phase"))
     

  

if __name__ == '__main__':
    unittest.main()
