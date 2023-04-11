FROM debian:10
WORKDIR /local
RUN apt-get update -y && \
    apt-get install -y \
      gcc make patchelf wget tar git
RUN wget "https://github.com/Devil666face/ChatGPTosBot/releases/download/v04.11/python-3.10.8-debian10.tgz"
RUN tar -xf python-3.10.8-debian10.tgz && \
    ./bin/python3.10 -m venv venv
COPY build build
CMD ["/local/build"]