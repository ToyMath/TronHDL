import unittest
from tronhdl.generator import VerilogGenerator

class TestVerilogGenerator(unittest.TestCase):
    def test_generate_adder(self):
        python_code = """
@TronHDL.module(input_width=4, output_width=4)
def Adder(a, b, sum):
    sum = a + b
"""
        generator = VerilogGenerator(input_width=4, output_width=4)
        verilog_code = generator.generate_verilog(python_code)
        expected_verilog = """module Adder (
    input [4-1:0] a,
    input [4-1:0] b,
    output [4-1:0] sum
);

    assign sum = (a + b);

endmodule
"""
        self.assertIn("module Adder", verilog_code)
        self.assertIn("assign sum = (a + b);", verilog_code)

if __name__ == '__main__':
    unittest.main()
