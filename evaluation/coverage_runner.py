from pathlib import Path
import subprocess

def run_coverage(test_dir="tests"):
    try:
        subprocess.run(
            ["coverage", "run", "-m", "pytest", test_dir],
            check=True
        )

        result = subprocess.run(
            ["coverage", "report"],
            capture_output=True,
            text=True
        )

        return result.stdout

    except Exception as e:
        return str(e)