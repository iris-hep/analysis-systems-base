from datetime import datetime
from pathlib import Path

import nox

# Default sessions to run if no session handles are passed
nox.options.sessions = ["lock"]


DIR = Path(__file__).parent.resolve()


@nox.session(reuse_venv=True)
def lock(session):
    """
    Build a lockfile for the image with conda-lock

    Examples:

        $ nox --session lock
        $ nox --session lock -- pip-tools  # Only build the pip-tools lock file
        $ nox --session lock -- conda-lock  # Only build the conda-lock lock file
    """
    session.install("--upgrade", "conda-lock")

    lock_pip_tools = False
    lock_conda_lock = False
    if not session.posargs:
        lock_pip_tools = True
        lock_conda_lock = True
    if "pip-tools" in session.posargs:
        lock_pip_tools = True
    if "conda-lock" in session.posargs:
        lock_conda_lock = True

    if lock_pip_tools:
        session.run("docker", "pull", "python:3.8", external=True)
        # At the moment this requires a manual intervention to add the hash
        # from https://download.pytorch.org/whl/cpu/ for torch
        session.run(
            "docker",
            "run",
            "--rm",
            "-v",
            f"{DIR}:/build",
            "-w",
            "/build",
            "python:3.8",
            "/bin/bash",
            "docker/compile_dependencies.sh",
            external=True,
        )
        session.run(
            "cp", "docker/_requirements.lock", "docker/requirements.lock", external=True
        )
        session.log("rm docker/_requirements.lock")
        root_controlled_file = DIR / "docker" / "_requirements.lock"
        if root_controlled_file.exists():
            root_controlled_file.unlink()
    if lock_conda_lock:
        # Name lockfile full.conda-lock.yml to avoid name conflicts while still
        # retaining the required '.conda-lock.yml' name ending.
        # TODO: Simplify environment and rename to just .conda-lock.yml.
        session.run(
            "conda-lock",
            "lock",
            "--platform",
            "linux-64",
            "--file",
            "docker/environment.yml",
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
    current_date = datetime.now().strftime("%Y-%m-%d")
    session.run(
        "docker",
        "pull",
        "gitlab-registry.cern.ch/linuxsupport/alma9-base:20230601-2",
        external=True,
    )
    session.run(
        "docker",
        "build",
        "--progress=plain",
        "--file",
        "docker/Dockerfile",
        "--tag",
        "hub.opensciencegrid.org/iris-hep/analysis-systems-base:latest",
        "--tag",
        f"hub.opensciencegrid.org/iris-hep/analysis-systems-base:{current_date}",
        "docker",
        external=True,
    )


@nox.session()
def tag(session):
    """
    Tag images
    """
    for tag in session.posargs:
        session.run(
            "docker",
            "tag",
            "hub.opensciencegrid.org/iris-hep/analysis-systems-base:latest",
            f"hub.opensciencegrid.org/iris-hep/analysis-systems-base:{tag}",
            external=True,
        )


@nox.session()
def publish(session):
    """
    Push images to container registries
    """
    for tag in ["latest", datetime.now().strftime("%Y-%m-%d")]:
        session.run(
            "docker",
            "push",
            f"hub.opensciencegrid.org/iris-hep/analysis-systems-base:{tag}",
            external=True,
        )


@nox.session()
def deploy(session):
    """
    Build, tag, and push to registry
    """
    session.notify("build")
    session.notify("publish")
