FROM debian/buster_slim

RUN apt-get update && \
    apt-get upgrade -y \
    apt-get install -y \
      python3

RUN pip install --upgrade pip \
      mysql-connector

ADD ./insert-data.py /usr/local/bin/insert-data.py

ENV PYTHONUNBUFFERED 1

CMD ["python", "-u", "/usr/local/bin/insert-data.py"]
