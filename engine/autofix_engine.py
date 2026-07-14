import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "deepseek-coder:6.7b"


def auto_fix_code(code, language="Python"):
    """
    GOD LEVEL AI AUTO FIX
    Uses DeepSeek via Ollama to repair code intelligently
    """

    prompt = f"""
You are an expert software debugger.

Fix the following {language} code.

Rules:
- Fix syntax errors
- Fix indentation
- Fix missing brackets
- Fix missing colons
- Fix logic mistakes if obvious
- Do NOT explain
- Return ONLY corrected code

CODE:
{code}
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            }
        )

        data = response.json()
        fixed_code = data.get("response", "").strip()

        return fixed_code if fixed_code else code

    except Exception as e:
        print("AI FIX ERROR:", e)
        return code
