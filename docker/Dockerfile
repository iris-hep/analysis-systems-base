FROM coffeateam/coffea-dask:0.7.19-fastjet-3.3.4.0rc9-ge92ece7 as base

COPY conda-lock.yml /tmp/docker/conda-lock.yml
# RUN mamba activate base && \
#     mamba env update --file docker/conda-lock.yml
# RUN mamba env update --file /tmp/docker/conda-lock.yml
RUN mamba install --yes conda-lock && \
    conda-lock install \
        --mamba \
        --name base \
        /tmp/docker/conda-lock.yml

# Make images Singularity compatible
RUN mkdir -p /opt/conda
