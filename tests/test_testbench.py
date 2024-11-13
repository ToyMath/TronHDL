import ast
import unittest
from tronhdl.testbench import VerilogTestbenchGenerator

class TestVerilogTestbenchGenerator(unittest.TestCase):
    def test_generate_testbench(self):
        python_code = """
@TronHDL.testbench('Adder', input_widths={'a':4, 'b':4}, output_widths={'sum':4})
def tb_Adder():
    a = 1
    b = 2
    delay(10)
    display("Test 1 - a: %b, b: %b, sum: %b", a, b, sum)
"""
        generator = VerilogTestbenchGenerator(
            module_name='Adder',
            input_widths={'a':4, 'b':4},
            output_widths={'sum':4}
        )
        generator.visit(ast.parse(python_code))
        verilog_code = generator.generate()
        self.assertIn("module tb_Adder;", verilog_code)
        self.assertIn("reg [4-1:0] a;", verilog_code)
        self.assertIn("wire [4-1:0] sum;", verilog_code)
        self.assertIn("$display(\"Test 1 - a: %b, b: %b, sum: %b\", a, b, sum);", verilog_code)

if __name__ == '__main__':
    unittest.main()
