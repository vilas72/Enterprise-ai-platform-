# System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     API Layer (FastAPI)                      │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐   │
│  │ Chat     │ Document │ Embedding│   RAG    │  Health  │   │
│  │ Router   │ Router   │ Router   │ Router   │ Router   │   │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘   │
└─────────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ Conversation │   │     RAG      │   │  Embedding   │
│  Orchestrator│   │  Pipeline    │   │  Service     │
└──────────────┘   └──────────────┘   └──────────────┘
        │                 │                   │
        ▼                 ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ Conversation │   │ Hybrid Search│   │ Vector Store │
│  Service     │   │  (Vector +   │   │              │
│              │   │   Keyword)   │   └──────────────┘
└──────────────┘   └──────────────┘
        │
        ▼
┌──────────────┐
│  AI Service  │
│(Multi-Provider)
└──────────────┘
```

## Component Diagram

### Core Services

1. **Conversation Service**
   - Manages conversation lifecycle
   - Persists messages to store
   - Delegates memory management

2. **RAG Pipeline**
   - Query rewriting (contextual query understanding)
   - Hybrid search (vector + keyword)
   - Reranking
   - Context building

3. **Embedding Service**
   - Generates embeddings via provider
   - Caches results
   - Supports multiple models

4. **AI Service**
   - Multi-provider LLM abstraction
   - Prompt templating
   - Token counting
   - Usage tracking

## Data Flow

### Chat Flow
```
User Message
    │
    ▼
Conversation Manager (persist message)
    │
    ▼
Memory Manager (apply trimming/summarization)
    │
    ▼
Context Builder (gather recent history + memories)
    │
    ▼
RAG Pipeline
    ├─ Query Rewriter (convert follow-up to standalone)
    ├─ Hybrid Search (retrieve relevant docs)
    └─ Reranker (rank top-k results)
    │
    ▼
Prompt Builder (construct system + context + query)
    │
    ▼
AI Service (call LLM provider)
    │
    ▼
Response Parser
    │
    ▼
Conversation Manager (persist response)
    │
    ▼
Return to Client
```

## Technology Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Runtime | Python 3.12 | Performance, ecosystem for AI |
| API Framework | FastAPI | Modern async web framework |
| Async | asyncio + anyio | Native Python async |
| LLM Providers | OpenAI + Google Gemini | Multi-provider flexibility |
| Vector Search | In-memory (Phase 1) → Weaviate/Pinecone (Phase 2) | Scalability path |
| Data Store | In-memory (Phase 1) → PostgreSQL + pgvector (Phase 2) | Production ready |
| Caching | Redis (future) | Response & embedding caching |
| Monitoring | OpenTelemetry | Vendor-neutral observability |
| Testing | pytest + hypothesis | Comprehensive testing |

## Scalability Considerations

### Horizontal Scaling
- **Stateless API servers**: Multiple instances behind load balancer
- **Shared vector store**: Centralized embeddings index
- **Distributed conversation store**: Database-backed storage

### Vertical Scaling
- **Async concurrency**: Handle 1000s of concurrent users per instance
- **Lazy loading**: Load knowledge bases on-demand
- **Caching layers**: Redis for frequent queries

### Cost Optimization
- **Provider selection**: Route queries to cheapest suitable provider
- **Token budgeting**: Enforce per-user/team token limits
- **Retrieval optimization**: Minimize documents sent to LLM

## Security & Compliance

- **API Authentication**: API keys + JWT tokens (future)
- **Rate Limiting**: Per-user, per-team limits
- **Audit Logging**: All interactions logged for compliance
- **Data Retention**: Configurable conversation retention policies
- **RBAC**: Role-based access control (Phase 2)
