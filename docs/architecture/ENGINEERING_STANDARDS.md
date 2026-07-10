# Engineering Standards & Best Practices

## 1. SOLID Principles

### Single Responsibility Principle (SRP)

Each class has ONE reason to change.

**✅ Good**
```python
class ConversationService:
    """Manages conversation lifecycle only"""
    async def create_conversation(self): ...
    async def add_message(self): ...
    async def get_messages(self): ...

class ConversationMemoryManager:
    """Manages memory policy only"""
    async def apply_trim(self): ...
    async def summarize(self): ...
```

**❌ Bad**
```python
class ConversationManager:
    # Does TOO much: persistence, memory, search, generation
    def create(): ...
    def trim_memory(): ...
    def retrieve_documents(): ...
    def generate_response(): ...
```

**Application**: Each service in `app/` should have ONE domain responsibility.

---

### Open/Closed Principle (OCP)

Open for extension, closed for modification.

**✅ Good**
```python
class Reranker(ABC):
    @abstractmethod
    async def rerank(self, request: RerankRequest) -> RerankResult:
        pass

class CrossEncoderReranker(Reranker):
    async def rerank(self, ...):
        # New implementation without changing Reranker
        pass
```

**❌ Bad**
```python
class RerankerService:
    if reranker_type == "cross_encoder":
        # ...
    elif reranker_type == "lm_judge":
        # ...
    # Need to modify this file for new reranker
```

**Application**: Use abstract base classes for plugins (rerankers, search strategies, providers).

---

### Liskov Substitution Principle (LSP)

Subclasses must be substitutable for their base class.

**✅ Good**
```python
class EmbeddingProvider(ABC):
    async def generate(self, request: EmbeddingRequest) -> EmbeddingResponse:
        pass

class OpenAIEmbeddings(EmbeddingProvider):
    # Can be used anywhere EmbeddingProvider is expected
    async def generate(self, ...): ...

class GeminiEmbeddings(EmbeddingProvider):
    # Can be used anywhere EmbeddingProvider is expected
    async def generate(self, ...): ...
```

**❌ Bad**
```python
class WeirdEmbeddings(EmbeddingProvider):
    # Returns dict instead of EmbeddingResponse
    # Breaks contract, not truly substitutable
    def generate(self, ...): return {}
```

**Application**: All provider implementations must be interchangeable.

---

### Interface Segregation Principle (ISP)

Don't force clients to depend on interfaces they don't use.

**✅ Good**
```python
class VectorStore(ABC):
    @abstractmethod
    async def search(self, ...): pass

class FullTextSearch(ABC):
    @abstractmethod
    async def search(self, query: str): pass

# Client only depends on what it needs
class HybridSearch:
    def __init__(self, vector_store: VectorStore, keyword_search: FullTextSearch):
        pass
```

**❌ Bad**
```python
class SearchService(ABC):
    # Too broad, clients forced to implement everything
    @abstractmethod
    async def vector_search(self): pass
    @abstractmethod
    async def keyword_search(self): pass
    @abstractmethod
    async def rerank(self): pass
    @abstractmethod
    async def cache(self): pass
```

**Application**: Break large interfaces into focused, segregated ones.

---

### Dependency Inversion Principle (DIP)

Depend on abstractions, not concretions.

**✅ Good**
```python
class RagService:
    def __init__(self, 
                 hybrid_search: HybridSearch,  # Abstract
                 ai_service: AIService,  # Abstract
                 vector_store: VectorStore):  # Abstract
        pass
```

**❌ Bad**
```python
class RagService:
    def __init__(self):
        self.search = OpenAISearch()  # Concrete
        self.ai = OpenAIService()  # Concrete
        self.store = PineconeVectorStore()  # Concrete
```

**Application**: Inject dependencies; never create concrete instances directly.

---

## 2. Clean Architecture

```
Domain Layer (Entities, Use Cases)
    ↕
Application Layer (Services, DTOs)
    ↕
Infrastructure Layer (Repositories, External Services)
    ↕
Interface Layer (API, CLI)
```

### Layer Responsibilities

**Domain Layer** (`app/domain/`)
- Business logic (enterprise rules)
- Entities (Conversation, Message)
- Value Objects (MessageRole, ConversationPolicy)
- NO external dependencies

**Application Layer** (`app/services/`, `app/orchestration/`)
- Use cases (ChatService, RagService)
- Business orchestration
- DTOs for request/response
- Minimal dependencies (only domain + infrastructure interfaces)

**Infrastructure Layer** (`app/vectorstore/`, `app/embeddings/`, `app/providers/`)
- External service integration
- Database/cache access
- File system operations
- Concrete implementations

