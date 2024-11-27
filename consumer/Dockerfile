FROM python:3.9-slim

WORKDIR /app

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY kafka-consumer.py .

CMD ["python", "kafka-consumer.py"]