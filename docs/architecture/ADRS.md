# Architecture Decision Records (ADRs)

## ADR-001: Multi-Provider LLM Architecture

**Status**: Accepted

**Context**:
- No single AI provider guarantees the best performance across all use cases
- Vendor lock-in risks if tied to single provider
- Different providers have different pricing, latencies, and capabilities

**Decision**:
Implement a provider abstraction layer (`ProviderFactory`) allowing runtime selection of LLM providers (OpenAI, Google Gemini, future providers).

**Consequences**:
- ✅ Flexibility to switch providers or combine multi-provider strategies
- ✅ Better resilience (failover capabilities)
- ✅ Cost optimization (use cheapest appropriate provider)
- ❌ Added complexity in provider management
- ❌ Need to test across multiple providers

**Alternatives Considered**:
1. Single vendor (OpenAI only) - rejected due to lock-in risk
2. Hard-coded routing logic - rejected, less flexible than factory pattern

---

## ADR-002: Async-First Architecture

**Status**: Accepted

**Context**:
- LLM API calls have high latency (500ms - 5s)
- Multiple external services (vector search, embeddings, knowledge bases)
- Enterprise workloads need high concurrency

**Decision**:
Build entire platform with async/await patterns using FastAPI and asyncio. All I/O operations are async.

**Consequences**:
- ✅ Can handle 100s of concurrent users on single instance
- ✅ Better resource utilization (threads freed during I/O wait)
- ✅ Natural backpressure handling
- ❌ Requires async-compatible libraries throughout
- ❌ Different mental model than synchronous code

---

## ADR-003: Hybrid Search (Vector + Keyword)

**Status**: Accepted

**Context**:
- Pure vector search misses exact phrase matches and rare entities
- Pure keyword search misses semantic similarity
- Different domains benefit from different search strategies

**Decision**:
Implement hybrid search combining vector similarity and keyword BM25 with reciprocal rank fusion.

**Consequences**:
- ✅ Better retrieval accuracy (typically 10-15% improvement over single method)
- ✅ Resilient to missing embeddings
- ✅ Handles both semantic and lexical queries
- ❌ Added search latency (sequential scoring)
- ❌ More complex ranking logic

---

## ADR-004: Conversation Session Model

**Status**: Accepted

**Context**:
- Need to maintain conversation state across requests
- Different consumption patterns: single-turn Q&A vs. multi-turn conversations
- Memory constraints require conversation pruning

**Decision**:
Implement immutable `ConversationSession` aggregate with `ConversationMemoryManager` handling trimming and summarization policies.

**Consequences**:
- ✅ Clear separation of concerns (storage vs. memory policy)
- ✅ Flexible memory strategies (auto-trim, sliding window, summarization)
- ✅ Audit-friendly (immutable message history)
- ❌ Need efficient search through conversation history
- ❌ Summarization requires additional LLM calls

---

## ADR-005: Reranking Pipeline

**Status**: Accepted

**Context**:
- Initial retrieval can return 20-50 results
- LLM context windows limit how much context we can include
- Cross-encoder models provide better relevance than embedding models

**Decision**:
Add pluggable reranking layer that can use different strategies (noop, cross-encoder, LLM-as-judge).

**Consequences**:
- ✅ Can improve top-k accuracy by 20-30%
- ✅ Pluggable design allows different strategies for different domains
- ✅ Separates ranking logic from retrieval
- ❌ Additional latency (typically 200-500ms)
- ❌ Requires training or fine-tuning rerankers for domain

---

## ADR-006: Event-Driven Architecture (Future)

**Status**: Proposed

**Context**:
- Conversation lifecycle has multiple stages (creation, message added, summarization needed, etc.)
- Different services need to react to same events
- Scaling challenges with direct coupling

**Decision**:
Migrate to event-driven architecture with event bus (Kafka/Redis) for:
- Conversation events (created, message_added, summarized, archived)
- Search events (indexed, reranked, cached)
- Billing events (token_consumed, cost_calculated)

**Consequences**:
- ✅ Better separation of concerns
- ✅ Easy to add new event listeners without changing core
- ✅ Better scaling (services can process events asynchronously)
- ❌ Eventual consistency challenges
- ❌ Added operational complexity (need event infrastructure)
- ❌ Harder to debug (non-linear event flows)

**Timeline**: Phase 2 (post-MVP)
