import ast

def analyze_python_static(code):
    issues = []

    try:
        tree = ast.parse(code)
    except Exception as e:
        issues.append(f"Static parse error: {str(e)}")
        return issues

    # --- Unused variables ---
    assigned = set()
    used = set()

    class Analyzer(ast.NodeVisitor):
        def visit_Name(self, node):
            if isinstance(node.ctx, ast.Store):
                assigned.add(node.id)
            if isinstance(node.ctx, ast.Load):
                used.add(node.id)
            self.generic_visit(node)

        # Detect division by zero
        def visit_BinOp(self, node):
            if isinstance(node.op, ast.Div):
                if isinstance(node.right, ast.Constant) and node.right.value == 0:
                    issues.append("Possible division by zero.")
            self.generic_visit(node)

        # Detect unreachable code
        def visit_FunctionDef(self, node):
            for stmt in node.body:
                if isinstance(stmt, ast.Return):
                    issues.append(f"Unreachable code detected after return in function '{node.name}'.")
            self.generic_visit(node)

    Analyzer().visit(tree)

    unused = assigned - used
    for var in unused:
        issues.append(f"Unused variable detected: '{var}'.")

    return issues


def analyze_c_static(code):
    issues = []
    lines = code.split("\n")

    # Missing header
    if "#include <stdio.h>" not in code:
        issues.append("Missing header: stdio.h")

    # Check missing semicolon (basic)
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped and not stripped.endswith(("{", "}", ";", "#")):
            issues.append(f"Possible missing semicolon at line {i+1}.")

    # Detect infinite loop
    if "while(1)" in code or "while(1){" in code:
        issues.append("Infinite loop detected: while(1)")

    return issues
