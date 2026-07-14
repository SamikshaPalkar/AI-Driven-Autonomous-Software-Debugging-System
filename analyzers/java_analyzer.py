# analyzers/java_analyzer.py

def analyze_java_code(code):
    """
    Simple Java syntax checker (dummy analyzer)
    """

    try:
        # Example: Missing semicolon
        if ";" not in code:
            return {
                "status": "error",
                "type": "SyntaxError",
                "message": "Possible missing semicolon.",
                "line": 1
            }

        # Example: Missing main method
        if "main" not in code:
            return {
                "status": "error",
                "type": "SyntaxError",
                "message": "Missing main() function.",
                "line": 1
            }

        # Example: Missing System.out.println
        if "System.out.println" not in code:
            return {
                "status": "warning",
                "type": "Suggestion",
                "message": "Consider using System.out.println for output.",
                "line": 1
            }

        # If nothing wrong
        return {
            "status": "success",
            "message": "Java code looks valid!"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
