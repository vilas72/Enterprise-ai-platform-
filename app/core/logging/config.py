import logging
import logging.config


def configure_logging(level: str = "INFO") -> None:
    """
    Configure application logging using dictConfig.

    This is the central logging configuration for the
    Enterprise AI Platform.
    """

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,

            "filters": {
                "correlation": {
                    "()": "app.core.logging.filters.CorrelationIdFilter",
                }
            },

            "formatters": {
                "enterprise": {
                    "()": "app.core.logging.formatter.EnterpriseFormatter",
                    "format": (
                        "%(asctime)s | "
                        "%(levelname)-8s | "
                        "%(correlation_id)s | "
                        "%(name)s | "
                        "%(message)s"
                    ),
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                }
            },

            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "enterprise",
                    "filters": ["correlation"],
                    "stream": "ext://sys.stdout",
                }
            },

           "root": {
            "handlers": ["console"],
            "level": level,
           },
        }
    )