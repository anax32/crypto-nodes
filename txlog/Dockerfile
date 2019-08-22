# build the deployable
FROM debian:buster-slim

RUN apt-get update && \
    apt-get install -y \
              python3 \
              python3-pip

RUN pip3 install pyzmq

COPY ./zmq_c.py /usr/local/bin/zmq_c.py

# default run command

ENV PYTHONUNBUFFERED 1

CMD ["python3", "-u", "/usr/local/bin/zmq_c.py"]
