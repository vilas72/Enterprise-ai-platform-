from contextvars import ContextVar

_correlation_id: ContextVar[str | None] = ContextVar(
    "correlation_id",
    default=None,
)


class RequestContext:

    @staticmethod
    def set_correlation_id(correlation_id: str) -> None:
        _correlation_id.set(correlation_id)

    @staticmethod
    def get_correlation_id() -> str | None:
        return _correlation_id.get()

    @staticmethod
    def clear() -> None:
        _correlation_id.set(None)