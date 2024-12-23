from confluent_kafka import Consumer, KafkaError
import base64
import os
import csv
import json
import time

# Kafka Consumer Configuration
consumer_conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'image-data-consumer-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_conf)

output_dir = "task/output_images"
csv_file = "annotations.csv"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

consumer.subscribe(['image-data'])  # Subscribe to the topic

def process_message(msg):
    try:
        # Decode message
        data = json.loads(msg.value().decode('utf-8'))
        image_data = base64.b64decode(data["image"])
        annotation = data["annotation"]

        # Save the image to a file
        image_path = os.path.join(output_dir, annotation.replace(" ", "_") + ".jpg")
        with open(image_path, "wb") as img_file:
            img_file.write(image_data)

        # Append to CSV
        with open(csv_file, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([image_path, annotation])

        print(f"Saved Image: {image_path} with Annotation: {annotation}")
        return True

    except Exception as e:
        print(f"Error processing message: {e}")
        return False

if __name__ == "__main__":
    try:
        # Initialize CSV file
        with open(csv_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Image Path", "Annotation"])  # Write CSV headers

        print("Starting Kafka Consumer...")
        total_messages = 0
        latencies = []
        messages_in_interval = 0
        start_time = time.time()
        interval_start_time = start_time
        log_interval = 10  # Log throughput every 10 seconds

        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f"Consumer error: {msg.error()}")
                    break

            # Measure latency (message consumption time - message production time)
            message_timestamp = msg.timestamp()[1]  # Get the message's timestamp
            if message_timestamp is not None:
                current_time = int(time.time() * 1000)  # Current time in ms
                latency = current_time - message_timestamp
                latencies.append(latency)
                print(f"Latency for message from Partition {msg.partition()}, Offset {msg.offset()}: {latency} ms")

            # Process the message
            if process_message(msg):
                total_messages += 1
                messages_in_interval += 1

            # Log throughput and average latency every `log_interval` seconds
            current_time = time.time()
            if current_time - interval_start_time >= log_interval:
                interval_time = current_time - interval_start_time
                interval_throughput = messages_in_interval / interval_time if interval_time > 0 else 0
                avg_latency = sum(latencies) / len(latencies) if latencies else 0
                print(f"\n✅ Interval Throughput: {interval_throughput:.2f} messages/second (Last {log_interval} seconds)")
                print(f"✅ Average Latency: {avg_latency:.2f} ms (Last {log_interval} seconds)")
                messages_in_interval = 0
                interval_start_time = current_time
                latencies = []

    except KeyboardInterrupt:
        print("Consumer interrupted by user")
    finally:
        end_time = time.time()
        total_time = end_time - start_time
        overall_throughput = total_messages / total_time if total_time > 0 else 0
        avg_latency = sum(latencies) / len(latencies) if latencies else 0
        print(f"\n✅ Overall Consumer Throughput: {overall_throughput:.2f} messages/second")
        print(f"✅ Overall Average Latency: {avg_latency:.2f} ms")
        print(f"✅ Total Messages Consumed: {total_messages}")
        print("Closing Consumer...")
        consumer.close()
