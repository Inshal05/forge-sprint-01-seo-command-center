import requests

def ask(prompt):
    try:
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen3.5:9b",
                "prompt": prompt,
                "stream": False
            },
            timeout=180
        )
        return r.json().get("response", "").strip()
    except:
        return ""