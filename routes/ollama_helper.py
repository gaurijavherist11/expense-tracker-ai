import subprocess

def ask_ollama(prompt):
    result = subprocess.run(
        ["ollama", "run", "llama3.2:3b"],
        input=prompt,
        text=True,
        capture_output=True
    )
    return result.stdout.strip()
