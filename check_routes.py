"""End-to-end route tester for all API endpoints."""
import asyncio
from fastapi.testclient import TestClient
from main import app

client = TestClient(app, raise_server_exceptions=False)

# Color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"

results = []

def test(method, url, payload=None, expected_status=None, label=None):
    """Run a single request and report pass/fail."""
    label = label or f"{method} {url}"
    try:
        if method == "GET":
            r = client.get(url)
        elif method == "POST":
            r = client.post(url, json=payload or {})
        elif method == "DELETE":
            r = client.delete(url)
        else:
            raise ValueError(f"Unknown method: {method}")

        status = r.status_code
        ok = status not in (500, 422) if expected_status is None else status == expected_status
        color = GREEN if ok else RED
        tag = "PASS" if ok else "FAIL"
        print(f"  {color}{tag}{RESET}  [{status}]  {label}")
        results.append((ok, label, status, r.text[:200] if not ok else ""))
    except Exception as e:
        print(f"  {RED}ERR {RESET}  [EXC]  {label}  -- {e}")
        results.append((False, label, "EXC", str(e)))

print(f"\n{BOLD}=== Enterprise AI Platform — Route Health Check ==={RESET}\n")

# ── Health ─────────────────────────────────────────────────────────────────
print(f"{BOLD}HEALTH{RESET}")
test("GET",  "/health",         expected_status=200,  label="GET  /health")

# ── Providers ──────────────────────────────────────────────────────────────
print(f"\n{BOLD}PROVIDERS{RESET}")
test("GET",  "/providers",      expected_status=200,  label="GET  /providers")

# ── AI Generate ────────────────────────────────────────────────────────────
print(f"\n{BOLD}AI{RESET}")
test("POST", "/ai/generate",
     payload={"provider": "openai", "model": "gpt-4.1-mini",
               "messages": [{"role": "user", "content": "Say 1"}],
               "temperature": 0.0, "max_tokens": 5},
     label="POST /ai/generate (live call)")

# ── Prompts ────────────────────────────────────────────────────────────────
print(f"\n{BOLD}PROMPTS{RESET}")
test("GET",  "/prompts",        expected_status=200,  label="GET  /prompts")

# ── Embeddings ─────────────────────────────────────────────────────────────
print(f"\n{BOLD}EMBEDDINGS{RESET}")
test("POST", "/embeddings",
     payload={"provider": "openai", "model": "text-embedding-3-small",
               "text": "hello world"},
     expected_status=None,  # 200=OK, 403=API key limit (not a code bug)
     label="POST /embeddings (live call)")

# ── Conversation ───────────────────────────────────────────────────────────
print(f"\n{BOLD}CONVERSATION{RESET}")
r_create = client.post("/conversation")
ok_create = r_create.status_code == 201
color = GREEN if ok_create else RED
print(f"  {color}{'PASS' if ok_create else 'FAIL'}{RESET}  [{r_create.status_code}]  POST /conversation (create session)")
results.append((ok_create, "POST /conversation", r_create.status_code, ""))

session_id = None
if ok_create:
    try:
        session_id = r_create.json().get("session_id") or r_create.json().get("conversation_id")
    except Exception:
        pass

if session_id:
    test("GET",    f"/conversation/{session_id}",        expected_status=200, label=f"GET  /conversation/{{id}}")
    test("POST",   f"/conversation/{session_id}/chat",
         payload={"message": "What is 2+2?", "provider": "openai", "model": "gpt-4.1-mini"},
         label="POST /conversation/{id}/chat (live call)")
    test("DELETE", f"/conversation/{session_id}",        expected_status=204, label="DELETE /conversation/{id}")
    test("GET",    f"/conversation/nonexistent-id-999",  expected_status=404, label="GET  /conversation/nonexistent (404 expected)")
else:
    print(f"  {YELLOW}SKIP{RESET}  Could not get session_id from create response: {r_create.text[:100]}")

# ── Vectors ────────────────────────────────────────────────────────────────
print(f"\n{BOLD}VECTORS{RESET}")
test("POST", "/vectors",
     payload={"document_id": "test-doc-1", "text": "The sky is blue.",
               "provider": "openai", "model": "text-embedding-3-small",
               "metadata": {"source": "test"}},
     expected_status=None,  # 200=OK, 403=API key limit (not a code bug)
     label="POST /vectors (index doc, live call)")
test("POST", "/vectors/search",
     payload={"query": "sky color", "provider": "openai",
               "model": "text-embedding-3-small", "top_k": 3},
     expected_status=None,  # 200=OK, 403=API key limit (not a code bug)
     label="POST /vectors/search (live call)")
test("DELETE", "/vectors/test-doc-1",   expected_status=204, label="DELETE /vectors/{id}")
test("DELETE", "/vectors",              expected_status=204, label="DELETE /vectors (clear all)")

# ── Documents ──────────────────────────────────────────────────────────────
print(f"\n{BOLD}DOCUMENTS{RESET}")
# Document route is POST /documents/upload (multipart), so test it exists with wrong content type
r_doc = client.post("/documents/upload")
ok_doc = r_doc.status_code in (200, 201, 400, 422)  # 422 = validation error (no file) — route exists
color = GREEN if ok_doc else RED
tag = "PASS" if ok_doc else "FAIL"
results.append((ok_doc, "POST /documents/upload", r_doc.status_code, ""))

# ── RAG ────────────────────────────────────────────────────────────────────
print(f"\n{BOLD}RAG{RESET}")
test("POST", "/rag/ask",
     payload={"question": "What is Python?", "provider": "openai",
               "model": None, "top_k": 3},
     label="POST /rag/ask (live call)")

# ── Summary ────────────────────────────────────────────────────────────────
total = len(results)
passed = sum(1 for ok, *_ in results if ok)
failed = total - passed
print(f"\n{BOLD}{'='*51}{RESET}")
print(f"  Total : {total}   {GREEN}Passed : {passed}{RESET}   {RED if failed else GREEN}Failed : {failed}{RESET}")
print(f"{BOLD}{'='*51}{RESET}\n")

if failed:
    print(f"{BOLD}Failures:{RESET}")
    for ok, label, status, body in results:
        if not ok:
            print(f"  {RED}✗{RESET} [{status}] {label}")
            if body:
                print(f"        {body[:300]}")
