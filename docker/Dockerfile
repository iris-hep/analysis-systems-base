FROM coffeateam/coffea-dask:0.7.19-fastjet-3.3.4.0rc9-ge92ece7 as base

# COPY environment.yml /docker/environment.yml
# COPY conda-lock.yml /docker/conda-lock.yml

COPY environment-full.yml /docker/environment-full.yml
COPY full.conda-lock.yml /docker/conda-lock.yml
# RUN mamba activate base && \
#     mamba env update --file docker/conda-lock.yml
# RUN mamba env update --file /docker/conda-lock.yml
# RUN mamba install --yes conda-lock && \
#     mamba update --yes urllib3 && \
#     conda-lock --version && \
#     conda-lock install \
#         --mamba \
#         /docker/conda-lock.yml

# RUN ls -lhtra /docker/conda-lock.yml && \
#     mamba env update --file /docker/conda-lock.yml

# RUN ls -lhtra /docker/conda-lock.yml && \
#     mamba env update --file /docker/environment.yml && \
#     mamba clean -y --all

RUN mamba install --yes conda-lock && \
    conda-lock install --help && \
    conda-lock install \
        --mamba \
        --name debug \
        /docker/conda-lock.yml

# Make images Singularity compatible
# Make a symbolic link between installation /opt/conda/etc/grid-security and actual directory /etc/grid-security
RUN mkdir -p /opt/conda && \
    ln --symbolic /opt/conda/etc/grid-security /etc/grid-security
