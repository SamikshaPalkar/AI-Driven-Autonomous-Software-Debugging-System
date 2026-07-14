import ast

def analyze_python_code(code):
    try:
        ast.parse(code)
        return {"status": "success", "message": "No syntax errors"}
    except SyntaxError as e:
        return {
            "status": "error",
            "type": "SyntaxError",
            "line": e.lineno,
            "offset": e.offset,
            "text": e.text.strip() if e.text else "",
            "message": e.msg
        }
