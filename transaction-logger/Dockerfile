ARG BASE_IMAGE=anax32/python-zmq
FROM $BASE_IMAGE

RUN pip3 install --no-cache-dir \
       pymongo \
       requests \
       boto3

COPY ./zmq_c.py /usr/local/bin/zmq_c.py
COPY ./textwriter.py /usr/local/bin/textwriter.py
COPY ./mongowriter.py /usr/local/bin/mongowriter.py
COPY ./bitcoindrpc.py /usr/local/bin/bitcoindrpc.py
COPY ./s3_uploader.py /usr/local/bin/s3_uploader.py

# default run command

ENV PYTHONUNBUFFERED 1

CMD ["python3", "-u", "/usr/local/bin/zmq_c.py"]
