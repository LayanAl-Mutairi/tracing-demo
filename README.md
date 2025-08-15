# Distributed Tracing Lab with FastAPI and Jaeger

## Overview

This lab demonstrates how to add distributed tracing to a FastAPI application using OpenTelemetry and visualize the traces using Jaeger.

---

## Project Components

- **FastAPI**: Python web framework for building APIs.
- **OpenTelemetry SDK**: For generating trace data.
- **Jaeger Exporter**: Sends trace data to Jaeger.
- **Jaeger All-in-One Docker Image**: Runs Jaeger agent, collector, and UI.
- **Docker & Docker Compose**: For containerized deployment of app and Jaeger.

---

## Files

- `main.py`: FastAPI application with OpenTelemetry instrumentation.
- `Dockerfile`: Docker image for the FastAPI app.
- `docker-compose.yml`: Defines services for Jaeger and the app.
- `requirements.txt`: Python dependencies.

---

## Prerequisites

- Docker and Docker Compose installed on your machine.
- Python 3.8+ for running locally without Docker.

---

## Setup & Run

1. Build and start the containers:
docker-compose up --build

3. Access FastAPI order endpoint:
http://localhost:8000/order

3. Access Jaeger UI to view traces:
http://localhost:16686


---

## How It Works

- The app is instrumented using OpenTelemetry’s FastAPI instrumentation to automatically trace HTTP requests.

- Custom spans are created for order processing steps: `order_process`, `check_inventory`, and `payment_processing`.

- Traces are sent to the Jaeger agent running as a Docker container.

- Jaeger UI lets you search and visualize traces per service.

---
## Trace Structure Example
Each HTTP request (GET or POST) to /order generates a trace that looks like this in Jaeger UI:

```mermaid
graph TD
    A[HTTP Request: GET/POST /order]
    A --> B[Span: order_process]
    B --> B1[order.id: "ord-1234"]
    B --> B2[user.id: "user-3"]
    B --> B3[order.amount: 276.45]
    B --> C[Span: check_inventory<br/>Time spent checking stock]
    B --> D[Span: payment_processing<br/>Time spent handling payment]

This hierarchical view helps visualize the workflow and performance timing of each step in order processing.

---
## Example Request using curl
You can test the POST /order endpoint using the following curl command:

curl -X POST http://localhost:8000/order \
  -H "Content-Type: application/json" \
  -d '{ "order_id": "ord-5678", "user_id": "user-3", "amount": 199.99 }'

---
## Results

  -  Each HTTP request to the /order endpoint generates a trace visible in Jaeger UI under service name fake-orders-app.

  -  Traces include nested spans showing the processing workflow with timestamps and custom attributes such as order ID, user ID, and amount.

  -  The background thread continuously generates fake orders that also appear in the traces for continuous monitoring demonstration

---
    
## Conclusion

This lab shows how to integrate OpenTelemetry tracing with FastAPI and Jaeger. It provides visibility into application workflows and performance, enabling effective debugging and monitoring in distributed systems.

---

## Author
Layan Al-Mutairi
