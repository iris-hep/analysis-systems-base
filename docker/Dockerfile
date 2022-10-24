FROM coffeateam/coffea-dask:0.7.19-fastjet-3.3.4.0rc9-ge92ece7 as base

COPY environment.yml /tmp/docker/environment.yml
COPY conda-lock.yml /tmp/docker/conda-lock.yml
# RUN mamba activate base && \
#     mamba env update --file docker/conda-lock.yml
# RUN mamba env update --file /tmp/docker/conda-lock.yml
# RUN mamba install --yes conda-lock && \
#     mamba update --yes urllib3 && \
#     conda-lock --version && \
#     conda-lock install \
#         --mamba \
#         /tmp/docker/conda-lock.yml

# RUN ls -lhtra /tmp/docker/conda-lock.yml && \
#     mamba env update --file /tmp/docker/conda-lock.yml

RUN ls -lhtra /tmp/docker/conda-lock.yml && \
    mamba env update --file /tmp/docker/environment.yml

# Make images Singularity compatible
RUN mkdir -p /opt/conda
