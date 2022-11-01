FROM centos:centos7 as base
# FROM coffeateam/coffea-dask:0.7.19-fastjet-3.3.4.0rc9-ge92ece7 as base

SHELL [ "/bin/bash", "-c" ]

ENV TZ="Etc/UTC"

COPY environment.yml /docker/environment.yml
COPY full.conda-lock.yml /docker/conda-lock.yml
COPY requirements.lock /docker/requirements.lock
COPY requirements.txt /docker/requirements.txt

RUN yum install -y \
      bzip2  && \
    yum clean all && \
    yum autoremove -y && \
    curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj -C /usr/local/bin/ --strip-components=1 bin/micromamba && \
    /usr/local/bin/micromamba shell init -p /opt/micromamba && \
    cp /root/.bashrc /etc/.bashrc && \
    . /etc/.bashrc && \
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
    echo 'export  PATH="/opt/micromamba/bin:${PATH}"' >> /root/.bashrc && \
    echo "micromamba activate analysis-systems" >> /root/.bashrc && \
    cp /root/.bashrc /etc/.bashrc && \
    micromamba activate analysis-systems && \
    rm -rf /opt/micromamba/envs/lock && \
    micromamba env list && \
    micromamba install \
        --channel conda-forge \
        --yes \
            cmake \
            gcc \
            git  && \
    micromamba clean --yes --all && \
    python -m pip --no-cache-dir install --upgrade pip setuptools wheel && \
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

# Make a symbolic link between installation <...>/etc/grid-security and actual directory /etc/grid-security
# Ensure ENTRYPOINT is executable
RUN ln --symbolic /opt/micromamba/envs/analysis-systems/etc/grid-security /etc/grid-security && \
    chmod +x /etc/.bashrc

ENTRYPOINT [ "/etc/.bashrc" ]
