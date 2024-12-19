from confluent_kafka import Producer
import base64
import os
import json

# Confg
producer_conf = {
    'bootstrap.servers': 'localhost:9092',
    'batch.size': 32768,
    'compression.type': 'lz4'
}

producer = Producer(producer_conf)

image_dir = "task/dataset/labeled dataset"
topic_name = "images-data"

# Callback  
def on_delivery(err, msg):
    if err:
        print(f"Delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# Function to produce image messages
def produce_images(directory, topic):
    for filename in os.listdir(directory):
        if filename.endswith((".jpg")):
            try:
                # Read and encode the image
                filepath = os.path.join(directory, filename)
                with open(filepath, "rb") as image_file:
                    image_data = base64.b64encode(image_file.read()).decode('utf-8')
                
                # Prepare 
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

                producer.poll(0) # Non-blocking
                print(f"Sent: {filename}")

            except Exception as e:
                print(f"Error processing {filename}: {e}")

    producer.flush()
    print("All messages sent.")

# Main execution
if __name__ == "__main__":
    print("Starting Kafka Producer...")
    produce_images(image_dir, topic_name)
    print("Kafka Producer finished.")
