# build the deployable
FROM python:3.7-slim

# FOR RPI WE NEED TO DO SOME APT-GET
RUN apt-get update && \
    apt-get install -qy \
       build-essential \
       python3-dev

# NB: we can't use alpine here because pyzmq needs compiling,
#     there maybe a package in apk called 'py3-zmq' which is
#     ready compiled: check?
RUN pip3 install --upgrade --no-cache-dir \
       pyzmq \
       pymongo \
       requests

COPY ./zmq_c.py /usr/local/bin/zmq_c.py
COPY ./textwriter.py /usr/local/bin/textwriter.py
COPY ./mongowriter.py /usr/local/bin/mongowriter.py
COPY ./bitcoindrpc.py /usr/local/bin/bitcoindrpc.py

# default run command

ENV PYTHONUNBUFFERED 1

CMD ["python3", "-u", "/usr/local/bin/zmq_c.py"]
