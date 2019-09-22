FROM anax32/python-zmq

RUN pip3 install --no-cache-dir \
      requests

COPY ./getchaininfo.py /usr/local/bin/getchaininfo.py

# default run command

ENV PYTHONUNBUFFERED 1

CMD ["python3", "-u", "/usr/local/bin/getchaininfo.py"]
