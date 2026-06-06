from __future__ import annotations

import requests

MODEL = "qwen3.5:9b"
MODEL_CALLS = 0


def ask(prompt: str) -> str:
    global MODEL_CALLS

    try:
        MODEL_CALLS += 1

        r = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        r.raise_for_status()

        data = r.json()

        return data.get("response", "").strip()

    except Exception as e:
        print("OLLAMA ERROR:", e)
        return ""