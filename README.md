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

1. **Clone the Repository**

    ```bash
    git clone https://github.com/ToyMath/TronHDL.git
    cd TronHDL
    ```

2. **Install TronHDL via pip**

    ```bash
    pip install .
    ```

3. **Install Icarus Verilog**

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
