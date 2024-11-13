FROM python:3.12

WORKDIR /app
COPY publisher.py .

RUN pip install paho-mqtt

CMD ["python", "publisher.py"]
