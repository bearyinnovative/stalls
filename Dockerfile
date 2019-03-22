FROM python:3.7-alpine3.8

ARG build_date
ARG commit
ARG version

ENV WORKSPACE /workspace
ENV PYTHONPATH="$WORKSPACE"
ENV LC_ALL="en_US.UTF-8"
ENV LANG="en_US.UTF-8"
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
COPY ./scripts $WORKSPACE/scripts
COPY ./deploy $WORKSPACE/deploy

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories;\ 
    apk add --no-cache gcc musl-dev linux-headers \
                       build-base cairo-dev cairo cairo-tools \
                       python3-dev mariadb-dev build-base mariadb-connector-c \
                       jpeg-dev zlib-dev freetype-dev \
                       lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
    && pip3 install -r /tmp/requirements.txt -i https://pypi.douban.com/simple \
    && pip3 install gunicorn mysqlclient==1.4.2.post1 \
    && apk del gcc musl-dev linux-headers build-base \
    && chmod +x /entrypoint.sh

RUN echo "*	*	*	*	*	python $WORKSPACE/scripts/cron/notify_expired.py 2>&1 >> $WORKSPACE/cronjob.log" > /etc/crontabs/root

ENTRYPOINT "/entrypoint.sh"
