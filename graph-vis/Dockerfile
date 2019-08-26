FROM python:3-slim

RUN pip install --no-cache-dir \
          pymongo \
          networkx \
          matplotlib \
          scipy

ADD read-docs-example.py /usr/local/bin/read-docs-example.py
#ADD make-graph.py /usr/local/bin/make-graph.py
