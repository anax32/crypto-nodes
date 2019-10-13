FROM python:3-slim

RUN apt-get update && \
    apt-get install -y \
      graphviz \
      libgraphviz-dev \
      pkg-config \
      build-essential

RUN pip install --no-cache-dir \
          pymongo \
          networkx==1.11 \
          matplotlib \
          scipy \
          plotly==2.7.0 \
          pygraphviz

ADD read-docs-example.py /usr/local/bin/read-docs-example.py
ADD make-graph.py /usr/local/bin/make-graph.py

CMD python -m http.server --directory /home/gv/html_serv/ 80
