from prometheus_client import Counter, Gauge, Histogram

prices_fetched = Counter(
    "geip_prices_fetched_total",
    "Total number of price fetches",
    ["source", "status"]
)

news_articles = Counter(
    "geip_news_articles_total",
    "Total number of news articles fetched",
    ["source", "status"]
)

cache_hits = Counter(
    "geip_cache_hits_total",
    "Total cache hits",
    ["endpoint"]
)

cache_misses = Counter(
    "geip_cache_misses_total",
    "Total cache misses",
    ["endpoint"]
)

active_alerts = Gauge(
    "geip_active_alerts",
    "Number of active alerts",
    ["severity"]
)

pipeline_runs = Counter(
    "geip_pipeline_runs_total",
    "Total pipeline runs",
    ["layer", "status"]
)

api_request_duration = Histogram(
    "geip_api_request_duration_seconds",
    "API request duration in seconds",
    ["method", "endpoint", "status_code"]
)
