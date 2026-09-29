"""Repeatable Week 5 release gate. Run from the repository root."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*args):
    print("+", " ".join(args), flush=True)
    subprocess.run(args, cwd=ROOT, check=True)


if __name__ == "__main__":
    run(sys.executable, "-m", "compileall", "-q", "app", "scripts", "tests")
    run(sys.executable, "-m", "pytest", "-q")
    run(sys.executable, "-m", "pytest", "-q", "tests/test_ml_eval.py")
    print("RELEASE GATE: PASS")
