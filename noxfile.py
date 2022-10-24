import shutil
import sys
from pathlib import Path

import nox

ALL_PYTHONS = ["3.8", "3.9", "3.10"]

# Default sessions to run if no session handles are passed
# nox.options.sessions = ["lint", "tests-3.10"]
nox.options.sessions = ["lock"]


DIR = Path(__file__).parent.resolve()

@nox.session(reuse_venv=True)
def lock(session):
    """
    Lint with pre-commit.
    Build a lockfile for the image with conda-lock
    """
    session.install("--upgrade", "conda-lock")
    # session.run("pre-commit", "run", "--all-files", *session.posargs)
