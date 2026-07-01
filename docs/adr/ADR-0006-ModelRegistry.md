# ADR-0006: Model Registry for Provider Metadata

## Status

Accepted

## Date

2026-06-30

## Authors

Enterprise AI Platform Team

## Business Requirement

The platform must expose supported models and providers through a single, authoritative API surface so clients can discover valid provider/model combinations.

## Context

Provider model support is required for request validation, defaults, and API discovery. Without a registry, model metadata can become fragmented across provider implementations or hard-coded in multiple endpoints.

## Decision Drivers

- Centralize supported model metadata.
- Support provider-specific default and streaming capabilities.
- Keep discovery endpoints up to date with implementation support.
- Minimize duplicated model logic across services and routers.

## Decision

Implement a `ModelRegistry` that stores supported models and metadata for each provider. The registry exposes helper methods to list supported providers, provider models, default models, and support checks. The `/providers` API surface uses `ModelRegistry` for discovery.

## Architecture Diagram

```mermaid
flowchart LR
    ModelRegistry[ModelRegistry] --> API[Provider API]
    API --> Clients[Clients]
    Services[Application Services] --> ModelRegistry
```

## Design Patterns

- Registry: exposes shared model metadata.
- Single Source of Truth: keeps provider/model definitions in one module.
- Query API: functions enable discovery without provider-specific logic.

## Alternatives Considered

- Persisting model metadata in a database or external service.
- Using provider SDKs to query supported models at runtime.
- Duplicating metadata across provider classes.

## Consequences

- Supported providers and models are easy to maintain in one place.
- Discovery endpoints remain consistent with implemented support.
- Metadata changes require code updates and redeployment.

## Risks

- The in-memory registry may diverge from actual provider capabilities.
- Hard-coded provider metadata needs updates when new models are released.
- Adding provider-specific settings may require richer metadata support.

## Future Improvements

- Load registry metadata from configuration or feature flags.
- Add model versioning and deprecation metadata.
- Integrate provider capability detection at startup.
- Support provider-specific capability queries (e.g. embeddings, multimodal).

## Related ADRs

- [ADR-0001: Centralize Provider Creation with a Factory](ADR-0001-ProviderFactory.md)
- [ADR-0005: Provider Registry and Bootstrap](ADR-0005-ProviderRegistry.md)

## Related Requirements

- [NFR-EXT-001: Provider extensibility](../architecture/nfr.md#nfr-ext-001-provider-extensibility)
- [NFR-QLT-001: Answer quality](../architecture/nfr.md#nfr-qlt-001-answer-quality)

## Project Improvement

- Provides a stable model discovery API.
- Reduces duplication in validation and default resolution.
- Makes provider model metadata explicit and shareable.
