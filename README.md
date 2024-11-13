# TronHDL 🚀✨

**TronHDL** is your ultimate Python-powered transcompiler designed to **supercharge** ASIC and FPGA designs! Harness the power of Python's simplicity and flexibility to generate robust Verilog modules and testbenches effortlessly. Whether you're a seasoned hardware designer or just starting out, TronHDL transforms your design workflow, making hardware development **faster**, **smarter**, and **more efficient**. 💡🔧

## 🌟 Features 🌟

- **🔄 Seamless Module Generation**: Define Verilog modules using Python decorators.
- **🧪 Automated Testbench Creation**: Craft comprehensive testbenches with ease.
- **⚡️ Rapid Simulation**: Compile and run simulations directly from Python scripts.
- **🔍 Intuitive Debugging**: Leverage Python's readability for easier troubleshooting.
- **🔧 Extensible Architecture**: Customize and extend TronHDL to fit your unique design needs.
- **📦 Ready for PyPI**: Install TronHDL effortlessly via pip and integrate it into your projects.

## 📥 Installation 📥

### 🛠️ Prerequisites

- **Python 3.6+** 🐍
- **Icarus Verilog** for simulation 🚀

### 🚀 Steps to Install

**Clone the Repository**

    ```bash
    git clone https://github.com/ToyMath/TronHDL.git
    cd TronHDL
    ```

**Install TronHDL via pip**

    ```bash
    pip install .
    ```

**Install Icarus Verilog**

- **Ubuntu/Debian**

    ```bash
    sudo apt-get install iverilog
    ```

- **macOS (using Homebrew)**

    ```bash
    brew install icarus-verilog
    ```

- **Windows**

    Download and install from [Icarus Verilog Releases](http://bleyer.org/icarus/).

## 🛠️ Quick Start 🛠️

### 🔧 Defining Verilog Modules

Use the `@TronHDL.module` decorator to define your Verilog modules effortlessly.

```python
from tronhdl import TronHDL

@TronHDL.module(input_width=4, output_width=4)
def Adder(a, b, sum):
    sum = a + b
```

```python
from tronhdl import TronHDL

@TronHDL.module(input_width=4, output_width=4)
def Subtractor(x, y, difference):
    difference = x - y
```

```python
from tronhdl import TronHDL

@TronHDL.module(input_width=8, output_width=16)
def matrix_mult_2x2(a11, a12, a21, a22, b11, b12, b21, b22, c11, c12, c21, c22):
    c11 = a11 * b11 + a12 * b21
    c12 = a11 * b12 + a12 * b22
    c21 = a21 * b11 + a22 * b21
    c22 = a21 * b12 + a22 * b22
```

Use the `@TronHDL.testbench` decorator to define your tests.

```python
from tronhdl import TronHDL, display, delay

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
```

```python
from tronhdl import TronHDL, display, delay

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
```

```python
from tronhdl import TronHDL, display, delay

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
    a11 = 0
    a12 = 0
    a21 = 0
    a22 = 0
    b11 = 0
    b12 = 0
    b21 = 0
    b22 = 0
    delay(100)

    a11 = 1
    a12 = 2
    a21 = 3
    a22 = 4
    b11 = 5
    b12 = 6
    b21 = 7
    b22 = 8
    delay(100)

    display("Resulting Matrix:")
    display("C11: %d, C12: %d", c11, c12)
    display("C21: %d, C22: %d", c21, c22)
```

Run all simulations

```python
TronHDL.run_all_simulations()
```