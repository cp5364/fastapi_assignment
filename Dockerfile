
FROM python:alpine3.17 as base
# FROM alpine:3.14 as build

WORKDIR /code

COPY . /code

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN echo '%wheel ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers.d/wheel


ENTRYPOINT ["sh", "/code/entrypoint.sh"]

