# DO NOT CHANGE THIS
FROM --platform=linux/amd64 amazonlinux:2 AS base

RUN yum install -y python3

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python3 -m pip install --upgrade pip

# CHANGE THIS TO YOUR REQUIREMENTS
RUN python3 -m pip install \
    great_expectations==0.15.6 \
    venv-pack==0.2.0

# DO NOT CHANGE THIS
RUN mkdir /output && venv-pack -o /output/pyspark_ge.tar.gz

FROM scratch AS export
COPY --from=base /output/pyspark_ge.tar.gz /