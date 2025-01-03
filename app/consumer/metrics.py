from prometheus_client import Counter

transcription_requests = Counter("transcription_requests_total", "Total transcription requests processed")
transcription_errors = Counter("transcription_errors_total", "Total transcription errors")
