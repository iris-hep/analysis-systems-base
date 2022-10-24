import shutil
import sys
from pathlib import Path

import nox

# Default sessions to run if no session handles are passed
nox.options.sessions = ["lock"]


DIR = Path(__file__).parent.resolve()


@nox.session(reuse_venv=True)
def lock(session):
    """
    Build a lockfile for the image with conda-lock
    """
    session.install("--upgrade", "conda-lock")
    # session.run("pre-commit", "run", "--all-files", *session.posargs)
    session.run("conda-lock", "--help")
    session.run("conda-lock", "lock", "--help")
    session.run("conda-lock", "install", "--help")
    # session.run(
    #     "conda-lock",
    #     "lock",
    #     "--platform",
    #     "linux-64",
    #     "--file",
    #     "docker/environment.yml",
    #     "--lockfile",
    #     "docker/conda-lock.yml",
    # )
    # session.run(
    #     "conda-lock",
    #     "lock",
    #     "--platform",
    #     "linux-64",
    #     "--file",
    #     "docker/old-environment.yml",
    #     "--lockfile",
    #     "docker/old-conda-lock.yml",
    # )
    session.run(
        "conda-lock",
        "lock",
        "--platform",
        "linux-64",
        "--file",
        "docker/environment-full.yml",
        "--kind",
        "lock",
        "--lockfile",
        "docker/full.conda-lock.yml",
    )


@nox.session()
def build(session):
    """
    Build image
    """
    session.run(
        "docker",
        "build",
        "--file",
        "docker/Dockerfile",
        "--tag",
        "iris-hep/analysis-systems-base:latest",
        "--tag",
        "iris-hep/analysis-systems-base:2022-10-24",
        "docker",
        external=True
    )
