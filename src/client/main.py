import sys
import os
import time
import requests
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators.b3 import B3MultiFormat
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Variables
OTEL_ENDPOINT = os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT', '').strip('"')
WEBAPP_ENDPOINT = os.getenv('WEBAPP_ENDPOINT', '').strip('"')
TIME_TO_WAIT = int(os.getenv('TIME_BETWEEN_REQUESTS', '10'))

# OTEL Traces initialization
propagator = B3MultiFormat()
set_global_textmap(B3MultiFormat())
provider = TracerProvider()
otlp_exporter = OTLPSpanExporter(endpoint=OTEL_ENDPOINT)
batch_processor = BatchSpanProcessor(otlp_exporter)
provider.add_span_processor(batch_processor)


trace.set_tracer_provider(provider)
tracer = trace.get_tracer("client.custom.main")

def send_request(endpoint):
    with tracer.start_as_current_span("send-requests"):
        carrier = {}
        propagator.inject(carrier)
        print(carrier)
        requests.get(endpoint, headers=carrier)

def main():
    while True:
        time.sleep(TIME_TO_WAIT)
        hello_endpoint = "{}/hello".format(WEBAPP_ENDPOINT)
        for _ in range(20):
            send_request(hello_endpoint)

if __name__ == "__main__":
    main()
