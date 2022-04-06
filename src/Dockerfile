FROM    python:3.6

COPY    requirements.txt /
RUN     apt-get update && \
        apt-get install -y libgl1 libglib2.0-0 libxrender1 libsm6 && \
        pip install -r /requirements.txt

COPY    . /src
WORKDIR /src

CMD     python3.6 app.py