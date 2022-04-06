FROM    python:3.6.13-slim-buster

COPY    requirements.txt /
RUN     pip install -r /requirements.txt

COPY    . /src
WORKDIR /src

CMD     python3 app.py