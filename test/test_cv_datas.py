

from ec4py import CV_Datas,CV_Data
from ec4py import AREA,AREA_CM
from ec4py.util import Quantity_Value_Unit as QVU
#"import inc_dec    # "The code to test
import unittest   # The test framework
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

#from test_ec_datas_util import pop_and_len
#from help_fx import test_quantities_add
from .help_fx import pop_and_len

E =np.array([1,2,3])
paths = []
path_to_dataSetFolder = Path(".").cwd() / "test_data" /"CV"
print(path_to_dataSetFolder)
#C:\Users\gusta\Documents\GitHub\Python\NordicEC\EC4py\test_data\CV\CV_144700_ 3.tdms
#paths.append( path_to_dataSetFolder / "CV_144913_ 3.tdms")
paths.append( path_to_dataSetFolder / "CV_144700_ 3.tdms")
paths.append( path_to_dataSetFolder / "CV_153541_ 3.tdms")
#paths.append( path_to_dataSetFolder / "CV_153333_ 3.tdms")
#paths.append( path_to_dataSetFolder / "CV_151300_ 3.tdms")
#paths.append( path_to_dataSetFolder / "CV_151725_ 3.tdms")
#paths.append( path_to_dataSetFolder / "CV_151512_ 3.tdms")
    



def AAAquantities_add( datasType_with_a_length ):
    datas = datasType_with_a_length
    for data in datas:
        data.set_area("2 m^2" )
        data.set_area("1 m^2" )
        data.set_mass("3 g")
        data.set_mass("2 g")      

class Test_CV_Datas(unittest.TestCase):
    
    def test_files_exists(self):
        for path in paths:
            self.assertTrue(path.exists)
            
    def test_files_load(self):
        datas = CV_Datas(paths)
        
    def test_set_i_at_E_to_zero(self):
        data = CV_Data()
        data.i_p = np.ones(len(data.E))*5
        data.i_n = np.ones(len(data.E))*3 
        datas = CV_Datas()
        datas.append(data)
        datas.append(data.copy())
        datas.set_i_at_E_to_zero(0.3)
        for d in datas:
            self.assertTrue(np.allclose(d.i_p, 0,  atol=1e-10, rtol=1e-10))
            self.assertTrue(np.allclose(d.i_n, 0,  atol=1e-10, rtol=1e-10))
        
    def test_plot(self):
        datas = CV_Datas(paths)
        a = datas.plot()
        datas.plot(AREA)
        plt.close("all")
        
class test_CV_Data_arrays(unittest.TestCase):
    def test_pop_and_len(self):
        pop_and_len(self, CV_Datas(), CV_Data(),CV_Data())

    def test_quantities(self):
        datas = CV_Datas()
        datas.append(CV_Data())
        datas.append(CV_Data())
        AAAquantities_add(datas)
        length = len(datas)
        area = datas.area
        self.assertEqual(len(area), length)    
        for a in area:
            self.assertEqual(a.quantity, "A")
        #mass
        mass = datas.mass
        #mass
        self.assertEqual(len(mass), length)    
        for a in mass:
            self.assertEqual(a.quantity, "m")


