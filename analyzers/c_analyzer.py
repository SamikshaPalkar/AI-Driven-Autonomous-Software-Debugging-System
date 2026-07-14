import subprocess
import tempfile
import os

def analyze_c_code(code):
    try:
        # Create temporary C file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".c") as tmp:
            tmp.write(code.encode())
            tmp_path = tmp.name

        # Compile using GCC
        compile_cmd = ["gcc", tmp_path, "-o", tmp_path + ".out"]
        process = subprocess.run(compile_cmd, capture_output=True, text=True)

        if process.returncode != 0:
            return {"status": "error", "message": process.stderr}

        return {"status": "success", "message": "C code compiled successfully!"}

    finally:
        # Cleanup temporary files
        try:
            os.remove(tmp_path)
        except:
            pass
