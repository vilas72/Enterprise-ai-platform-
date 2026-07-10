# Phase 2 Implementation Guide

## Overview

Phase 2 builds on the MVP foundation with production-ready features:
1. **Performance**: Caching layer, optimized search
2. **Memory**: Advanced conversation summarization
3. **Intelligence**: Fine-tuning pipeline for domain adaptation
4. **Persistence**: PostgreSQL + pgvector integration

## Getting Started

### 1. Install Development Dependencies

```bash
# Install testing and development tools
pip install -r requirements-dev.txt

# Verify installation
pytest --version
black --version
```

### 2. Run Existing Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=app --cov-report=html

# Run only unit tests (fast)
pytest tests/unit/ -v

# Run only integration tests
pytest tests/integration/ -v

# Run specific test file
pytest tests/unit/test_conversation_service.py -v

# Run specific test
pytest tests/unit/test_conversation_service.py::test_create_conversation -v
```

### 3. Code Quality Checks

```bash
# Format code
black app/ tests/

# Check formatting without changes
black app/ tests/ --check

# Sort imports
isort app/ tests/

# Lint code
flake8 app/ tests/ --max-line-length=100

# Type checking
mypy app/
```

## Architecture: Phase 2 Modules

### Caching Layer

**File**: `app/cache/`

**Key Classes**:
- `CacheBackend`: Abstract interface for any cache
- `InMemoryCache`: Development (uses dict)
- `RedisCache`: Production (uses Redis)
- `CacheService`: High-level API

**Integration Points**:
- Embedding generation → cache embeddings
- Search queries → cache top-k results
- API responses → optional response caching

**Implementation Checklist**:
- [ ] Add caching to `EmbeddingService.generate()`
- [ ] Add caching to `HybridSearch.search()`
- [ ] Cache invalidation on document update
- [ ] Redis cache backend setup
- [ ] Cache statistics/monitoring

### Summarization Module

**File**: `app/summarization/`

**Key Classes**:
- `Summarizer`: Abstract summarization interface
- `TrivialSummarizer`: Stats-based (testing)
- `LLMSummarizer`: LLM-powered (production)

**Integration Points**:
- Conversation memory management
- Session compression
- Context reduction

**Implementation Checklist**:
- [ ] Integrate with `ConversationMemoryManager`
- [ ] Create memory sliding window
- [ ] Implement token budgeting
- [ ] Add summarization tests
- [ ] Performance benchmarking

### Fine-Tuning Pipeline

**File**: `app/fine_tuning/`

**Key Classes**:
- `FineTuningPipeline`: Job orchestration
- `FineTuningConfig`: Configuration
- `FineTuningStatus`: Status tracking

**Integration Points**:
- OpenAI fine-tuning API
- Dataset management
- Model versioning
- Evaluation metrics

**Implementation Checklist**:
- [ ] OpenAI fine-tuning API wrapper
- [ ] Training dataset preparation
- [ ] Model evaluation metrics
- [ ] Rollout strategy
- [ ] A/B testing framework

## Testing Strategy

### Test Pyramid

```
     /\
    /  \  E2E Tests (5%)
   /____\
  /      \
 /        \ Integration Tests (25%)
/__________\
/          \
            Unit Tests (70%)
```

### Unit Test Template

```python
import pytest
from app.module.service import MyService

@pytest.fixture
def service():
    """Create service instance."""
    return MyService()

def test_feature_success(service):
    """Test happy path."""
    result = service.do_something()
    assert result is not None

def test_feature_error(service):
    """Test error handling."""
    with pytest.raises(ValueError):
        service.do_something_invalid()

@pytest.mark.asyncio
async def test_async_feature(service):
    """Test async operations."""
    result = await service.do_something_async()
    assert result is not None
```

### Integration Test Template

```python
import pytest
from app.service_a import ServiceA
from app.service_b import ServiceB

@pytest.fixture
def workflow():
    """Create full workflow."""
    service_a = ServiceA()
    service_b = ServiceB()
    return service_a, service_b

@pytest.mark.asyncio
async def test_workflow(workflow):
    """Test services working together."""
    service_a, service_b = workflow
    
    result_a = await service_a.process()
    result_b = await service_b.process(result_a)
    
    assert result_b is not None
