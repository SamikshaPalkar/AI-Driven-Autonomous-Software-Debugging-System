from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
import os
import io
from datetime import datetime

# ==============================
# ANALYZERS
# ==============================
from analyzers.python_analyzer import analyze_python_code
from analyzers.c_analyzer import analyze_c_code
from analyzers.java_analyzer import analyze_java_code
from analyzers.javascript_analyzer import analyze_js_code

from analyzers.static_analyzer import analyze_python_static, analyze_c_static

# ==============================
# AI ENGINES
# ==============================
from engine.suggestion_engine import generate_suggestion
from engine.autofix_engine import auto_fix_code
from engine.report_generator import generate_report, generate_pdf_report

from ml.bug_classifier import classify_severity

app = Flask(__name__)

# ==============================
# REPORT DIRECTORY
# ==============================
REPORT_DIR = os.path.join(os.getcwd(), "reports")
os.makedirs(REPORT_DIR, exist_ok=True)

# ==============================
# PAGE ROUTES
# ==============================
@app.route("/")
@app.route("/debugger")
def debugger():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/languages")
def languages():
    return render_template("languages.html")

@app.route("/documentation")
def documentation():
    return render_template("documentation.html")

# ==============================
# REPORT LIST PAGE
# ==============================
@app.route("/reports")
def reports_page():
    files = os.listdir(REPORT_DIR)
    files = [f for f in files if f.endswith(".json")]
    return render_template("reports.html", reports=files)

@app.route("/reports/<path:filename>")
def download_report(filename):
    return send_from_directory(REPORT_DIR, filename, as_attachment=True)

# ==============================
# PDF DOWNLOAD
# ==============================
@app.route("/download_pdf", methods=["POST"])
def download_pdf():
    data = request.get_json()

    if not data or "report" not in data:
        return jsonify({"error": "Missing report data"}), 400

    pdf_bytes = generate_pdf_report(data["report"])

    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name="AI_Debug_Report.pdf"
    )

# ==============================
# MAIN ANALYZE ENGINE
# ==============================
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        code = request.form.get("code", "")
        language = request.form.get("language", "")

        if not code.strip():
            return jsonify({"status": "error", "message": "No code provided"}), 400

        # -----------------------------
        # LANGUAGE ANALYSIS
        # -----------------------------
        if language == "Python":
            result = analyze_python_code(code)
            static_issues = analyze_python_static(code)

        elif language == "C":
            result = analyze_c_code(code)
            static_issues = analyze_c_static(code)

        elif language == "Java":
            result = analyze_java_code(code)
            static_issues = []

        elif language == "JavaScript":
            result = analyze_js_code(code)
            static_issues = []

        else:
            return jsonify({"status": "error", "message": "Unsupported language"}), 400

        # -----------------------------
        # SEVERITY ML MODEL
        # -----------------------------
        severity = classify_severity(result, language)

        # -----------------------------
        # AI SUGGESTION ENGINE
        # -----------------------------
        try:
            suggestion = generate_suggestion(result, code, language)
        except:
            suggestion = {"summary": "Suggestion failed", "solution": "", "fixed_code": ""}

        # -----------------------------
        # GOD MODE AUTO FIX (OLLAMA)
        # -----------------------------
        try:
            fixed_code = auto_fix_code(code, language)
        except:
            fixed_code = ""

        # -----------------------------
        # REPORT GENERATION
        # -----------------------------
        report_text = generate_report(
            result=result,
            suggestion=suggestion,
            severity=severity,
            static_issues=static_issues,
            fixed_code=fixed_code
        )

        # -----------------------------
        # SAVE REPORT FILE
        # -----------------------------
        filename = datetime.now().strftime("%Y%m%d_%H%M%S.json")
        filepath = os.path.join(REPORT_DIR, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(report_text)

        # -----------------------------
        # FINAL RESPONSE
        # -----------------------------
        return jsonify({
            "status": "success",
            "analysis": result,
            "severity": severity,
            "static_analysis": static_issues,
            "suggestion": suggestion,
            "auto_fix": fixed_code if fixed_code else "No auto-fix generated",
            "report": report_text
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ==============================
# AUTO FIX ENDPOINT (OPTIONAL)
# ==============================
@app.route("/autofix", methods=["POST"])
def autofix():
    try:
        code = request.form.get("code")
        language = request.form.get("language")

        fixed = auto_fix_code(code, language)

        return jsonify({
            "fixed_code": fixed
        })
    except Exception as e:
        return jsonify({"error": str(e)})

# ==============================
# RUN APP
# ==============================
if __name__ == "__main__":
    app.run(debug=True)
