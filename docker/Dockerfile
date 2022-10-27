FROM debian:bullseye-slim as base
# FROM coffeateam/coffea-dask:0.7.19-fastjet-3.3.4.0rc9-ge92ece7 as base

SHELL [ "/bin/bash", "-c" ]

ENV DEBIAN_FRONTEND="noninteractive"
ENV TZ="Etc/UTC"

COPY environment.yml /docker/environment.yml
COPY full.conda-lock.yml /docker/conda-lock.yml
COPY requirements.lock /docker/requirements.lock
COPY requirements.txt /docker/requirements.txt

RUN apt-get update && \
    apt-get install -yq --no-install-recommends \
        curl \
        bzip2 \
        libarchive-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    curl -sL micro.mamba.pm/install.sh | bash

# Need to manually source conda.sh for some reason, as `. /root/.bashrc` doesn't work?
RUN . /root/micromamba/etc/profile.d/micromamba.sh && \
    micromamba create --name lock && \
    micromamba activate lock && \
    micromamba env list && \
    micromamba install --channel conda-forge --yes conda-lock && \
    conda-lock install --help && \
    conda-lock install \
        --micromamba \
        --name analysis-systems \
        /docker/conda-lock.yml && \
    micromamba clean --yes --all && \
    echo "micromamba activate analysis-systems" >> /root/.bashrc && \
    conda activate analysis-systems && \
    rm -rf /root/micromamba/envs/lock && \
    micromamba env list && \
    micromamba clean --yes --all && \
    python -m pip --no-cache-dir install --upgrade pip && \
    python -m pip --no-cache-dir install \
        --no-deps \
        --require-hashes \
        --only-binary :all: \
        --no-binary torch-geometric \
        --requirement /docker/requirements.lock && \
    python -m pip --no-cache-dir install \
        --find-links https://data.pyg.org/whl/torch-1.12.1+cpu.html \
        torch-scatter \
        torch-sparse \
        torch-cluster \
        torch-spline-conv

# If need to split into two stages for debugging
# RUN . /opt/conda/etc/profile.d/conda.sh && \
#     conda activate analysis-systems && \
#     conda env remove --name lock && \
#     mamba env list && \
#     python -m pip --no-cache-dir install --upgrade pip && \
#     python -m pip --no-cache-dir install \
#         --no-deps \
#         --require-hashes \
#         --only-binary :all: \
#         --no-binary torch-geometric \
#         --requirement /docker/requirements.lock && \
#     python -m pip --no-cache-dir install \
#         --find-links https://data.pyg.org/whl/torch-1.12.1+cpu.html \
#         torch-scatter \
#         torch-sparse \
#         torch-cluster \
#         torch-spline-conv

# Make images Singularity compatible
# Make a symbolic link between installation /opt/conda/etc/grid-security and actual directory /etc/grid-security
RUN mkdir -p /opt/conda && \
    ln --symbolic /opt/conda/etc/grid-security /etc/grid-security
