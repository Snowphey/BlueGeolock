FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY kafka-producer.py .
COPY blue_lock_data.json .
COPY u_20_data.json .
COPY bin_data.json .
COPY kcr_data.json .

CMD ["python", "kafka-producer.py"]