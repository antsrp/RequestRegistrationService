FROM python:3.12.0a2-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install -r requirements.txt

COPY . .

CMD ["python3", "main.py"]
