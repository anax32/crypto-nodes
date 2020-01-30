FROM logstash:7.5.2

USER root

#RUN yum update -y && \
RUN yum install -y \
      gettext && \
    yum clean all

USER logstash

ADD ./pipeline/logstash.conf.template /usr/share/logstash/pipeline/logstash.conf.template

ENV LOGSTASH_CONFIG_TEMPLATE=/usr/share/logstash/pipeline/logstash.conf.template
ENV LOGSTASH_CONFIG=/usr/share/logstash/pipeline/logstash.conf

CMD ["/bin/bash", "-c", "env && envsubst < ${LOGSTASH_CONFIG_TEMPLATE} > ${LOGSTASH_CONFIG} && logstash -f ${LOGSTASH_CONFIG}"]
