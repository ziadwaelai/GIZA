from confluent_kafka import Consumer, KafkaError
import base64
import os
import csv
import json

# config
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

consumer.subscribe(['image-data']) # subscribe to the topic

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
        
        # CSV
        with open(csv_file, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([image_path, annotation])
        
        print(f"Saved Image: {image_path} with Annotation: {annotation}")

    except Exception as e:
        print(f"Error processing message: {e}")





if __name__ == "__main__":
    # Main Consumer Loop
    try:
        with open(csv_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Image Path", "Annotation"])  # Write CSV headers

        print("Starting Kafka Consumer...")
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
            
            process_message(msg)

    except KeyboardInterrupt:
        print("Consumer interrupted by user")

    finally:
        print("Closing Consumer...")
        consumer.close()

