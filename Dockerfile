FROM c0defox/alpine-pylint:latest
ADD . /opt
WORKDIR /opt
ENTRYPOINT ["pylint_runner"]
