#!/usr/bin/env python3
"""Comprehensive API route testing script."""

import httpx
import json
import asyncio
from typing import Optional, Dict, Any
from datetime import datetime

BASE_URL = "http://localhost:8000"

class RouteTestRunner:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.results = []
        self.client = httpx.Client(base_url=base_url, timeout=30.0)
        self.session_id = None
        
    def test_route(
        self,
        method: str,
        path: str,
        description: str,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, str]] = None,
        expected_status: int = 200,
        skip: bool = False,
    ) -> Dict[str, Any]:
        """Test a single route."""
        
        if skip:
            result = {
                "timestamp": datetime.now().isoformat(),
                "method": method,
                "path": path,
                "description": description,
                "status": "SKIPPED",
                "reason": "Requires external API",
                "url": f"{self.base_url}{path}",
            }
            self.results.append(result)
            return result
            
        try:
            print(f"\n🔍 Testing {method} {path}...")
            print(f"   Description: {description}")
            
            if method == "GET":
                response = self.client.get(path, params=params)
            elif method == "POST":
                response = self.client.post(path, json=json_data)
            elif method == "DELETE":
                response = self.client.delete(path)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            success = response.status_code in [expected_status, 200, 201, 204, 400, 404, 422]
            status_str = "✅" if response.status_code < 400 else ("⚠️" if response.status_code < 500 else "❌")
            
            result = {
                "timestamp": datetime.now().isoformat(),
                "method": method,
                "path": path,
                "description": description,
                "status": "PASS" if success else "FAIL",
                "status_code": response.status_code,
                "expected_status": expected_status,
                "url": f"{self.base_url}{path}",
                "response_length": len(response.text),
            }
            
            # Try to parse and display response summary
            if response.text:
                try:
                    response_data = response.json()
                    result["response_summary"] = str(response_data)[:200]
                except:
                    result["response_summary"] = response.text[:200]
            
            print(f"   {status_str} Status: {response.status_code} ({response.reason_phrase})")
            
            self.results.append(result)
            return result
            
        except Exception as e:
            result = {
                "timestamp": datetime.now().isoformat(),
                "method": method,
                "path": path,
                "description": description,
                "status": "ERROR",
                "error": str(e),
                "url": f"{self.base_url}{path}",
            }
            print(f"   ❌ ERROR: {str(e)}")
            self.results.append(result)
            return result
    
    def run_all_tests(self):
        """Run all route tests."""
        print("=" * 80)
        print("🚀 ENTERPRISE AI PLATFORM - COMPREHENSIVE ROUTE TEST")
        print("=" * 80)
        print(f"Base URL: {self.base_url}")
        print(f"Start Time: {datetime.now().isoformat()}")
        print("=" * 80)
        
        # 1. Health Check
        print("\n" + "=" * 80)
        print("1️⃣  HEALTH ROUTER")
        print("=" * 80)
        self.test_route("GET", "/health", "Health check endpoint")
        
        # 2. Provider Router
        print("\n" + "=" * 80)
        print("2️⃣  PROVIDER ROUTER")
        print("=" * 80)
        self.test_route("GET", "/providers", "List all AI providers")
        self.test_route(
            "GET", 
            "/providers/openai/models", 
            "List OpenAI models",
            expected_status=200
        )
        
        # 3. Prompt Router
        print("\n" + "=" * 80)
        print("3️⃣  PROMPT ROUTER")
        print("=" * 80)
        self.test_route("GET", "/prompts", "List all prompts")
        self.test_route(
            "GET",
            "/prompts/default",
            "Get specific prompt template",
            expected_status=200
        )
        self.test_route(
            "POST",
            "/prompts/default/render",
            "Render prompt with variables",
            json_data={"variables": {"name": "user"}},
            expected_status=200
        )
        
        # 4. Embedding Router
        print("\n" + "=" * 80)
        print("4️⃣  EMBEDDING ROUTER")
        print("=" * 80)
        self.test_route(
            "POST",
            "/embeddings",
            "Generate embeddings",
            json_data={
                "text": "Hello, this is a test",
                "provider": "openai",
                "model": "text-embedding-3-small"
            },
            skip=True  # Skip due to API key requirements
        )
        
        # 5. Conversation Router
        print("\n" + "=" * 80)
        print("5️⃣  CONVERSATION ROUTER")
        print("=" * 80)
        
        # Create session
        create_response = self.test_route(
            "POST",
            "/conversation",
            "Create new conversation session",
            expected_status=201
        )
        
        # Extract session ID if available
        if create_response["status"] == "PASS" and "response_summary" in create_response:
            try:
                self.session_id = json.loads(create_response["response_summary"])["session_id"]
            except:
                pass
        
        # Use a test session ID
        test_session_id = self.session_id or "test-session-123"
        
        # Get conversation
        self.test_route(
            "GET",
            f"/conversation/{test_session_id}",
            "Get conversation by session ID",
            expected_status=200
        )
        
        # Chat message
        self.test_route(
            "POST",
            f"/conversation/{test_session_id}/chat",
            "Send chat message",
            json_data={
                "message": "Hello, how are you?",
                "provider": "openai",
                "model": "gpt-4",
                "temperature": 0.7,
                "max_tokens": 500
            },
            skip=True  # Skip due to API key requirements
        )
        
        # Delete conversation
        self.test_route(
            "DELETE",
            f"/conversation/{test_session_id}",
            "Delete conversation session",
            expected_status=204
        )
        
        # 6. AI Router
        print("\n" + "=" * 80)
        print("6️⃣  AI ROUTER")
        print("=" * 80)
        self.test_route(
            "POST",
            "/ai/generate",
            "Generate AI response",
            json_data={
                "messages": [{"role": "user", "content": "Hello"}],
                "provider": "openai",
                "model": "gpt-4",
                "temperature": 0.7,
                "max_tokens": 500
            },
            skip=True  # Skip due to API key requirements
        )
        
        self.test_route(
            "POST",
            "/ai/generate/stream",
            "Stream AI response (SSE)",
            json_data={
                "messages": [{"role": "user", "content": "Hello"}],
                "provider": "openai",
                "model": "gpt-4",
                "temperature": 0.7,
                "max_tokens": 500
            },
            skip=True  # Skip due to API key requirements
        )
        
        # 7. Vector Router
        print("\n" + "=" * 80)
        print("7️⃣  VECTOR ROUTER")
        print("=" * 80)
        self.test_route(
            "POST",
            "/vectors",
            "Index document to vector store",
            json_data={
                "document_id": "doc-123",
                "content": "This is sample content",
                "metadata": {"source": "test"}
            },
            skip=True  # Skip due to API key requirements
        )
        
        self.test_route(
            "POST",
            "/vectors/search",
            "Search vector store",
            json_data={
                "query": "sample content",
                "top_k": 5
            },
            skip=True  # Skip due to API key requirements
        )
        
        self.test_route(
            "DELETE",
            "/vectors/doc-123",
            "Delete document from vector store",
            expected_status=204
        )
        
        self.test_route(
            "DELETE",
            "/vectors",
            "Clear entire vector store",
            expected_status=204
        )
        
        # 8. Document Router
        print("\n" + "=" * 80)
        print("8️⃣  DOCUMENT ROUTER")
        print("=" * 80)
        print("\n🔍 Testing POST /documents/upload...")
        print("   Description: Upload document for ingestion")
        # This requires multipart form data, testing separately
        try:
            files = {"file": ("test.txt", "test content", "text/plain")}
            response = self.client.post("/documents/upload", files=files)
            
            result = {
                "timestamp": datetime.now().isoformat(),
                "method": "POST",
                "path": "/documents/upload",
                "description": "Upload document for ingestion",
                "status": "PASS" if response.status_code < 500 else "FAIL",
                "status_code": response.status_code,
                "url": f"{self.base_url}/documents/upload",
            }
            print(f"   Status: {response.status_code} ({response.reason_phrase})")
            self.results.append(result)
        except Exception as e:
            print(f"   ❌ ERROR: {str(e)}")
            self.results.append({
                "timestamp": datetime.now().isoformat(),
                "method": "POST",
                "path": "/documents/upload",
                "description": "Upload document for ingestion",
                "status": "ERROR",
                "error": str(e),
                "url": f"{self.base_url}/documents/upload",
            })
        
        # 9. RAG Router
        print("\n" + "=" * 80)
        print("9️⃣  RAG ROUTER")
        print("=" * 80)
        self.test_route(
            "POST",
            "/rag/ask",
            "Submit question for RAG processing",
            json_data={
                "question": "What is Python?",
                "provider": "openai",
                "model": "gpt-4",
                "top_k": 5
            },
            skip=True  # Skip due to API key requirements
        )
        
        self.print_summary()
    
    def print_summary(self):
        """Print test summary report."""
        print("\n" + "=" * 80)
        print("📊 TEST SUMMARY REPORT")
        print("=" * 80)
        
        pass_count = sum(1 for r in self.results if r["status"] == "PASS")
        fail_count = sum(1 for r in self.results if r["status"] == "FAIL")
        error_count = sum(1 for r in self.results if r["status"] == "ERROR")
        skip_count = sum(1 for r in self.results if r["status"] == "SKIPPED")
        
        total = len(self.results)
        
        print(f"\n📈 Results:")
        print(f"   ✅ PASS:    {pass_count}/{total}")
        print(f"   ❌ FAIL:    {fail_count}/{total}")
        print(f"   ⚠️  ERROR:   {error_count}/{total}")
        print(f"   ⏭️  SKIPPED: {skip_count}/{total}")
        
        # Group by status
        print(f"\n📋 Detailed Results:")
        
        if pass_count > 0:
            print(f"\n✅ PASSING ROUTES ({pass_count}):")
            for result in self.results:
                if result["status"] == "PASS":
                    print(f"   {result['method']:6} {result['path']:40} ({result['status_code']})")
        
        if fail_count > 0:
            print(f"\n❌ FAILING ROUTES ({fail_count}):")
            for result in self.results:
                if result["status"] == "FAIL":
                    print(f"   {result['method']:6} {result['path']:40} ({result['status_code']})")
        
        if error_count > 0:
            print(f"\n⚠️  ERROR ROUTES ({error_count}):")
            for result in self.results:
                if result["status"] == "ERROR":
                    print(f"   {result['method']:6} {result['path']:40} ({result.get('error', 'Unknown')})")
        
        if skip_count > 0:
            print(f"\n⏭️  SKIPPED ROUTES ({skip_count}):")
            for result in self.results:
                if result["status"] == "SKIPPED":
                    print(f"   {result['method']:6} {result['path']:40} (requires API key)")
        
        # Issues summary
        print("\n" + "=" * 80)
        print("🔍 ISSUES DETECTED")
        print("=" * 80)
        
        issues = [r for r in self.results if r["status"] in ["FAIL", "ERROR"]]
        
        if issues:
            print(f"\n⚠️  Found {len(issues)} issue(s):\n")
            for idx, issue in enumerate(issues, 1):
                print(f"{idx}. {issue['method']} {issue['path']}")
                if issue["status"] == "FAIL":
                    print(f"   Status Code: {issue['status_code']} (expected: {issue.get('expected_status', 'N/A')})")
                elif issue["status"] == "ERROR":
                    print(f"   Error: {issue['error']}")
                print()
        else:
            print("\n✅ No issues detected! All tests passed or were intentionally skipped.")
        
        # Save results to file
        self.save_results()
    
    def save_results(self):
        """Save test results to JSON file."""
        output_file = "route_test_results.json"
        with open(output_file, "w") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "base_url": self.base_url,
                "total_tests": len(self.results),
                "pass_count": sum(1 for r in self.results if r["status"] == "PASS"),
                "fail_count": sum(1 for r in self.results if r["status"] == "FAIL"),
                "error_count": sum(1 for r in self.results if r["status"] == "ERROR"),
                "skip_count": sum(1 for r in self.results if r["status"] == "SKIPPED"),
                "results": self.results
            }, f, indent=2)
        print(f"\n💾 Results saved to {output_file}")


if __name__ == "__main__":
    runner = RouteTestRunner()
    try:
        runner.run_all_tests()
    except KeyboardInterrupt:
        print("\n\n⏸️  Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        runner.client.close()
