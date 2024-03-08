import json
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# OTEL Traces initialization
provider = TracerProvider()
otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317", insecure=True)
batch_processor = BatchSpanProcessor(otlp_exporter)
provider.add_span_processor(batch_processor)

trace.set_tracer_provider(provider)
tracer = trace.get_tracer("my.tracer.something")

def hello_world():
    with tracer.start_as_current_span("hellow-world-span") as span:
        message = "Hello, World! for the webapp!"
        data = {
            "message": message
        }
        json_data = json.dumps(data)
        return json_data

def main():
    print(hello_world())

if __name__ == "__main__":
    main()
