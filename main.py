from fastapi import FastAPI
from pydantic import BaseModel
from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

import time
import threading
import random

trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "fake-orders-app"})
    )
)
tracer = trace.get_tracer(__name__)

jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,  
)
span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

app = FastAPI()
FastAPIInstrumentor().instrument_app(app)

class Order(BaseModel):
    order_id: str
    user_id: str
    amount: float

def process_order(order_id: str, user_id: str, amount: float):
    with tracer.start_as_current_span("order_process") as span:
        span.set_attribute("order.id", order_id)
        span.set_attribute("user.id", user_id)
        span.set_attribute("order.amount", amount)

        time.sleep(random.uniform(0.2, 1.0))
        with tracer.start_as_current_span("check_inventory"):
            time.sleep(random.uniform(0.1, 0.4))

        with tracer.start_as_current_span("payment_processing"):
            time.sleep(random.uniform(0.1, 0.4))

@app.get("/order")
def generate_order():
    order_id = f"ord-{random.randint(1000,9999)}"
    user_id = f"user-{random.randint(1,5)}"
    amount = round(random.uniform(10, 500), 2)
    process_order(order_id, user_id, amount)
    return {"order_id": order_id, "user_id": user_id, "amount": amount}

@app.post("/order")
def create_order(order: Order):
    process_order(order.order_id, order.user_id, order.amount)
    return {"status": "order processed", "order": order}

def auto_generate():
    while True:
        try:
            order_id = f"ord-{random.randint(1000,9999)}"
            user_id = f"user-{random.randint(1,5)}"
            amount = round(random.uniform(10, 500), 2)
            process_order(order_id, user_id, amount)
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(5)

threading.Thread(target=auto_generate, daemon=True).start()
