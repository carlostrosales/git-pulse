import json
import gzip
import requests
import time
from kafka import KafkaProducer

# --- config ---
KAFKA_TOPIC = 'gh-events'
KAFKA_BROKER = 'kafka:9092'
ARCHIVE_URL = "https://data.gharchive.org/2024-01-01-0.json.gz"

def main():
    # --- kafka setup ---
    producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    # --- Download, decompress, read/send event to kafka topic
    start_time = time.time()
    print("Downloading archive...")
    response = requests.get(ARCHIVE_URL, stream=True)

    # Opens stream for reading the compressed GZIP file in chunks from a file-like object
    # 'response.raw' is the raw binary stream from an HTTP response (from requests), instead of reading file from disk, reading from the stream (response.raw)
    # use this pattern when downloading from a URL, streaming the content directly (i.e. avoiding saving to disk), or wanting to decompress on the fly
    # as 's' gives access to the uncompressed stream via a variable
    with gzip.GzipFile(fileobj=response.raw) as s:
        count = 0
        for i, line in enumerate(s):
            try:
                event = json.loads(line.decode("utf-8"))
                producer.send(KAFKA_TOPIC, event)
                count += 1
            except Exception as e:
                print("Error:", e)

    producer.flush()
    duration = time.time() - start_time
    print(f"Done sending events to Kafka. Sent {count} events in {duration:.2f} seconds.")

if __name__ == "__main__":
    main()