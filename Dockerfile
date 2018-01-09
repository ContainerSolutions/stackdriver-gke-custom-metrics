FROM python:3.6.4-stretch

RUN pip install google-cloud-monitoring
RUN pip install kubernetes

WORKDIR /app
COPY metricspush.py /app

CMD python metricspush.py