
from ec4py.method_util import EC_Array_class

from pathlib import Path
import numpy as np

import unittest   # The test framework

gdata_u = np.array([range(0,101)])/100
gdata_d = np.array([range(99,0,-1)])/100

gdata_ud = np.concatenate((gdata_u, gdata_d),axis=1)
gdata_du = np.concatenate((gdata_d, gdata_u),axis=1)

######################################################################################
class test_array_class( unittest.TestCase ):
     
    def test_ini_class(self):
        EC_Array_class()

    def test_append(self):
        a=EC_Array_class()
        array = [5,2,1]
        for x in array:
            a.append(x)
        self.assertEqual(len(a),len(array))
        self.assertListEqual(a.datas,array)
        for i in range(len(a)):
            self.assertEqual(a[i],array[i])
        for i,x in enumerate(a):
            self.assertEqual(x,array[i])
        sub= a[1:3]
        array_sub= array[1:3]
        for i in range(len(sub)):
            self.assertEqual(sub[i],array_sub[i])

        sub = a[["a",'b']]
        
        for i in range(len(sub)):
                    self.assertEqual(sub[i],array_sub[i])
        
                


if __name__ == '__main__':
    unittest.main()
