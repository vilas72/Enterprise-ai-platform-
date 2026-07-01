# ADR-0002: Centralize Application Logging

## Status

Accepted

## Date

2026-06-27

## Authors

Enterprise AI Platform Team

## Business Requirement

Platform operations require consistent, configurable logs for troubleshooting,
monitoring, and future audit integration.

## Context

Services need a shared logging format and level. Creating handlers independently
can duplicate output and make operational behavior inconsistent.

## Decision Drivers

- Consistent log formatting across modules.
- Environment-controlled verbosity.
- Prevention of duplicate handlers.
- Compatibility with standard Python tooling.

## Decision

Use `setup_logger()` as the centralized logger constructor. It reads the log
level from application settings, applies a standard console format, and avoids
adding duplicate handlers to an existing named logger.

## Architecture Diagram

```mermaid
flowchart LR
    Env[Environment] --> Settings[Settings]
    Settings --> Setup[setup_logger]
    Setup --> Logger[Named Logger]
    Logger --> Console[Console Handler]
```

## Design Patterns

- Factory Function: creates consistently configured named loggers.
- Singleton-by-name: Python logging reuses logger instances by name.
- Externalized Configuration: the log level is environment-driven.

## Alternatives Considered

- Module-level `basicConfig()` offers less control over handler composition.
- Provider-specific logging setup would fragment format and levels.
- A third-party logging framework is unnecessary at the current scale.

## Consequences

- Logs share a predictable timestamp, level, logger, and message format.
- Log verbosity changes without source-code edits.
- Current output is console-only and unstructured.

## Risks

- Propagation to root handlers may duplicate messages in some hosts.
- Sensitive provider data could be logged without redaction controls.
- Plain text logs are harder to query at production scale.

## Future Improvements

- Add JSON structured logging and correlation IDs.
- Add secret and prompt redaction.
- Support environment-specific handlers and centralized log collection.
- Define audit logging separately from operational logging.

## Related ADRs

- [ADR-0003: Centralized Configuration](ADR-0003-Configuration.md)

## Related Requirements

- [NFR-OBS-001: Observability](../architecture/nfr.md#nfr-obs-001-observability)
- [NFR-SEC-001: Secret protection](../architecture/nfr.md#nfr-sec-001-secret-protection)

## Project Improvement

- Replaces ad hoc logger setup with one reusable configuration point.
- Prepares the platform for production observability standards.
