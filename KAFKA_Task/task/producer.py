from confluent_kafka import Producer
import base64
import os
import json
import time

# Kafka Producer Configuration
producer_conf = {
    'bootstrap.servers': 'localhost:9092',
    'batch.size': 65536,
    'compression.type': "lz4",
}

producer = Producer(producer_conf)

image_dir = "task/dataset/labeled dataset"
topic_name = "image-data"

# Callback for delivery reports
def on_delivery(err, msg):
    if err:
        print(f"Delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# Function to produce image messages and measure throughput
def produce_images(directory, topic):
    total_messages = 0
    start_time = time.time()

    for filename in os.listdir(directory):
        if filename.endswith(".jpg"):
            try:
                # Read and encode the image
                filepath = os.path.join(directory, filename)
                with open(filepath, "rb") as image_file:
                    image_data = base64.b64encode(image_file.read()).decode('utf-8')

                # Prepare message
                message = {
                    "image": image_data,
                    "annotation": filename.split(".")[0]
                }
                msg = json.dumps(message)

                # Send the message to Kafka
                producer.produce(
                    topic,
                    key=filename.encode('utf-8'),
                    value=msg.encode('utf-8'),
                    callback=on_delivery
                )

                producer.poll(0)  # Non-blocking
                print(f"Sent: {filename}")
                total_messages += 1

            except Exception as e:
                print(f"Error processing {filename}: {e}")

    producer.flush()
    end_time = time.time()

    # Calculate throughput
    total_time = end_time - start_time
    throughput = total_messages / total_time if total_time > 0 else 0
    print(f"\n✅ Producer Throughput: {throughput:.2f} messages/second")
    print("All messages sent.")

# Main execution
if __name__ == "__main__":
    print("Starting Kafka Producer...")
    produce_images(image_dir, topic_name)
    print("Kafka Producer finished.")
