FROM python:3.10.5-alpine3.16

LABEL description="Dockerizing tz_library project"

ENV PYTHONUNBUFFERED 1

COPY ./project /project
COPY ./requirements.txt /
COPY ./entrypoint.sh /

WORKDIR /project
EXPOSE 8000

RUN apk update && \ 
    apk add gcc && \ 
    apk add musl-dev && \ 
    apk add postgresql-dev && \
    apk add tzdata && \ 
    pip install -r /requirements.txt

ENTRYPOINT ["sh", "/entrypoint.sh"]
