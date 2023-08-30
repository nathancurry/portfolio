FROM python:3.10
MAINTAINER nathancurry@gmail.com
WORKDIR /autoredis
COPY requirements.txt /autoredis
RUN pip install -U pip && pip install -r requirements.txt
COPY terraform /usr/bin
COPY autoredis-docker.sh /usr/bin
ENTRYPOINT ["autoredis-docker.sh"]
