def classify_severity(result, language="python"):
    """
    Rule-based ML-style severity classifier.
    """

    if result["status"] == "success":
        return "Info"

    message = result.get("message", "")
    error_type = result.get("type", "") or ""

    # =======================
    # PYTHON SEVERITY LOGIC
    # =======================
    if language == "python":
        if "SyntaxError" in error_type:
            return "Critical"
        if "NameError" in error_type:
            return "Major"
        if "TypeError" in error_type:
            return "Major"
        if "IndentationError" in error_type:
            return "Major"
        if "Warning" in error_type or "deprecated" in message.lower():
            return "Warning"
        return "Minor"

    # =======================
    # C LANGUAGE SEVERITY LOGIC
    # =======================
    if language == "c":
        if "error" in message.lower() and "expected" in message.lower():
            return "Major"
        if "undeclared" in message.lower():
            return "Critical"
        if "warning" in message.lower():
            return "Warning"
        return "Minor"

    return "Info"
