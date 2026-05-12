from prometheus_fastapi_instrumentator import Instrumentator

instrumentator = Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=True,
    should_respect_env_var=True,
    should_instrument_requests_inprogress=True,
    excluded_handlers=["/metrics", "/health", "/health/live", "/health/ready"],
    inprogress_name="geip_inprogress_requests",
    inprogress_labels=True,
)


def setup_metrics(app):
    instrumentator.instrument(app)
