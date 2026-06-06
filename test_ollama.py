import subprocess

result = subprocess.run(
    ["ollama", "run", "qwen3.5:9b", "hello"],
    capture_output=True,
    text=True,
    timeout=30
)

print("STDOUT:")
print(result.stdout)

print("STDERR:")
print(result.stderr)

print("RETURN CODE:")
print(result.returncode)