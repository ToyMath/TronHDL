import ast
import os
import subprocess
import textwrap
from functools import wraps
import inspect

from .generator import VerilogGenerator
from .testbench import VerilogTestbenchGenerator

class TronHDL:
    """
    TronHDL: A Python transcompiler for ASICs and FPGAs.
    """

    testbenches = {}

    @staticmethod
    def module(input_width=4, output_width=4):
        """
        Decorator to convert a Python function into a Verilog module.
        Accepts optional input and output bit widths.
        """
        def decorator(func):
            generator = VerilogGenerator(input_width=input_width, output_width=output_width)
            # Retrieve the source code of the function
            try:
                source = inspect.getsource(func)
            except OSError as e:
                raise RuntimeError(f"Could not retrieve source code for function '{func.__name__}': {e}")

            source = textwrap.dedent(source)
            verilog_code = generator.generate_verilog(source)
            module_name = func.__name__
            filename = f"{module_name}.v"
            with open(filename, 'w') as f:
                f.write(verilog_code)
            print(f"Verilog module '{module_name}' has been generated and saved to '{filename}'.")
            print(f"\nGenerated Verilog Code for {module_name}:\n{'-'*40}\n{verilog_code}\n{'-'*40}\n")
            return func
        return decorator

    @staticmethod
    def testbench(module_name, input_widths=None, output_widths=None):
        """
        Decorator to define and save a Verilog testbench for a given module.
        Testbench is written in Python-like syntax and converted to Verilog using AST.
        """
        def decorator(func):
            source = inspect.getsource(func)
            source = textwrap.dedent(source)
            tree = ast.parse(source)

            generator = VerilogTestbenchGenerator(
                module_name=module_name,
                input_widths=input_widths or {},
                output_widths=output_widths or {}
            )
            generator.visit(tree)
            verilog_code = generator.generate()

            filename = f"tb_{module_name}.v"
            with open(filename, 'w') as f:
                f.write(verilog_code)
            TronHDL.testbenches[module_name] = filename
            print(f"Verilog testbench for '{module_name}' has been generated and saved to '{filename}'.\n")
            print(f"Generated Verilog Testbench for {module_name}:\n{'-'*40}\n{verilog_code}\n{'-'*40}\n")
            return func
        return decorator

    @staticmethod
    def run_verilog_simulation(module_name):
        """
        Compiles and runs the simulation for the given module using its testbench.
        """
        verilog_filename = f"{module_name}.v"
        testbench_filename = f"tb_{module_name}.v"
        simulation_output = f"{module_name}_simulation_output.txt"

        if not os.path.exists(verilog_filename):
            print(f"Error: Verilog module file '{verilog_filename}' does not exist.")
            return
        if not os.path.exists(testbench_filename):
            print(f"Error: Testbench file '{testbench_filename}' does not exist.")
            return

        try:
            compile_command = f"iverilog -o tb_{module_name}.vvp {verilog_filename} {testbench_filename}"
            print(f"Compiling {module_name} with testbench...")
            subprocess.run(compile_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            run_command = f"vvp tb_{module_name}.vvp > {simulation_output}"
            print(f"Running simulation for {module_name}...")
            subprocess.run(run_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            with open(simulation_output, 'r') as out_file:
                output = out_file.read()
                print(f"\nSimulation Results for {module_name}:\n{'-'*40}\n{output}\n{'-'*40}\n")

        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running the simulation for module '{module_name}':")
            print(e.stderr.decode())

        finally:
            if os.path.exists(f"tb_{module_name}.vvp"):
                os.remove(f"tb_{module_name}.vvp")
            if os.path.exists(simulation_output):
                os.remove(simulation_output)

    @staticmethod
    def run_all_simulations():
        """
        Runs simulations for all modules that have associated testbenches.
        """
        modules = list(TronHDL.testbenches.keys())
        for module in modules:
            TronHDL.run_verilog_simulation(module)
