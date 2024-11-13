import ast

class VerilogGenerator(ast.NodeVisitor):
    """
    Generates Verilog code from Python function definitions.
    """
    def __init__(self, input_width=4, output_width=4):
        self.operators = {
            ast.Add: '+',
            ast.Sub: '-',
            ast.Mult: '*',
            ast.Div: '/',
            ast.Mod: '%',
        }
        self.verilog_code = ""
        self.input_width = input_width
        self.output_width = output_width

    def get_operator(self, op):
        return self.operators.get(type(op), None)

    def get_operand(self, node):
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Constant):
            if isinstance(node.value, str):
                return node.value
            else:
                return str(node.value)
        elif isinstance(node, ast.BinOp):
            left = self.get_operand(node.left)
            right = self.get_operand(node.right)
            operator = self.get_operator(node.op)
            if operator is None:
                raise NotImplementedError(f"Operator {type(node.op)} not supported.")
            return f"({left} {operator} {right})"
        else:
            raise NotImplementedError(f"Operand type {type(node)} not supported.")

    def visit_FunctionDef(self, node):
        module_name = node.name
        inputs = []
        outputs = []
        assignments = []

        arg_names = [arg.arg for arg in node.args.args]

        assigned_vars = set()
        for stmt in node.body:
            if isinstance(stmt, ast.Assign):
                for target in stmt.targets:
                    if isinstance(target, ast.Name):
                        assigned_vars.add(target.id)

        inputs = [arg for arg in arg_names if arg not in assigned_vars]
        outputs = list(assigned_vars)

        for stmt in node.body:
            if isinstance(stmt, ast.Assign):
                target = self.get_operand(stmt.targets[0])
                value = self.get_operand(stmt.value)
                assignments.append(f"assign {target} = {value};")

        verilog = f"module {module_name} (\n"
        port_lines = []
        for inp in inputs:
            port_lines.append(f"    input [{self.input_width}-1:0] {inp}")
        for outp in outputs:
            port_lines.append(f"    output [{self.output_width}-1:0] {outp}")
        verilog += ",\n".join(port_lines)
        verilog += "\n);\n\n"

        for assign in assignments:
            verilog += f"    {assign}\n"

        verilog += "\nendmodule\n"

        self.verilog_code += verilog + "\n"

    def generate_verilog(self, python_code):
        tree = ast.parse(python_code)
        self.visit(tree)
        return self.verilog_code
