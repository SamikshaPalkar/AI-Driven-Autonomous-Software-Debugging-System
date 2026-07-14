# analyzers/javascript_analyzer.py

def analyze_js_code(code):
    """
    Simple JavaScript syntax checker (dummy analyzer)
    """

    try:
        # Missing semicolon
        if "console.log" in code and not code.strip().endswith(";"):
            return {
                "status": "error",
                "type": "SyntaxError",
                "message": "Missing semicolon at the end of line.",
                "line": 1
            }

        # Suggest using console.log
        if "console.log" not in code:
            return {
                "status": "warning",
                "type": "Suggestion",
                "message": "Consider using console.log for debugging.",
                "line": 1
            }

        # If code looks good
        return {
            "status": "success",
            "message": "JavaScript code looks valid!"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
