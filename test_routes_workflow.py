#!/usr/bin/env python3
"""Comprehensive API route testing with workflow validation."""

import httpx
import json
from typing import Optional, Dict, Any
from datetime import datetime

BASE_URL = "http://localhost:8000"

class RouteTestWithWorkflow:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.results = []
        self.client = httpx.Client(base_url=base_url, timeout=30.0)
        self.created_session_id = None
        
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
            
            success = response.status_code == expected_status
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
                    result["response_data"] = response_data
                    result["response_summary"] = str(response_data)[:200]
                except:
                    result["response_summary"] = response.text[:200]
            
            print(f"   {status_str} Status: {response.status_code} ({response.reason_phrase})")
            if "response_data" in result:
                print(f"   Response: {result['response_data']}")
            
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
    
    def run_workflow_test(self):
        """Test the complete workflow."""
        print("=" * 80)
        print("🚀 ENTERPRISE AI PLATFORM - COMPREHENSIVE ROUTE TEST WITH WORKFLOW")
        print("=" * 80)
        print(f"Base URL: {self.base_url}")
        print(f"Start Time: {datetime.now().isoformat()}")
        print("=" * 80)
        
        # 1. Health Check
        print("\n" + "=" * 80)
        print("1️⃣  HEALTH ROUTER")
        print("=" * 80)
        self.test_route("GET", "/health", "Health check endpoint", expected_status=200)
        
        # 2. Provider Router
        print("\n" + "=" * 80)
        print("2️⃣  PROVIDER ROUTER")
        print("=" * 80)
        self.test_route("GET", "/providers", "List all AI providers", expected_status=200)
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
        self.test_route("GET", "/prompts", "List all prompts", expected_status=200)
        
        # 4. Conversation Router - WORKFLOW TEST
        print("\n" + "=" * 80)
        print("4️⃣  CONVERSATION ROUTER - WORKFLOW")
        print("=" * 80)
        
        # Create session
        create_result = self.test_route(
            "POST",
            "/conversation",
            "Create new conversation session",
            expected_status=201
        )
        
        if create_result["status"] == "PASS" and "response_data" in create_result:
            self.created_session_id = create_result["response_data"].get("session_id")
            print(f"\n✅ Created session with ID: {self.created_session_id}")
            
            # Get the conversation
            if self.created_session_id:
                self.test_route(
                    "GET",
                    f"/conversation/{self.created_session_id}",
                    "Get conversation by session ID",
                    expected_status=200
                )
        
        # 5. Vector Router
        print("\n" + "=" * 80)
        print("5️⃣  VECTOR ROUTER")
        print("=" * 80)
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
        
        # 6. Document Router
        print("\n" + "=" * 80)
        print("6️⃣  DOCUMENT ROUTER")
        print("=" * 80)
        print("\n🔍 Testing POST /documents/upload...")
        print("   Description: Upload document for ingestion")
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
        
        # 7. API-Dependent Tests (Skipped)
        print("\n" + "=" * 80)
        print("7️⃣  API-DEPENDENT ROUTES (SKIPPED - Require API Keys)")
        print("=" * 80)
        
        skipped_routes = [
            ("POST", "/embeddings", "Generate embeddings"),
            ("POST", "/ai/generate", "Generate AI response"),
            ("POST", "/ai/generate/stream", "Stream AI response (SSE)"),
            ("POST", "/vectors", "Index document to vector store"),
            ("POST", "/vectors/search", "Search vector store"),
            ("POST", "/rag/ask", "Submit question for RAG processing"),
        ]
        
        if self.created_session_id:
            skipped_routes.insert(0, ("POST", f"/conversation/{self.created_session_id}/chat", "Send chat message"))
        
        for method, path, description in skipped_routes:
            self.test_route(
                method,
                path,
                description,
                skip=True
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
        pass_rate = (pass_count / total * 100) if total > 0 else 0
        
        print(f"\n📈 Results:")
        print(f"   ✅ PASS:    {pass_count}/{total} ({pass_rate:.1f}%)")
        print(f"   ❌ FAIL:    {fail_count}/{total}")
        print(f"   ⚠️  ERROR:   {error_count}/{total}")
        print(f"   ⏭️  SKIPPED: {skip_count}/{total}")
        
        # Group by status
        print(f"\n📋 Detailed Results by Status:")
        
        if pass_count > 0:
            print(f"\n✅ PASSING ROUTES ({pass_count}):")
            for result in self.results:
                if result["status"] == "PASS":
                    print(f"   {result['method']:6} {result['path']:40} ({result['status_code']})")
        
        if fail_count > 0:
            print(f"\n❌ FAILING ROUTES ({fail_count}):")
            for result in self.results:
                if result["status"] == "FAIL":
                    print(f"   {result['method']:6} {result['path']:40} ({result['status_code']}) - expected {result.get('expected_status', 'N/A')}")
        
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
            print(f"\n✅ Pass Rate: {pass_rate:.1f}% ({pass_count} / {total - skip_count} testable routes)")
        
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
                "created_session_id": self.created_session_id,
                "results": self.results
            }, f, indent=2)
        print(f"\n💾 Results saved to {output_file}")


if __name__ == "__main__":
    runner = RouteTestWithWorkflow()
    try:
        runner.run_workflow_test()
    except KeyboardInterrupt:
        print("\n\n⏸️  Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        runner.client.close()
