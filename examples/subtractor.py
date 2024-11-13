from tronhdl import TronHDL, display, delay

@TronHDL.module(input_width=4, output_width=4)
def Subtractor(x, y, difference):
    difference = x - y

@TronHDL.testbench('Subtractor', input_widths={'x':4, 'y':4}, output_widths={'difference':4})
def tb_Subtractor():
    # Test Case 1
    x = 4
    y = 2
    delay(10)
    display("Test 1 - x: %b, y: %b, difference: %b", x, y, difference) # type: ignore

    # Test Case 2
    x = 10
    y = 6
    delay(10)
    display("Test 2 - x: %b, y: %b, difference: %b", x, y, difference) # type: ignore

if __name__ == "__main__":
    TronHDL.run_all_simulations()
