import os
import sys
import json
import signal
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.propagators.b3 import B3MultiFormat
from opentelemetry.propagate import extract, set_global_textmap
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Variables
PORT = 8080
OTEL_ENDPOINT = os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT', '').strip('"')

# OTEL Traces initialization
provider = TracerProvider()
set_global_textmap(B3MultiFormat())
otlp_exporter = OTLPSpanExporter(endpoint=OTEL_ENDPOINT)
batch_processor = BatchSpanProcessor(otlp_exporter)
provider.add_span_processor(batch_processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("webapp.custom.main")

def hello_world(headers):
    with tracer.start_as_current_span("hello-world", context=extract(headers)):
        message = "Hello, World! for the webapp!"
        data = {"message": message}
        json_data = json.dumps(data)
        print(json_data, file=sys.stderr)

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = "<html><body><h1>Welcome to Webapp!</h1></body></html>"
            self.wfile.write(bytes(message, "utf8"))
        elif self.path == '/hello':
            hello_world(self.headers)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = "<html><body><h1>Welcome to Hello World!</h1></body></html>"
            self.wfile.write(bytes(message, "utf8"))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = "<html><body><h1>404 Not Found</h1></body></html>"
            self.wfile.write(bytes(message, "utf8"))

def handle_sigterm(*args):
    raise KeyboardInterrupt()

def main():
    signal.signal(signal.SIGTERM, handle_sigterm)
    
    try:
        with HTTPServer(('', PORT), Handler) as httpd:
            print(f"Server running on port {PORT}")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped.")

if __name__ == "__main__":
    main()