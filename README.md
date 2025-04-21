📦 Kafka Multi-Service Setup with Docker
========================================

This project demonstrates a minimal yet complete Apache Kafka setup using Docker Compose, featuring multiple interconnected services:

- Kafka Broker (in KRaft mode, no ZooKeeper)
- Python Producer
- Python Consumer

All services are connected via a shared Docker bridge network.

🧩 Services Overview
--------------------

🔹 broker
- Runs Apache Kafka using KRaft mode (no ZooKeeper).
- Advertises two listeners:
  - PLAINTEXT://broker:29092 — for internal Docker communication.
  - PLAINTEXT_HOST://localhost:9092 — for external tools like kafka-console-producer.

🔹 producer
- A Python service that produces messages to Kafka.
- Dynamically determines the correct Kafka bootstrap server:
  - broker:29092 when running inside Docker.
  - localhost:9092 when running outside Docker.
- Includes a built-in Python function to wait until Kafka is ready before sending messages.

🔹 consumer
- A Python service that subscribes to Kafka topics and prints incoming messages.
- Uses the same internal Kafka bootstrap resolution and wait logic as the producer.

🚀 Running the Project
----------------------

Build and start all services with:

    docker-compose up --build

This will:
- Start the Kafka broker
- Run the producer and consumer after verifying Kafka is ready (via internal logic)

🔁 Kafka Communication
----------------------

- Topic configuration is handled automatically in code.
- You can change the topic name via environment variables or code.

🛠 Docker Network
-----------------

All services run on the same custom Docker bridge network, enabling hostname-based discovery (e.g., the broker is accessible as `broker` from within other containers).
