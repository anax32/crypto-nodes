sudo docker run \
  -it \
  --rm \
  -v $(pwd)/database/:/home/jovyan/work/ \
  -p 8888:8888 \
  jupyter/minimal-notebook
