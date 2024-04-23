# Python OTEL Example

<pre><code>┌─────────────┐                     ┌─────────────┐
│             │      HTTP 1.1       │             │
│   Client    │───────/hello───────▶│   Webapp    │
│             │                     │             │
└─────────────┘                     └─────────────┘</code></pre>


This Python applications utilizes tracing with a minimal reliance on external libraries, emphasizing core functionality without the need for web frameworks or non-standard library resources, demonstrating how to instrument an application from scratch (OTEL). It also includes Kubernetes manifests for easy deployment. 

Test your OLTP collector by simply using kubectl apply with your clusters.

## OTEL Services implemented
- [x] Tracing
- [-] Metrics
- [-] Logs


## Versions
- Python 3.8
- OTEL Collector 0.95.0

## Usage
### Prerequisites

Before you begin, ensure that you have the following:

- A Kubernetes cluster up and running
- `kubectl` command-line tool installed and configured to connect to your cluster
- `curl` command-line tool installed

### Step 1: Set the OpenTelemetry Endpoint

The first step is to set the environment variable `OTEL_EXPORTER_OTLP_ENDPOINT` to specify the endpoint where the traces will be sent. In this example, we'll set it to `http://observe-traces.observe.svc.cluster.local:4317`.

```shell
export OTEL_EXPORTER_OTLP_ENDPOINT="http://observe-traces.observe.svc.cluster.local:4317"
```

### Step 2: Deploy Client Component

Next, we'll deploy the client component of the Python application. The Kubernetes manifest file for the client component is hosted on GitHub in the `p404/python-otel-example` repository.

```shell
curl -s https://raw.githubusercontent.com/p404/python-otel-example/main/.kustomize/client.yaml | envsubst | kubectl apply -f -
```

This command does the following:
1. It downloads the `client.yaml` manifest file using `curl`.
2. The `envsubst` command substitutes the `OTEL_EXPORTER_OTLP_ENDPOINT` environment variable in the manifest file.
3. The resulting manifest is then applied to the Kubernetes cluster using `kubectl apply -f -`.

### Step 3: Deploy Webapp Component

Similar to the client component, we'll deploy the webapp component of the Python application. The Kubernetes manifest file for the webapp component is also hosted on GitHub in the same repository.

```shell
curl -s https://raw.githubusercontent.com/p404/python-otel-example/main/.kustomize/webapp.yaml | envsubst | kubectl apply -f -
```

This command follows the same steps as the previous one, but it downloads and applies the `webapp.yaml` manifest file.

### One-Liner
```shell
export OTEL_EXPORTER_OTLP_ENDPOINT="http://observe-traces.observe.svc.cluster.local:4317" && \
curl -s https://raw.githubusercontent.com/p404/python-otel-example/main/.kustomize/client.yaml | envsubst | kubectl apply -f - && \
curl -s https://raw.githubusercontent.com/p404/python-otel-example/main/.kustomize/webapp.yaml | envsubst | kubectl apply -f -
```