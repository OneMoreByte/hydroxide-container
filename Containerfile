FROM golang:alpine AS build

ADD ./hydroxide /go/src/hydroxide
RUN cd /go/src/hydroxide && GO111MODULE=on go build /go/src/hydroxide/cmd/hydroxide

FROM alpine:latest

RUN apk add python3 py3-pexpect

COPY --from=build /go/src/hydroxide/hydroxide /app/hydroxide

ENV PROTONMAIL_USER=""
ENV PROTONMAIL_PASS=""

ENV HYDROXIDE_NO_SMTP="false"
ENV HYDROXIDE_NO_IMAP="false"
ENV HYDROXIDE_NO_CARDDAV="false"

ENV HYDROXIDE_SMTP_HOST="127.0.0.1"
ENV HYDROXIDE_IMAP_HOST="127.0.0.1"
ENV HYDROXIDE_CARDDAV_HOST="127.0.0.1"
ENV HYDROXIDE_SMTP_PORT="1025"
ENV HYDROXIDE_IMAP_PORT="1143"
ENV HYDROXIDE_CARDDAV_PORT="8080"

ENV HYDROXIDE_TLS_CERT=""
ENV HYDROXIDE_TLS_KEY=""
ENV HYDROXIDE_TLS_CLIENT_CA=""

ENV HYDROXIDE_DEBUG="false"


COPY ./entrypoint.py /app/entrypoint
RUN adduser -D -g '' hydroxide
USER hydroxide
WORKDIR /home/hydroxide


ENTRYPOINT ["/app/entrypoint"]
