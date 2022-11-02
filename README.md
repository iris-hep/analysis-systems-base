# analysis-systems-base
Base Docker image for Analysis Systems environment

## Get image

```
docker pull hub.opensciencegrid.org/iris-hep/analysis-systems-base:latest
```

## Usage

### Running as root

```
docker run --rm -ti -p 8888:8888 hub.opensciencegrid.org/iris-hep/analysis-systems-base:latest
```

### Running as non-root user

```
docker run --rm -ti -p 8888:8888 --user $(id -u $USER):$(id -g) hub.opensciencegrid.org/iris-hep/analysis-systems-base:latest
```
