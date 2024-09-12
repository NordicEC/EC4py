

from ec4py import Quantity_Value_Unit as QVU
#"import inc_dec    # "The code to test
import unittest   # The test framework

a = QVU("5 m","l")
b = QVU(2. ,"m","l")
c = QVU(6. ,"s","t")

class Test_Quantity_Value_Unit(unittest.TestCase):
    def test_create(self):
        self.assertEqual(QVU("5 m").value, 5.0)
        self.assertEqual(QVU("5 m").unit, "m")
        self.assertEqual(QVU("5 a^2 b^-3").unit, "a^2 b^-3")
        self.assertEqual(QVU(5,"m","q").quantity, "q")
        self.assertEqual(QVU(5,"m","q").unit, "m")

    def test_add(self):
        q = a+b
        self.assertEqual(q.value, 7.0)
        self.assertEqual(q.unit, "m")
        #different units
        with self.assertRaises(Exception):
            a+c

        
        
    def test_sub(self):
        value = a.value - b.value
        self.assertEqual((a-b).value, value)
        self.assertEqual((a-b).unit, "m")
        with self.assertRaises(Exception):
            a-c
    
    def test_mul(self):
        q = a*b
        self.assertEqual(q.value, 10.0)
        self.assertEqual(q.unit, "m^2")
        q = q / 5
        self.assertEqual(q.value, 2.0)
        self.assertEqual(q.unit, "m^2")
        q = q*c
        self.assertEqual(q.value, 12.0)
        self.assertEqual(q.unit, "m^2 s")
        with self.assertRaises(Exception):
            a*dict
    
    def test_pow(self):
        q = a**3
        v = a.value**3 
        self.assertEqual(q.value, v)
        self.assertEqual(q.unit, "m^3")
        q = a**-2
        self.assertEqual(q.value, 1/25.0)
        self.assertEqual(q.unit, "m^-2")
        with self.assertRaises(Exception):
            a**dict
        
        
if __name__ == '__main__':
    unittest.main()
