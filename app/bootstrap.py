from app.events.dependencies import (
    get_event_registry,
)

from app.events.models.event_type import EventType

from app.reflection.dependencies import (
    get_reflection_engine,
)

from app.reflection.reflection_subscriber import (
    ReflectionSubscriber,
)


def initialize() -> None:

    registry = get_event_registry()

    reflection = ReflectionSubscriber(
        get_reflection_engine(),
    )

    registry.register(
        EventType.RUNTIME_COMPLETED,
        reflection,
    )

    registry.register(
        EventType.RUNTIME_FAILED,
        reflection,
    )

    registry.register(
        EventType.STEP_FAILED,
        reflection,
    )

    registry.register(
        EventType.WORKFLOW_COMPLETED,
        reflection,
    )