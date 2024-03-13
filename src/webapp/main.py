import json
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from http.server import HTTPServer, SimpleHTTPRequestHandler


# Variables
PORT = 8080

# OTEL Traces initialization
provider = TracerProvider()
otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317")
batch_processor = BatchSpanProcessor(otlp_exporter)
provider.add_span_processor(batch_processor)

trace.set_tracer_provider(provider)
tracer = trace.get_tracer("webapp.custom.main")

def hello_world():
    with tracer.start_as_current_span("hello-world") as span:
        message = "Hello, World! for the webapp!"
        data = {
            "message": message
        }
        json_data = json.dumps(data)
        return json_data

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            message = "<html><body><h1>Welcome to Webapp!</h1></body></html>"
            self.wfile.write(bytes(message, "utf8"))
        elif self.path == '/hello':
            hello_world()
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

def main():
    with HTTPServer(('', PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    main()
