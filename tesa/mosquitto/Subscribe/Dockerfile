FROM python:3.8-slim

WORKDIR /app
COPY subscriber.py .

RUN pip install paho-mqtt

CMD ["python", "subscriber.py"]
