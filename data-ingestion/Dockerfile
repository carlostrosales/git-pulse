FROM python:3.9-slim
WORKDIR /app
COPY . /app/
RUN pip install kafka-python requests
CMD ["python", "send_to_kafka.py"]