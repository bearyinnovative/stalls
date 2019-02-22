FROM python:2.7-alpine3.8

ARG build_date
ARG commit
ARG version

ENV WORKSPACE /workspace
ENV PYTHONPATH="$WORKSPACE"
ENV STALLS_HOST="localhost"
ENV STALLS_PORT="5000"
ENV STALLS_GUNICORN_WORKERS="1"
ENV STALLS_BABEL_TRANSLATION_DIRECTORIES="$WORKSPACE/stalls/translations"

RUN mkdir $WORKSPACE
WORKDIR $WORKSPACE

# Generate version and build information
RUN echo "$version" >> $WORKSPACE/version
RUN echo "$commit" >> $WORKSPACE/commit
RUN echo "$build_date" >> $WORKSPACE/build_date

COPY ./entrypoint.sh /entrypoint.sh
COPY ./requirements.txt /tmp/requirements.txt
COPY ./component $WORKSPACE/component
COPY ./stalls $WORKSPACE/stalls
COPY ./deploy $WORKSPACE/deploy


RUN pip install -r /tmp/requirements.txt -i https://pypi.douban.com/simple \
    && pip install gunicorn \
    && chmod +x /entrypoint.sh

RUN echo "*	*	*	*	*	python $WORKSPACE/scripts/cron/notify_expired.py 2>&1 >> $WORKSPACE/cronjob.log" > /etc/crontabs/root

ENTRYPOINT "/entrypoint.sh"
