import os
import asyncio
import socket
from aiokafka import AIOKafkaConsumer

# Kafka configuration
kafka_broker = os.getenv('KAFKA_BROKER', 'localhost:9092')
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

async def consume_messages():
    await wait_for_kafka(host, port)
    # await asyncio.sleep(2)
    # Create Kafka consumer
    consumer = AIOKafkaConsumer(
        'test-topic',  # Topic to consume from
        bootstrap_servers=kafka_broker,
        group_id=None,  # Consumer group
    )

    # Start the consumer
    await consumer.start()

    try:
        print(f"Consumer connected to Kafka at {kafka_broker} and waiting for messages...")
        async for message in consumer:
            print(f"Consumed message: {message.value.decode('utf-8')}")
    finally:
        # Close the consumer after it's done
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(consume_messages())
