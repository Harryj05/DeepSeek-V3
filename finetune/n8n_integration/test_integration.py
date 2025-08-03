"""
Test Script for MedAssist AI + n8n Integration
Verifies the complete WhatsApp bot setup
"""

import requests
import json
import time
from typing import Dict, List

class MedAssistIntegrationTester:
    """Test the MedAssist AI + n8n integration."""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.test_results = []
    
    def test_health_endpoint(self) -> bool:
        """Test the health check endpoint."""
        try:
            response = requests.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Health check passed: {data}")
                self.test_results.append({"test": "health_check", "status": "passed", "data": data})
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                self.test_results.append({"test": "health_check", "status": "failed", "error": response.text})
                return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            self.test_results.append({"test": "health_check", "status": "error", "error": str(e)})
            return False
    
    def test_chat_endpoint(self, message: str, user_id: str = "test_user") -> bool:
        """Test the chat endpoint."""
        try:
            payload = {
                "message": message,
                "user_id": user_id
            }
            
            response = requests.post(
                f"{self.base_url}/chat",
                headers={"Content-Type": "application/json"},
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Chat test passed for '{message}':")
                print(f"   Response: {data['response'][:100]}...")
                print(f"   Input Type: {data['input_type']}")
                self.test_results.append({
                    "test": "chat_endpoint",
                    "status": "passed",
                    "message": message,
                    "response": data
                })
                return True
            else:
                print(f"❌ Chat test failed: {response.status_code}")
                self.test_results.append({
                    "test": "chat_endpoint",
                    "status": "failed",
                    "message": message,
                    "error": response.text
                })
                return False
        except Exception as e:
            print(f"❌ Chat test error: {e}")
            self.test_results.append({
                "test": "chat_endpoint",
                "status": "error",
                "message": message,
                "error": str(e)
            })
            return False
    
    def test_webhook_endpoint(self) -> bool:
        """Test the webhook endpoint with simulated WhatsApp data."""
        try:
            # Simulate WhatsApp webhook payload
            webhook_payload = {
                "entry": [{
                    "id": "test_entry_id",
                    "changes": [{
                        "value": {
                            "messaging_product": "whatsapp",
                            "metadata": {
                                "display_phone_number": "1234567890",
                                "phone_number_id": "test_phone_id"
                            },
                            "messages": [{
                                "from": "test_user_123",
                                "id": "test_message_id",
                                "timestamp": str(int(time.time())),
                                "type": "text",
                                "text": {
                                    "body": "I have fever"
                                }
                            }]
                        }
                    }]
                }]
            }
            
            response = requests.post(
                f"{self.base_url}/webhook",
                headers={"Content-Type": "application/json"},
                json=webhook_payload
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Webhook test passed:")
                print(f"   User ID: {data.get('user_id')}")
                print(f"   Input Type: {data.get('input_type')}")
                self.test_results.append({
                    "test": "webhook_endpoint",
                    "status": "passed",
                    "data": data
                })
                return True
            else:
                print(f"❌ Webhook test failed: {response.status_code}")
                self.test_results.append({
                    "test": "webhook_endpoint",
                    "status": "failed",
                    "error": response.text
                })
                return False
        except Exception as e:
            print(f"❌ Webhook test error: {e}")
            self.test_results.append({
                "test": "webhook_endpoint",
                "status": "error",
                "error": str(e)
            })
            return False
    
    def test_session_management(self, user_id: str = "test_user") -> bool:
        """Test session management endpoints."""
        try:
            # Test get session
            response = requests.get(f"{self.base_url}/session/{user_id}")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Session get test passed: {data}")
                
                # Test clear session
                response = requests.delete(f"{self.base_url}/session/{user_id}")
                if response.status_code == 200:
                    print(f"✅ Session clear test passed")
                    self.test_results.append({
                        "test": "session_management",
                        "status": "passed",
                        "data": data
                    })
                    return True
                else:
                    print(f"❌ Session clear test failed: {response.status_code}")
                    return False
            else:
                print(f"❌ Session get test failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Session management test error: {e}")
            self.test_results.append({
                "test": "session_management",
                "status": "error",
                "error": str(e)
            })
            return False
    
    def test_medassist_scenarios(self) -> bool:
        """Test various MedAssist AI scenarios."""
        scenarios = [
            ("Hi", "welcome"),
            ("I have fever", "symptom_checker"),
            ("emergency", "emergency"),
            ("tips", "health_tips"),
            ("web", "web_app"),
            ("[Voice message: Mujhe pet mein dard hai]", "voice_message")
        ]
        
        all_passed = True
        for message, expected_type in scenarios:
            print(f"\n🧪 Testing scenario: {expected_type}")
            success = self.test_chat_endpoint(message)
            if not success:
                all_passed = False
        
        return all_passed
    
    def run_all_tests(self) -> Dict:
        """Run all integration tests."""
        print("🏥 MedAssist AI + n8n Integration Test Suite")
        print("=" * 50)
        
        tests = [
            ("Health Check", self.test_health_endpoint),
            ("Chat Endpoint", lambda: self.test_chat_endpoint("Hi")),
            ("Webhook Endpoint", self.test_webhook_endpoint),
            ("Session Management", self.test_session_management),
            ("MedAssist Scenarios", self.test_medassist_scenarios)
        ]
        
        results = {}
        for test_name, test_func in tests:
            print(f"\n📋 Running {test_name}...")
            try:
                success = test_func()
                results[test_name] = "PASSED" if success else "FAILED"
            except Exception as e:
                print(f"❌ {test_name} error: {e}")
                results[test_name] = "ERROR"
        
        # Print summary
        print("\n" + "=" * 50)
        print("📊 TEST SUMMARY")
        print("=" * 50)
        
        passed = 0
        total = len(results)
        
        for test_name, result in results.items():
            status_icon = "✅" if result == "PASSED" else "❌"
            print(f"{status_icon} {test_name}: {result}")
            if result == "PASSED":
                passed += 1
        
        print(f"\n🎯 Overall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! Your MedAssist AI + n8n integration is ready!")
        else:
            print("⚠️  Some tests failed. Please check the configuration.")
        
        return {
            "summary": results,
            "passed": passed,
            "total": total,
            "details": self.test_results
        }
    
    def save_test_results(self, filename: str = "integration_test_results.json"):
        """Save test results to file."""
        results = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "tests": self.test_results
        }
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"💾 Test results saved to {filename}")

def main():
    """Run the integration tests."""
    tester = MedAssistIntegrationTester()
    
    # Check if server is running
    print("🔍 Checking if MedAssist AI server is running...")
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running!")
        else:
            print("❌ Server is not responding correctly")
            print("Please start the server with: python medassist_whatsapp_bot.py")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
        print("Please start the server with: python medassist_whatsapp_bot.py")
        return
    
    # Run tests
    results = tester.run_all_tests()
    
    # Save results
    tester.save_test_results()
    
    # Print n8n integration instructions
    if results["passed"] == results["total"]:
        print("\n🚀 Next Steps for n8n Integration:")
        print("1. Import the workflow: medassist_whatsapp_workflow.json")
        print("2. Configure WhatsApp Business API credentials")
        print("3. Update webhook URLs in the workflow")
        print("4. Test with actual WhatsApp messages")
        print("5. Monitor the integration in n8n")

if __name__ == "__main__":
    main() 