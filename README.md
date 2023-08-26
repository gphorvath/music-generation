# Music Gen Experiment

## Description

A dockerized version of [facebook/MusicGen](https://huggingface.co/spaces/facebook/MusicGen) that uses Poetry, FastAPI, and Uvicorn.

## Dependencies

* Cuda version 12
* `cudnn 8`
* `libnccl2`
* Poetry

## Setup

* Ensure you have the above dependencies squared away (nvidia drivers are always fun to setup...)

``` shell
# Configure Poetry Virtual Environment
poetry config virtualenvs.in-project true

poetry install
```

### Run Locally

``` shell
# Start Server
poetry shell # Opens a shell in the Poetry Virtual Environment

uvicorn main:app --reload # Starts the server
```

Navigate to `http://localhost:8000/docs` to verify it works.

### Jupyter Notebook

The `testbed.ipynb` gives you everything you need to test drive the API.

## Docker

``` shell
# Make sure to periodically prune your old images (they can be large)
docker builder prune

docker build . -t music-gen:0.1

docker run -it --rm -p 5000:5000 --gpus all music-gen:0.1 # included in docker-run.sh
```

Navigate to `http://localhost:5000/docs` to verify it works.
