# build the deployable
# FIXME: we use pyzmq in a few places, so make a base-image
FROM python:3.7-alpine

RUN apk update && \
    apk add --no-cache --virtual build-dependencies \
      g++ \
      python3-dev \
      zeromq-dev \
      linux-headers \
    && \
    python3 -m pip install --no-cache-dir \
      pyzmq \
      requests \
    && \
    apk del build-dependencies

RUN pip3 install --no-cache-dir \
       pyzmq \
       requests

COPY ./getchaininfo.py /usr/local/bin/getchaininfo.py

# default run command

ENV PYTHONUNBUFFERED 1

CMD ["python3", "-u", "/usr/local/bin/getchaininfo.py"]
