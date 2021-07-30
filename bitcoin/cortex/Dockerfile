from python:3-slim

copy requirements.txt /tmp/requirements.txt

run pip install --no-cache-dir -r /tmp/requirements.txt

copy ./src /src
workdir /src

env API_PORT=8080

cmd gunicorn \
      -w 1 \
      -k uvicorn.workers.UvicornH11Worker \
      -b 0.0.0.0:${API_PORT} \
      --access-logfile - \
      cortex.main:app
