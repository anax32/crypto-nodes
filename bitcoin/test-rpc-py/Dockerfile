ARG BASE_IMAGE=anax32/python-zmq
FROM $BASE_IMAGE

RUN pip3 install --no-cache-dir \
      requests

COPY ./getchaininfo.py /usr/local/bin/getchaininfo.py

# default run command

ENV PYTHONUNBUFFERED 1

CMD ["python3", "-u", "/usr/local/bin/getchaininfo.py"]
