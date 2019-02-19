FROM python:2.7-alpine3.8

ENV STALLS_HOST="localhost"
ENV STALLS_PORT="5000"
ENV STALLS_GUNICORN_WORKERS="1"

ENV WORKSPACE /workspace
RUN mkdir $WORKSPACE
WORKDIR $WORKSPACE

COPY ./requirements.txt /tmp/requirements.txt
COPY ./component $WORKSPACE/component
COPY ./stalls $WORKSPACE/stalls
COPY ./deploy $WORKSPACE/deploy

RUN pip install -r /tmp/requirements.txt -i https://pypi.douban.com/simple
RUN pip install gunicorn

ENTRYPOINT ["/usr/local/bin/gunicorn"]

CMD [ "-c", "/workspace/deploy/gunicorn_conf.py", "stalls.wsgi:application" ]