**Interface Layer** (`app/api/`, `app/middleware/`)
- HTTP endpoints
- Request/response serialization
- API documentation
- Middleware

**Key Rule**: Dependencies only flow INWARD. The API layer depends on services, which depend on domain.

---

## 3. Async/Await Patterns

### Rule 1: All I/O is async

```python
# ✅ Good
async def search(self, query: str) -> list[Document]:
    results = await self.vector_service.search(query)
    return results

# ❌ Bad - blocks event loop
def search(self, query: str) -> list[Document]:
    results = self.vector_service.search(query)  # Synchronous
    return results
```

### Rule 2: Never block in async

```python
# ✅ Good - uses async-compatible library
async def process(self, items: list[str]):
    tasks = [self.process_one(item) for item in items]
    results = await asyncio.gather(*tasks)
    return results

# ❌ Bad - blocks event loop
async def process(self, items: list[str]):
    results = []
    for item in items:
        results.append(await self.process_one(item))  # Sequential
    return results
```

### Rule 3: Use context managers for resources

```python
# ✅ Good
async with VectorStore() as store:
    results = await store.search(query)
    # Cleanup happens automatically

# ❌ Bad - resource leak
store = VectorStore()
results = await store.search(query)
# Forget to cleanup
```

---

## 4. Testing Strategy

### Test Pyramid

```
      /\
     /  \  E2E Tests (5%)
    /    \
   /______\
   /\      \
  /  \      \  Integration Tests (20%)
 /    \      \
/______\      \
/\      \      \
  \  Unit   \  Unit Tests (75%)
   \Tests    \
    \        \
```

### Unit Tests
- Test single functions/methods in isolation
- Use mocks for external dependencies
- Fast execution (ms)
- 70-80% coverage target

```python
def test_context_builder_formats_documents():
    # Arrange
    documents = [RetrievedDocument(...)]
    builder = ContextBuilder()
    
    # Act
    context = builder.build(documents)
    
    # Assert
    assert "Document 1" in context
    assert document.text[:1000] in context
```

### Integration Tests
- Test multiple components together
- Use test fixtures (test database, test vector store)
- Real I/O but against test services
- Seconds execution time
- 15-25% coverage target

```python
@pytest.mark.asyncio
async def test_rag_service_with_real_search():
    # Setup
    search_service = HybridSearch(test_vector_store, test_keyword_search)
    rag_service = RagService(search_service, test_ai_service)
    
    # Index test documents
    await search_service.index_documents(test_docs)
    
    # Execute
    result = await rag_service.ask(RagRequest(...))
    
    # Verify
    assert len(result.sources) > 0
```

### E2E Tests
- Test full workflow through API
- Real services (staging)
- Minutes execution time
- 5-10% coverage target

```python
@pytest.mark.asyncio
async def test_chat_flow_e2e(client: AsyncClient):
    # Create conversation
    response = await client.post("/conversations", json={...})
    conversation_id = response.json()["id"]
    
    # Send message
    response = await client.post(
        f"/conversations/{conversation_id}/messages",
        json={"content": "Who am I?"}
    )
    
    # Verify response
    assert response.status_code == 200
    assert len(response.json()["response"]) > 0
```

### Coverage Targets by Module
- Core domain: 90%+ (ConversationService, RagService)
- Utilities: 70%+ (search, embeddings)
- API layers: 50%+ (routers, schemas)

---

## 5. Documentation Standards

### Code Documentation
- Every public class has docstring
- Every public method has docstring with Args/Returns
- Complex logic has inline comments
- Links to ADRs for architectural decisions

```python
class HybridSearch:
    """
    Combines vector similarity and keyword search using rank fusion.
    
    Implements: ADR-003: Hybrid Search Strategy
    
    This approach improves retrieval accuracy by 10-15% compared to
    single-method retrieval while remaining extensible for future
    ranking strategies.
    """
    
    async def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[SearchResult]:
        """
        Execute hybrid search on indexed documents.
        
        Args:
            query: Search query string
            top_k: Number of results to return
            
        Returns:
            List of SearchResult objects ranked by relevance
            
        Raises:
            SearchIndexNotInitializedError: If index not populated
            QueryValidationError: If query is empty
        """
        pass
```

### API Documentation
- OpenAPI/Swagger documentation
- Request/response examples
- Error codes with explanations

---

## 6. Code Review Checklist

- [ ] Follows SOLID principles
- [ ] Has tests (unit + integration)
- [ ] Documentation updated
- [ ] No hardcoded values/credentials
- [ ] Error handling proper
- [ ] Async patterns correct
- [ ] Dependency injection used
- [ ] ADR referenced if architecture decision
- [ ] Performance implications considered
- [ ] Security implications reviewed
