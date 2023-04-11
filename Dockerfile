FROM debian:10
WORKDIR /local
RUN apt-get update -y && \
    apt-get install -y \
      gcc make patchelf wget tar git
RUN git clone "https://github.com/Devil666face/ChatGPTosBot.git"
RUN wget "https://github.com/Devil666face/ChatGPTosBot/releases/download/v04.11/python-3.10.8-debian10.tgz"
RUN tar -xf python-3.10.8-debian10.tgz && \
    ./bin/python3.10 -m venv venv && \
    ./venv/bin/pip install -r ChatGPTosBot/requirements.txt
CMD ["./venv/bin/python","-m","nuitka","--standalone","--onefile","--follow-imports","ChatGPTosBot/main.py","&&","mkdir build","&&","mv main.bin build/"]