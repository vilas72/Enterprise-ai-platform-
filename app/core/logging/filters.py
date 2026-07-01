import logging

from app.core.request_context import RequestContext


class CorrelationIdFilter(logging.Filter):
    """
    Injects the correlation ID from RequestContext into
    every log record.
    """

    def filter(self, record: logging.LogRecord) -> bool:

        correlation_id = RequestContext.get_correlation_id()

        record.correlation_id = (
            correlation_id if correlation_id else "-"
        )

        return True