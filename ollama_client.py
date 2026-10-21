"""
Ollama LLM layer. Sends a prompt string, returns the text response.
"""

import sys
import requests
import config


def generate(prompt: str) -> str:
    """
    Send `prompt` to the local Ollama server and return the response text.
    """
    print(f"[Ollama] Sending prompt to {config.OLLAMA_MODEL}...")

    payload = {
        "model": config.OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }

    try:
        resp = requests.post(
            config.OLLAMA_URL,
            json=payload,
            timeout=config.OLLAMA_TIMEOUT,
        )
        resp.raise_for_status()
    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Cannot connect to Ollama.")
        print("Make sure Ollama is running in another terminal: ollama serve")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print(f"\n[ERROR] Ollama timed out after {config.OLLAMA_TIMEOUT}s.")
        print("Try a smaller model: ollama pull llama3.2:1b")
        print("Then set OLLAMA_MODEL = 'llama3.2:1b' in config.py")
        sys.exit(1)

    data = resp.json()
    analysis = data.get("response", "").strip()

    if not analysis:
        raise RuntimeError("Ollama returned an empty response.")

    print("[Ollama] Response received.")
    return analysis