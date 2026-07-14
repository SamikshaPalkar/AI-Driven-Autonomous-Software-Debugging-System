def generate_suggestion(result, code, language):


    if result["status"] == "success":
        return {
            "summary": "No issues detected.",
            "solution": "Your code looks correct!",
            "fixed_code": None
        }

    message = result.get("message", "")
    error_type = result.get("type", "")

    # ======================
    # PYTHON ERROR HANDLING
    # ======================
    if language == "python":
        if error_type == "SyntaxError":
            return {
                "summary": "There is a syntax error in your Python code.",
                "solution": "Check missing brackets, colons, or indentation.",
                "fixed_code": "Try correcting the syntax based on the error message."
            }

        return {
            "summary": "An error occurred while analyzing your Python code.",
            "solution": f"Error details: {message}",
            "fixed_code": None
        }

    # ======================
    # C ERROR HANDLING
    # ======================
    if language == "c":
        if "expected" in message:
            return {
                "summary": "Possible missing semicolon or incorrect syntax.",
                "solution": "Add missing semicolon or correct the line indicated.",
                "fixed_code": "Check the line shown in GCC error output."
            }

        return {
            "summary": "Compiler error detected in your C program.",
            "solution": message,
            "fixed_code": None
        }

    return {"summary": "Unknown error type.", "solution": message, "fixed_code": None}
