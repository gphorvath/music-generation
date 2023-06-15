# Music Gen Experiment

## Dependencies

* Cuda version 12
* `cudnn 8`
* `libnccl2`
* Poetry

## Setup

* Ensure you have the above dependencies squared away (nvidia drivers are always fun to setup...)
* `poetry install`

### Run Locally

``` shell
# Start Server
poetry shell # Opens a shell in the Poetry Virtual Environment

uvicorn main:app --reload # Starts the server
```

Now navigate to `http://localhost:8000/docs` to verify it works.

### Docker

``` shell
docker build . -t music-gen:0.1

docker run -it --rm -p 5000:5000 --gpus all music-gen:0.1
```