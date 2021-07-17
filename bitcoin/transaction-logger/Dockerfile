ARG BASE_IMAGE=anax32/python-zmq
FROM $BASE_IMAGE

RUN pip3 install --no-cache-dir \
       pymongo \
       requests \
       boto3

WORKDIR /src

COPY ./src /src

ENV PYTHONUNBUFFERED 1

CMD ["python3", "-u", "zmq_c.py"]