class test_CV_Datas_arithmetics( unittest.TestCase ):
    def test_s1_add(self):
        data = CV_Data()
        data.i_p = data.E*2
        data.i_n = data.E+2
        datab = data+data
        datas = CV_Datas()
        datas.append(data)
        datas.append(datab)
           
        datasb =datas+datas
        for d in range(len(datas)):
            self.assertTrue(np.allclose(datasb[d].i_p, datas[d].i_p*2,  atol=1e-10, rtol=1e-10))# type: ignore
            self.assertTrue(np.allclose(datasb[d].i_n, datas[d].i_n*2,  atol=1e-10, rtol=1e-10)) # type: ignore
        datasb =datas+3.0
        for d in range(len(datas)):
            self.assertTrue(np.allclose(datasb[d].i_p, datas[d].i_p+3,  atol=1e-10, rtol=1e-10))# type: ignore
            self.assertTrue(np.allclose(datasb[d].i_n, datas[d].i_n+3,  atol=1e-10, rtol=1e-10))# type: ignore
      
    def test_s1_add_b(self):
                data = CV_Data()
                data.i_p = np.ones([1])
                data.i_n = np.ones([2])
                datab = data+data
                datas = CV_Datas()
                datas.append(data)
                datas.append(datab)
                print(data.i_p)
                ###add a list
                off=[10.1,4]
                datasb =datas+off  # type: ignore
                for d in range(len(datas)):
                    print('aa', datas[d].i_p,'OFF:',off[d],'AA',datas[d].i_p+off[d],'RR',datasb[d].i_p)
                    self.assertTrue(np.allclose(datasb[d].i_p, datas[d].i_p+off[d],  atol=1e-5, rtol=1e-5))# type: ignore
                    self.assertTrue(np.allclose(datasb[d].i_n, datas[d].i_n+off[d],  atol=1e-5, rtol=1e-5))# type: ignore
              
                with self.assertRaises(ValueError):
                    data2 =data+[3]
                with self.assertRaises(ValueError):
                    data2 =data+[3,1,4]

        
    def test_s2_sub(self):
        data = CV_Data()
        data.i_p = data.E
        data.i_n = data.E+2
        datab = data.copy()
        datas = CV_Datas()
        datas.append(data)
        datas.append(datab)
        datasb =datas-3
        #print(datas[0].i_p-(3))
        #print(datasb[0].i_p)
        for d in range(len(datas)):
            self.assertTrue(np.allclose(datasb[d].i_p, datas[d].i_p-3,  atol=1e-10, rtol=1e-10))# type: ignore
            self.assertTrue(np.allclose(datasb[d].i_n, datas[d].i_n-3,  atol=1e-10, rtol=1e-10))# type: ignore
      
        ###add a list
        off=[2.0,3.0]
        datasb.sub(off)
        datasb =datas-off
        for d in range(len(datas)):
            self.assertTrue(np.allclose(datasb[d].i_p, datas[d].i_p-off[d],  atol=1e-10, rtol=1e-10))# type: ignore
            self.assertTrue(np.allclose(datasb[d].i_n, datas[d].i_n-off[d],  atol=1e-10, rtol=1e-10))# type: ignore
      
        off=[2.0,3]
        datasb =datas-off
        for d in range(len(datas)):
            self.assertTrue(np.allclose(datasb[d].i_p, datas[d].i_p-off[d],  atol=1e-10, rtol=1e-10))# type: ignore
            self.assertTrue(np.allclose(datasb[d].i_n, datas[d].i_n-off[d],  atol=1e-10, rtol=1e-10))# type: ignore
      
        with self.assertRaises(ValueError):
            data2 =data+[3]
        with self.assertRaises(ValueError):
            data2 =data+[3,1,4]

            
    def test_a3_mul(self):
        data = CV_Data()
        data.i_p = data.E
        data.i_n = data.E+2
        datas = CV_Datas()
        datas.append(data)
        datas.append(data.copy())
        datas.mul(2)
        for d in datas:
            self.assertTrue(np.allclose(d.i_p, d.E*2,  atol=1e-10, rtol=1e-10))
            self.assertTrue(np.allclose(d.i_n, (d.E+2)*2,  atol=1e-10, rtol=1e-10))
        datas2=datas*3
        for d in range(len(datas2)):    
            self.assertTrue(np.allclose(datas2[d].i_p, datas[d].i_p*3,  atol=1e-10, rtol=1e-10))# type: ignore
            self.assertTrue(np.allclose(datas2[d].i_n, datas[d].i_n*3,  atol=1e-10, rtol=1e-10))# type: ignore
        
        off=[2,3]
        datas2 =datas * off #type: ignore
        for d in range(len(datas2)):
            self.assertTrue(np.allclose(datas2[d].i_p, datas[d].i_p*off[d],  atol=1e-10, rtol=1e-10))# type: ignore
            self.assertTrue(np.allclose(datas2[d].i_n, datas[d].i_n*off[d],  atol=1e-10, rtol=1e-10))# type: ignore
        
        ###add a list
        with self.assertRaises(ValueError):
            data2 =datas*[3] # type: ignore
        with self.assertRaises(ValueError):
            data2 =datas*[3,1,4]  # type: ignore
        with self.assertRaises(TypeError):
            data2 =datas*datas  # type: ignore
                   
        
    def test_a4_div(self):
        data = CV_Data()
        data.i_p = data.E
        data.i_n = data.E+2
        datas = CV_Datas()
        datas.append(data)
        datas.append(data.copy())
        datas.append(data.copy())
 
        datas.div(3)
        for d in datas:
            self.assertTrue(np.allclose(d.i_p, d.E/3,  atol=1e-10, rtol=1e-10))
            self.assertTrue(np.allclose(d.i_n, (d.E+2)/3,  atol=1e-10, rtol=1e-10))
        datas2=datas/3
        for d in range(len(datas2)):    
            self.assertTrue(np.allclose(datas2[d].i_p, datas[d].i_p/3,  atol=1e-10, rtol=1e-10)) # type: ignore
        
        off=[3.,2.,2.]
        datas2 =datas / off           # type: ignore
        datas3=datas / 1
        datas3.div(off)
        print(datas[0].i_n[0],datas3[0].i_n[0],datas2[0].i_n[0])
        for d in range(len(datas2)):
            self.assertTrue(np.allclose(datas2[d].i_p[0], datas[d].i_p[0]/off[d],  atol=1e-1, rtol=1e-1)) # type: ignore
        for d in range(len(datas2)):
            self.assertTrue(np.allclose(datas3[d].i_p, datas[d].i_p/off[d],  atol=1e-5, rtol=1e-5)) # type: ignore
        datas3+=3
        datas3=datas3/datas3
                
        print(datas[1].i_n[1],datas3[1].i_n[1],datas2[1].i_n[1]/datas2[1].i_n[1])

        for d in range(len(datas2)):
            self.assertTrue(np.allclose(datas3[d].i_p, datas[d].i_p+3/(datas[d].i_p+3),  atol=10e-1, rtol=10e-1)) # type: ignore
              

     ###add a list
        with self.assertRaises(ValueError):
            data2 =datas*[3]  # type: ignore
        with self.assertRaises(ValueError):
            data2 =datas*[3,1,4,4]  # type: ignore
        with self.assertRaises(TypeError):
            data2 =datas*datas  # type: ignore
                   
    
       
        
        
    
  

if __name__ == '__main__':
    unittest.main()
