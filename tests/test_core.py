import os
import unittest
from tronhdl.core import TronHDL
from tronhdl.utils import delay, display

class TestTronHDLCore(unittest.TestCase):
    def test_module_decorator(self):
        @TronHDL.module(input_width=4, output_width=4)
        def Adder(a, b, sum):
            sum = a + b

        self.assertTrue(os.path.exists('Adder.v'))

    def test_testbench_decorator(self):
        @TronHDL.testbench('Adder', input_widths={'a':4, 'b':4}, output_widths={'sum':4})
        def tb_Adder():
            a = 1
            b = 2
            delay(10)
            display("Test 1 - a: %b, b: %b, sum: %b", a, b, sum)

        self.assertTrue(os.path.exists('tb_Adder.v'))

if __name__ == '__main__':
    unittest.main()
