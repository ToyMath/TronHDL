from tronhdl import TronHDL, display, delay

@TronHDL.module(input_width=4, output_width=4)
def Adder(a, b, sum):
    sum = a + b

@TronHDL.testbench('Adder', input_widths={'a':4, 'b':4}, output_widths={'sum':4})
def tb_Adder():
    # Test Case 1
    a = 1
    b = 2
    delay(10)
    display("Test 1 - a: %b, b: %b, sum: %b", a, b, sum)

    # Test Case 2
    a = 4
    b = 5
    delay(10)
    display("Test 2 - a: %b, b: %b, sum: %b", a, b, sum)

if __name__ == "__main__":
    TronHDL.run_all_simulations()
