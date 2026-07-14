import subprocess
import json

def ai_autofix(code, language):
    """
    AI Auto-Fix Engine using Ollama DeepSeek-Coder 6.7B
    """

    prompt = f"""
You are an AI Code Fixer.

Fix the following {language} code.
Make the code valid, clean, and runnable.
Do NOT explain, ONLY return fixed code.

CODE:
{code}
"""

    try:
        result = subprocess.run(
            ["ollama", "run", "deepseek-coder:6.7b"],
            input=prompt,
            text=True,
            capture_output=True
        )

        return result.stdout.strip()

    except Exception as e:
        return None
