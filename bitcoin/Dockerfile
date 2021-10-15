ARG BASE_IMAGE=anax32/python-zmq
FROM $BASE_IMAGE as logger

COPY ./txdb /txdb

RUN pip install --no-cache-dir /txdb/package

ENV PYTHONUNBUFFERED 1

CMD ["python3", "-m", "btctx.log"]
