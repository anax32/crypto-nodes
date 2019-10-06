ARG BASE_IMAGE=anax32/python-zmq
FROM $BASE_IMAGE

RUN pip3 install --no-cache-dir \
      requests \
      awscli

COPY ./getchaininfo.py /usr/local/bin/getchaininfo.py
COPY ./getrawtransaction.py /usr/local/bin/getrawtransaction.py

# default run command

ENV PYTHONUNBUFFERED 1

CMD ["python3", "-u", "/usr/local/bin/getchaininfo.py"]