```

## Development Workflow

### Branch Strategy

```
main (production)
├── develop (staging)
│   ├── feature/caching
│   ├── feature/summarization
│   └── feature/fine-tuning
└── hotfix (production fixes)
```

### Commit Workflow

```bash
# Create feature branch
git checkout -b feature/my-feature develop

# Make changes and commit
git add .
git commit -m "feat: add caching layer"

# Run tests before push
pytest tests/ --cov=app

# Push and create PR
git push origin feature/my-feature
```

### Pull Request Checklist

- [ ] Tests added/updated
- [ ] Code coverage >75%
- [ ] Black formatted
- [ ] No flake8 violations
- [ ] Docstrings added
- [ ] Documentation updated
- [ ] No breaking changes

## Performance Targets & Profiling

### Target Metrics

| Metric | Target | Method |
|--------|--------|--------|
| Cache hit rate | 85%+ | Track in CacheService |
| Search latency (p95) | <100ms | Use `timeit` module |
| Embedding generation | <500ms | Profile EmbeddingService |
| API response (p95) | <2s | Add timing middleware |
| Memory per session | <1MB | Use `memory_profiler` |

### Profiling Tools

```bash
# Install profiler
pip install memory-profiler line_profiler

# Profile memory usage
python -m memory_profiler script.py

# Profile execution time
kernprof -l -v script.py

# Using Python's built-in timeit
python -m timeit -s "import app" "app.service.method()"
```

### Example Profiling Code

```python
import time
from functools import wraps

def time_it(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} took {elapsed:.3f}s")
        return result
    return wrapper

# Usage
@time_it
async def my_function():
    await asyncio.sleep(1)
```

## Common Tasks

### Add a New Test

```bash
# 1. Create test file
touch tests/unit/test_my_service.py

# 2. Write test
# See test template above

# 3. Run test
pytest tests/unit/test_my_service.py -v

# 4. Check coverage
pytest tests/unit/test_my_service.py --cov=app.my_module
```

### Debug a Failing Test

```bash
# Run with verbose output
pytest tests/unit/test_failing.py -vv

# Stop at first failure
pytest tests/unit/test_failing.py -x

# Drop into debugger on failure
pytest tests/unit/test_failing.py --pdb

# Show print statements
pytest tests/unit/test_failing.py -s
```

### Profile Performance Bottleneck

```bash
# 1. Add timing to suspected function
@time_it
async def slow_function():
    # code here

# 2. Run in isolated test
pytest tests/unit/test_slow_function.py -s

# 3. Identify bottleneck from timing output

# 4. Optimize implementation

# 5. Benchmark improvement
pytest tests/unit/test_slow_function.py::test_performance -v
```

## Continuous Integration Setup

### GitHub Actions Workflow

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - run: pip install -r requirements-dev.txt
      - run: pytest tests/ --cov=app --cov-report=xml
      - run: black --check app/ tests/
      - run: flake8 app/ tests/
```

## Troubleshooting

### Tests not running

```bash
# Check pytest is installed
pip install pytest

# Check test discovery
pytest --collect-only tests/

# Run with verbose output
pytest tests/ -vv
```

### Import errors in tests

```bash
# Ensure tests/conftest.py exists
# Ensure app package has __init__.py
# Add workspace to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Async test errors

```bash
# Install pytest-asyncio
pip install pytest-asyncio

# Mark async tests
@pytest.mark.asyncio
async def test_async():
    pass
```

## Next Steps

1. **This Week**:
   - [ ] Install dependencies: `pip install -r requirements-dev.txt`
   - [ ] Run tests: `pytest tests/ -v`
   - [ ] Fix any failing tests
   - [ ] Verify coverage: `pytest tests/ --cov=app`

2. **Next Week**:
   - [ ] Implement caching integration
   - [ ] Add 10+ cache tests
   - [ ] Performance benchmark

3. **Week 3**:
   - [ ] Implement summarization
   - [ ] Add memory management tests
   - [ ] Verify token budgeting

4. **Week 4+**:
   - [ ] Fine-tuning pipeline
   - [ ] Database migration
   - [ ] Production deployment

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-asyncio docs](https://pytest-asyncio.readthedocs.io/)
- [FastAPI testing](https://fastapi.tiangolo.com/advanced/testing/)
- [Python unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
