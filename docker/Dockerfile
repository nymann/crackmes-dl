FROM debian:bookworm AS base-image
RUN apt-get update && useradd -m -u 1000 --shell /bin/bash u
RUN apt-get install --assume-yes --no-install-recommends python3

FROM base-image AS compile-image
RUN apt-get install -y --no-install-recommends make git python3-pip &&\
    pip install --upgrade pip

WORKDIR /usr/app
COPY . .
RUN make install

FROM base-image AS production-image
# RUN python3 -m site # if this ever breaks to get dist-packages folder.
WORKDIR /home/u
RUN mkdir crackmes
VOLUME /home/u/crackmes
COPY --from=compile-image /usr/local/lib/python3.9/dist-packages/ /usr/local/lib/python3.9/dist-packages/
COPY --from=compile-image /usr/local/bin/crackmes_dl /usr/local/bin/

USER u
CMD crackmes_dl download-all --output-dir crackmes
