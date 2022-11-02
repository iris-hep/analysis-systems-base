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

and then when inside run Jupyter Lab with corresponding options

```
jupyter lab --no-browser --ip 0.0.0.0 --port 8888
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
