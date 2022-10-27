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
    """
    session.install("--upgrade", "conda-lock")
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
    session.run("docker", "pull", "centos:centos7", external=True)
    session.run(
        "docker",
        "build",
        "--file",
        "docker/Dockerfile",
        "--tag",
        "iris-hep/analysis-systems-base:latest",
        "--tag",
        f"iris-hep/analysis-systems-base:{current_date}",
        "docker",
        external=True,
    )


@nox.session()
def tag(session):
    """
    Tag images
    """
    for tag in ["latest", datetime.now().strftime("%Y-%m-%d")]:
        session.run(
            "docker",
            "tag",
            f"iris-hep/analysis-systems-base:{tag}",
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
    session.notify("tag")
    session.notify("publish")
