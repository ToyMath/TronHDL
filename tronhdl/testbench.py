import ast

class VerilogTestbenchGenerator(ast.NodeVisitor):
    """
    Generates Verilog testbench code from Python functions.
    """
    def __init__(self, module_name, input_widths=None, output_widths=None):
        self.module_name = module_name
        self.testbench_name = f"tb_{module_name}"
        self.verilog_code = f"module {self.testbench_name};\n\n"
        self.initial_blocks = []
        self.input_widths = input_widths or {}
        self.output_widths = output_widths or {}

    def visit_FunctionDef(self, node):
        for stmt in node.body:
            self.visit(stmt)
        self.generate_verilog()

    def visit_Assign(self, node):
        targets = [self.visit(t) for t in node.targets]
        value = self.visit(node.value)
        for target in targets:
            self.initial_blocks.append(f"    {target} = {value};")

    def visit_Expr(self, node):
        expr = self.visit(node.value)
        if expr:
            self.initial_blocks.append(f"    {expr}")

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name == 'display':
                args = ', '.join([self.visit(arg) for arg in node.args])
                return f'$display({args});'
            elif func_name == 'delay':
                delay_time = self.visit(node.args[0])
                return f'#{delay_time};'
            elif func_name == 'clock':
                period = self.visit(node.args[0])
                return f"""
    always begin
        #{period//2} clk = ~clk;
    end
                """
        return ""

    def visit_Name(self, node):
        return node.id

    def visit_Constant(self, node):
        if isinstance(node.value, str):
            return f'"{node.value}"'
        elif isinstance(node.value, int):
            return str(node.value)
        else:
            return str(node.value)

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        op = self.visit(node.op)
        right = self.visit(node.right)
        return f"({left} {op} {right})"

    def visit_Add(self, node):
        return '+'

    def visit_Sub(self, node):
        return '-'

    def visit_Mult(self, node):
        return '*'

    def visit_Div(self, node):
        return '/'

    def visit_Mod(self, node):
        return '%'

    def visit_Str(self, node):
        return f'"{node.s}"'

    def visit_Num(self, node):
        return str(node.n)

    def generate_verilog(self):
        for inp, width in self.input_widths.items():
            self.verilog_code += f"    reg [{width}-1:0] {inp};\n"
        for outp, width in self.output_widths.items():
            self.verilog_code += f"    wire [{width}-1:0] {outp};\n"
        self.verilog_code += "\n"

        self.verilog_code += f"    // Instantiate the Unit Under Test (UUT)\n"
        self.verilog_code += f"    {self.module_name} uut (\n"
        port_connections = []
        for inp in self.input_widths.keys():
            port_connections.append(f"        .{inp}({inp})")
        for outp in self.output_widths.keys():
            port_connections.append(f"        .{outp}({outp})")
        self.verilog_code += ",\n".join(port_connections)
        self.verilog_code += "\n    );\n\n"

        self.verilog_code += "    initial begin\n"

        self.verilog_code += f"        $dumpfile(\"{self.testbench_name}.vcd\");\n"
        self.verilog_code += f"        $dumpvars(0, {self.testbench_name});\n\n"

        for stmt in self.initial_blocks:
            self.verilog_code += f"{stmt}\n"

        self.verilog_code += "\n        $finish;\n"
        self.verilog_code += "    end\n\n"

        self.verilog_code += "endmodule\n"

    def generate(self):
        return self.verilog_code
