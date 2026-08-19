from prometheus_client import Counter, Histogram, generate_latest
from prometheus_client import CONTENT_TYPE_LATEST


REQUEST_COUNT = Counter(
    "bank_requests_total",
    "Total HTTP requests",
    ["method", "endpoint"]
)

TRANSFER_SUCCESS = Counter(
    "bank_transfer_success_total",
    "Successful bank transfers"
)

TRANSFER_FAILED = Counter(
    "bank_transfer_failed_total",
    "Failed bank transfers"
)

REQUEST_LATENCY = Histogram(
    "bank_request_duration_seconds",
    "HTTP request latency"
)


def get_metrics():
    return generate_latest(), CONTENT_TYPE_LATEST
