# ADR-0005: Provider Registry and Bootstrap

## Status

Accepted

## Date

2026-06-30

## Authors

Enterprise AI Platform Team

## Business Requirement

The platform must support extensible provider onboarding and a centralized registration flow so new AI providers can be added without changing service-level logic.

## Context

The application has multiple AI provider implementations that must be discoverable and usable by the provider factory. Provider creation is separated from provider registration, and services need a stable provider lookup mechanism independent of provider construction.

## Decision Drivers

- Support pluggable provider implementations.
- Keep provider discovery and registration separate from runtime request handling.
- Enable provider registration once during startup rather than in every service call.
- Maintain a single source of truth for available providers.

## Decision

Use a `ProviderRegistry` class to maintain provider metadata and concrete provider class mappings. A startup bootstrap function, `register_providers()`, registers each supported provider implementation in the registry. The `ProviderFactory` resolves providers through the registry instead of hard-coding provider classes.

## Architecture Diagram

```mermaid
flowchart LR
    Startup[Application Startup] --> Bootstrap[register_providers()]
    Bootstrap --> Registry[ProviderRegistry]
    Client[AIService] --> Factory[ProviderFactory]
    Factory --> Registry
    Registry --> Provider[AIProvider implementations]
```

## Design Patterns

- Registry: stores provider mappings by name and exposes provider lookup.
- Bootstrap: creates a deterministic initialization step that registers known providers.
- Separation of Concerns: separates registration from object creation.

## Alternatives Considered

- Hard-coding provider classes directly in `ProviderFactory`.
- Loading provider mappings from configuration files at runtime.
- Using a dependency injection framework for provider discovery.

## Consequences

- New providers are added by registering them in one bootstrap location.
- Services remain decoupled from provider implementations.
- Global registry state must be initialized before provider creation.
- Provider registration order and side effects become part of startup behavior.

## Risks

- A missing bootstrap call could leave providers unregistered.
- Global registry state can make tests order-dependent.
- Provider registration may hide import-time dependency issues.

## Future Improvements

- Add provider capability metadata to the registry.
- Support dynamic provider registration from plugins or configuration.
- Perform provider registration validation at startup.
- Add provider health and lifecycle management.

## Related ADRs

- [ADR-0001: Centralize Provider Creation with a Factory](ADR-0001-ProviderFactory.md)
- [ADR-0003: Centralized Application Configuration](ADR-0003-Configuration.md)

## Related Requirements

- [NFR-EXT-001: Provider extensibility](../architecture/nfr.md#nfr-ext-001-provider-extensibility)
- [NFR-MNT-001: Maintainability](../architecture/nfr.md#nfr-mnt-001-maintainability)

## Project Improvement

- Simplifies adding new AI providers.
- Ensures runtime provider lookup is uniform across services.
- Removes provider initialization logic from business code.
