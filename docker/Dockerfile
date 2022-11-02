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
    micromamba shell init --prefix /opt/micromamba --shell bash && \
    /usr/local/bin/micromamba shell init --prefix /opt/micromamba && \
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
    echo 'export  PATH="/opt/micromamba/bin:${PATH}"' >> /etc/.bashrc && \
    echo "micromamba activate analysis-systems" >> /etc/.bashrc && \
    echo 'if [ -f /etc/.bashrc ]; then . /etc/.bashrc; fi' >> /etc/profile && \
    . /etc/.bashrc && \
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
        torch-spline-conv && \
    python -m ipykernel install \
        --name="analysis-systems" \
        --display-name="Analysis Systems" \
        --sys-prefix && \
    rm -rf /root/*

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

# * Make a symbolic link between installation <...>/etc/grid-security and actual directory /etc/grid-security
# * Make "analysis-systems" kernel discoverable to BNL SDCC which has kenerls at /u0b/software/jupyter/kernels/
# * Add build date file to easily check if analysis facilities have synced images
RUN ln --symbolic /opt/micromamba/envs/analysis-systems/etc/grid-security /etc/grid-security && \
    mkdir -p /u0b/software/jupyter/kernels && \
    ln --symbolic /opt/micromamba/envs/analysis-systems/share/jupyter/kernels/analysis-systems /u0b/software/jupyter/kernels/analysis-systems && \
    mkdir -p /.local && \
    chmod 777 /.local && \
    mkdir -p /.jupyter && \
    chmod 777 /.jupyter && \
    mkdir -p /.config && \
    chmod 777 /.config && \
    mkdir -p /.cache && \
    chmod 777 /.cache && \
    mkdir -p /work && \
    chmod 777 /work && \
    printf '#!/bin/bash\n\njupyter lab --no-browser --ip 0.0.0.0 --port 8888\n' > /docker/entrypoint.sh && \
    chmod 777 /docker/entrypoint.sh && \
    echo "# image build date: $(date)" > /docker/build_date.txt

WORKDIR /work

# Run with login shell to trigger /etc/profile
# c.f. https://youngstone89.medium.com/unix-introduction-bash-startup-files-loading-order-562543ac12e9
ENTRYPOINT ["/bin/bash", "-l"]
