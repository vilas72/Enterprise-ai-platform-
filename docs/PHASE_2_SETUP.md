# Phase 2 Development Setup

## Overview

Phase 2 introduces production-ready features including caching, advanced memory management, and fine-tuning capabilities.

## New Modules

### 1. Caching Layer (`app/cache/`)

**Purpose**: Improve performance through intelligent caching of embeddings and search results

**Components**:
- `CacheBackend`: Abstract base for pluggable cache implementations
- `InMemoryCache`: Development/testing implementation
- `RedisCache`: Production implementation (requires `aioredis`)
- `CacheService`: High-level caching API

**Usage**:
```python
from app.cache.cache_service import CacheService
from app.cache.cache_backend import InMemoryCache

cache = CacheService(backend=InMemoryCache())
await cache.cache_embedding("text", [0.1, 0.2, 0.3])
embedding = await cache.get_embedding("text")
```

**Phase 2 Targets**:
- 90% embedding cache hit rate
- <10ms cache lookup time
- 24-hour TTL for embeddings
- 1-hour TTL for search results

### 2. Summarization Module (`app/summarization/`)

**Purpose**: Compress conversation history using LLMs for efficient memory management

**Components**:
- `Summarizer`: Abstract base for summarization strategies
- `TrivialSummarizer`: Simple stats-based summarizer for testing
- `LLMSummarizer`: High-quality LLM-based summarization

**Usage**:
```python
from app.summarization.summarizer import LLMSummarizer

summarizer = LLMSummarizer(ai_service=ai_service)
summary = await summarizer.summarize(messages)
```

**Phase 2 Targets**:
- Reduce conversation memory by 70%
- <100ms summarization latency
- 95%+ information retention

### 3. Fine-Tuning Pipeline (`app/fine_tuning/`)

**Purpose**: Enable domain-specific model adaptation for improved RAG performance

**Components**:
- `FineTuningPipeline`: Job orchestration
- `FineTuningConfig`: Configuration dataclass
- `FineTuningStatus`: Job status enum

**Usage**:
```python
from app.fine_tuning.fine_tuning_pipeline import FineTuningPipeline, FineTuningConfig

pipeline = FineTuningPipeline()
config = FineTuningConfig(
    model_name="gpt-3.5-turbo",
    training_data_path="s3://bucket/data.jsonl",
    epochs=3
)
job_id = await pipeline.submit_job(config)
status = await pipeline.get_status(job_id)
```

**Phase 2 Targets**:
- Support OpenAI fine-tuning API
- Integration with Anthropic Claude fine-tuning (if available)
- Automated evaluation pipelines
- A/B testing framework

## Testing Infrastructure

### Test Organization

```
tests/
├── conftest.py              # Shared pytest configuration
├── fixtures/
│   ├── __init__.py
│   └── conftest.py         # Test fixtures (sample data, services)
├── mocks/
│   ├── __init__.py
│   └── mock_services.py    # Mock implementations
├── unit/
│   ├── __init__.py
│   ├── test_conversation_service.py
│   ├── test_rag_service.py
│   ├── test_cache_service.py
│   ├── test_hybrid_search.py
│   ├── test_embedding_service.py
│   ├── test_summarizer.py
│   └── test_fine_tuning.py
└── integration/
    ├── __init__.py
    ├── test_rag_pipeline.py
    └── test_conversation_workflow.py
```

### Running Tests

```bash
# Install testing dependencies
pip install pytest pytest-asyncio pytest-cov

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run only unit tests
pytest tests/unit/ -v

# Run only integration tests
pytest tests/integration/ -v

# Run with markers
pytest tests/ -m asyncio -v
```

### Test Coverage Targets

| Module | Target | Current |
|--------|--------|---------|
| conversation | 80% | TBD |
| rag | 80% | TBD |
| search | 85% | TBD |
| cache | 90% | TBD |
| summarization | 75% | TBD |
| fine_tuning | 70% | TBD |
| **Overall** | **75%** | TBD |

### Test Categories

**Unit Tests** (70% of tests):
- Individual service methods
- Error handling
- Edge cases
- Mock dependencies

**Integration Tests** (25% of tests):
- End-to-end workflows
- Service interactions
- Data flow verification

**E2E Tests** (5% of tests):
- Full API requests
- Real vector searches
- Document ingestion

## Phase 2 Milestones

### Week 1-2: Caching & Performance
- [ ] Implement Redis cache backend
- [ ] Add cache invalidation strategies
- [ ] Performance benchmarks (<100ms search)
- [ ] Test coverage >90%

### Week 3-4: Memory Management
- [ ] Summarization integration
- [ ] Sliding window memory
- [ ] Token budget tracking
- [ ] Test coverage >80%

### Week 5-6: Fine-Tuning
- [ ] Fine-tuning pipeline setup
- [ ] OpenAI API integration
- [ ] Evaluation metrics
- [ ] Test coverage >70%

### Week 7-8: Database Migration
- [ ] PostgreSQL schema design
- [ ] pgvector integration
- [ ] Migration scripts
- [ ] Performance verification

### Week 9-12: Polish & Deploy
- [ ] Security audit
- [ ] Load testing
- [ ] Documentation updates
- [ ] Staging deployment
- [ ] Production readiness checklist

## Performance Targets

| Metric | Target | Current |
|--------|--------|---------|
| Cache hit rate | 85% | N/A |
| Search latency (p95) | <100ms | ~200ms |
| Embedding generation | <500ms | TBD |
| API response (p95) | <2s | ~1.5s |
| Memory per session | <1MB | ~5MB |
| Uptime | 99.9% | N/A |

## Dependencies

Add to `requirements.txt`:

```
pytest==7.4.0
pytest-asyncio==0.21.0
pytest-cov==4.1.0
aioredis==2.0.1  # Optional, for Redis cache
```

Install with:
```bash
pip install -r requirements.txt
```

## Next Steps

1. **Install pytest dependencies**
   ```bash
   pip install pytest pytest-asyncio pytest-cov
   ```

2. **Run initial test suite**
   ```bash
   pytest tests/ -v --cov=app
   ```

3. **Fix any failing tests**
   - Review error messages
   - Update mocks as needed
   - Fix implementation issues

4. **Add more tests**
   - Target 75% coverage
   - Focus on critical paths
   - Add edge case tests

5. **Performance optimization**
   - Profile bottlenecks
   - Implement caching
   - Optimize queries

6. **Database migration**
   - Design schema
   - Create migration scripts
   - Plan cutover strategy
