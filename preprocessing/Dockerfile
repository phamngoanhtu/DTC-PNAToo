FROM    python:3.6.13-slim-buster

COPY    requirements.txt ./

RUN     apt-get update && \
        apt-get install -y libglib2.0-0 libsm6 libxext6 libxrender-dev && \
        pip install -r requirements.txt

COPY    ./ /src
WORKDIR /src

CMD     python3.6 service.py