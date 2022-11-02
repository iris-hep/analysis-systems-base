# analysis-systems-base
Base Docker image for Analysis Systems environment

## Get image

```
docker pull hub.opensciencegrid.org/iris-hep/analysis-systems-base:latest
```

## Usage

### Running as non-root user

Run the container with configuration options

```
docker run \
    --rm \
    -ti \
    --publish 8888:8888 \
    --user $(id -u $USER):$(id -g) \
    hub.opensciencegrid.org/iris-hep/analysis-systems-base:latest
```

which will then launch Jupyter Lab with corresponding option defaults

```
jupyter lab --no-browser --ip 0.0.0.0 --port 8888
```

#### Running without the defaults

If you just want an interactive shell or need to run with different options then pass in `--` as the `CMD`:

```
docker run \
    --rm \
    -ti \
    --publish 8888:8888 \
    --user $(id -u $USER):$(id -g) \
    hub.opensciencegrid.org/iris-hep/analysis-systems-base:latest --
```

### Running as root

(Not recommended)

```
docker run \
    --rm \
    -ti \
    --publish 8888:8888 \
    hub.opensciencegrid.org/iris-hep/analysis-systems-base:latest
```
