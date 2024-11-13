from tronhdl import TronHDL, display, delay

@TronHDL.module(input_width=8, output_width=16)
def matrix_mult_2x2(a11, a12, a21, a22, b11, b12, b21, b22, c11, c12, c21, c22):
    # Perform 2x2 matrix multiplication
    c11 = a11 * b11 + a12 * b21
    c12 = a11 * b12 + a12 * b22
    c21 = a21 * b11 + a22 * b21
    c22 = a21 * b12 + a22 * b22

@TronHDL.testbench(
    'matrix_mult_2x2',
    input_widths={
        'a11':8, 'a12':8, 'a21':8, 'a22':8,
        'b11':8, 'b12':8, 'b21':8, 'b22':8
    },
    output_widths={
        'c11':16, 'c12':16, 'c21':16, 'c22':16
    }
)
def tb_matrix_mult_2x2():
    # Initialize Inputs
    a11 = 0
    a12 = 0
    a21 = 0
    a22 = 0
    b11 = 0
    b12 = 0
    b21 = 0
    b22 = 0
    delay(100)

    # Stimulus
    a11 = 1
    a12 = 2
    a21 = 3
    a22 = 4
    b11 = 5
    b12 = 6
    b21 = 7
    b22 = 8
    delay(100)

    # Display Results
    display("Resulting Matrix:")
    display("C11: %d, C12: %d", c11, c12) # type: ignore
    display("C21: %d, C22: %d", c21, c22) # type: ignore

if __name__ == "__main__":
    TronHDL.run_all_simulations()
