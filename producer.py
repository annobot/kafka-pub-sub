import os
import asyncio
import socket
from aiokafka import AIOKafkaProducer

# Determine Kafka broker based on environment
kafka_broker = os.getenv('KAFKA_BROKER', 'localhost:9092')  # Default to localhost if not set

host, port = kafka_broker.split(':')

async def wait_for_kafka(host, port, timeout=60):
    print(f"Waiting for Kafka at {host}:{port}...")
    for _ in range(timeout):
        try:
            with socket.create_connection((host, int(port)), timeout=2):
                print("Kafka is up!")
                return
        except OSError:
            await asyncio.sleep(1)
    raise TimeoutError(f"Kafka at {host}:{port} didn't become available in {timeout} seconds")

async def send_message():
    await wait_for_kafka(host, port)
    # Create the Kafka producer
    producer = AIOKafkaProducer(bootstrap_servers=kafka_broker)
    
    # Start the producer
    await producer.start()

    try:
        # Send a test message to the 'test-topic'
        await producer.send_and_wait('test-topic', b'Hello, Kafka!')
        print(f'Connected to Kafka at {kafka_broker} and sent message.')
    finally:
        # Ensure the producer is closed after sending the message
        await producer.stop()

# Run the asynchronous function
loop = asyncio.get_event_loop()
loop.run_until_complete(send_message())
