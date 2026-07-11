import subprocess

subprocess.run(["git", "reset", "HEAD~1"])
subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", "Deployment configs and UI updates"])
subprocess.run(["git", "push", "origin", "main", "-f"])
