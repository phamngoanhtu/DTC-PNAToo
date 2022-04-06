FROM    python:3.6.13-slim-buster

COPY    requirements.txt /
RUN     apt-get update && \
        apt-get install --no-install-recommends --no-install-suggests -y build-essential && \
        rm -rf /var/lib/apt/lists/* && \
        pip install numpy==1.19.4 && \
        pip install -r /requirements.txt && \
        apt-get remove --purge -y build-essential && \
        apt-get autoremove -y

COPY    . /src
WORKDIR /src

CMD     python3 app.py