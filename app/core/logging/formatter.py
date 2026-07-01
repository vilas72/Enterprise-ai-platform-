import logging


class EnterpriseFormatter(logging.Formatter):
    """
    Enterprise log formatter.

    Ensures all custom logging attributes exist before formatting.
    This prevents KeyError exceptions if a field has not yet been
    populated by a logging filter.
    """

    DEFAULT_CORRELATION_ID = "-"
    DEFAULT_USER_ID = "-"
    DEFAULT_TENANT_ID = "-"
    DEFAULT_TRACE_ID = "-"

    def format(self, record: logging.LogRecord) -> str:
        """
        Populate custom attributes if they are missing.
        """

        if not hasattr(record, "correlation_id"):
            record.correlation_id = self.DEFAULT_CORRELATION_ID

        if not hasattr(record, "user_id"):
            record.user_id = self.DEFAULT_USER_ID

        if not hasattr(record, "tenant_id"):
            record.tenant_id = self.DEFAULT_TENANT_ID

        if not hasattr(record, "trace_id"):
            record.trace_id = self.DEFAULT_TRACE_ID

        return super().format(record)