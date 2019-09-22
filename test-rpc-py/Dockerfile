# build the deployable
FROM python:3.7-slim

RUN apt-get update && \
    apt-get install -yq \
       build-essential \
       python3-dev

RUN pip3 install --no-cache-dir \
       pyzmq \
       requests

COPY ./getchaininfo.py /usr/local/bin/getchaininfo.py

# default run command

ENV PYTHONUNBUFFERED 1

CMD ["python3", "-u", "/usr/local/bin/getchaininfo.py"]
