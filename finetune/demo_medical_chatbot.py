"""
Demo Script for Fine-tuned Medical Chatbot
Shows how the medical chatbot would work in practice.
"""

import json
import random
from typing import Dict, List
from medical_response_templates import MedicalResponseTemplates, COMMON_RESPONSES

class MedicalChatbotDemo:
    """Demo class for the medical chatbot."""
    
    def __init__(self):
        self.templates = MedicalResponseTemplates()
        self.conversation_history = []
        
        # Demo scenarios
        self.demo_scenarios = {
            "fever": {
                "user_inputs": [
                    "I have fever",
                    "मुझे बुखार है",
                    "I'm running a temperature",
                    "I feel hot and have a headache"
                ],
                "description": "Fever symptoms with structured medical guidance"
            },
            "emergency": {
                "user_inputs": [
                    "emergency",
                    "help urgent",
                    "I need immediate medical help",
                    "तत्काल सहायता"
                ],
                "description": "Emergency situation with immediate response"
            },
            "chest_pain": {
                "user_inputs": [
                    "I have chest pain",
                    "My chest hurts",
                    "मेरे सीने में दर्द है",
                    "Chest pain and shortness of breath"
                ],
                "description": "Chest pain with emergency protocols"
            },
            "voice_message": {
                "user_inputs": [
                    "[Voice message: Mujhe pet mein dard hai]",
                    "[Voice message: I have stomach pain]",
                    "[Voice message: मुझे बुखार है]"
                ],
                "description": "Voice message processing with confirmation"
            },
            "medical_advice": {
                "user_inputs": [
                    "I have diabetes, what should I do?",
                    "I have high blood pressure, what should I do?",
                    "What should I do for my hypertension?"
                ],
                "description": "General medical advice and recommendations"
            }
        }

    def simulate_model_response(self, user_input: str, scenario_type: str = None) -> str:
        """Simulate the fine-tuned model's response."""
        
        # Determine scenario type if not provided
        if not scenario_type:
            scenario_type = self._classify_input(user_input)
        
        # Generate appropriate response based on scenario
        if scenario_type == "fever":
            return self.templates.yellow_alert_response(
                conditions=COMMON_RESPONSES["fever"]["conditions"],
                actions=COMMON_RESPONSES["fever"]["actions"],
                see_doctor_conditions=COMMON_RESPONSES["fever"]["see_doctor"],
                nearby_options=COMMON_RESPONSES["fever"]["nearby"]
            )
        
        elif scenario_type == "emergency":
            return """🚨
EMERGENCY MODE ACTIVATED
Are you experiencing:
• Chest pain/Heart attack
• Breathing difficulty
• Severe bleeding
• Unconsciousness
• Other emergency"""
        
        elif scenario_type == "chest_pain":
            return self.templates.emergency_response(
                emergency_type=COMMON_RESPONSES["chest_pain"]["emergency_type"],
                phone_numbers=COMMON_RESPONSES["chest_pain"]["phone_numbers"],
                nearest_hospitals=COMMON_RESPONSES["chest_pain"]["hospitals"],
                waiting_instructions=COMMON_RESPONSES["chest_pain"]["waiting_instructions"]
            )
        
        elif scenario_type == "voice_message":
            # Extract the voice content
            if "pet mein dard" in user_input or "stomach pain" in user_input.lower():
                understood_text = "Stomach pain"
            elif "बुखार" in user_input or "fever" in user_input.lower():
                understood_text = "Fever"
            else:
                understood_text = "Medical symptom"
            
            return self.templates.voice_processing_response(understood_text)
        
        elif scenario_type == "medical_advice":
            if "diabetes" in user_input.lower():
                return self.templates.general_medical_advice(
                    advice_type="DIABETES MANAGEMENT",
                    recommendations=[
                        "Monitor blood sugar regularly",
                        "Follow prescribed diet",
                        "Exercise regularly",
                        "Take medications as prescribed"
                    ],
                    warnings=[
                        "Avoid high sugar foods",
                        "Check feet daily for wounds",
                        "Keep emergency contacts handy"
                    ],
                    follow_up="Schedule regular check-ups with your doctor"
                )
            elif "blood pressure" in user_input.lower() or "hypertension" in user_input.lower():
                return self.templates.general_medical_advice(
                    advice_type="HYPERTENSION MANAGEMENT",
                    recommendations=[
                        "Reduce salt intake",
                        "Exercise regularly",
                        "Manage stress",
                        "Monitor blood pressure"
                    ],
                    warnings=[
                        "Avoid excessive salt",
                        "Limit alcohol consumption",
                        "Don't skip medications"
                    ],
                    follow_up="Visit your doctor for blood pressure monitoring"
                )
        
        # Default response for unrecognized inputs
        return """🏥
I understand you have a medical concern. Let me help you better.
Could you please describe your symptoms in more detail?
• What symptoms are you experiencing?
• When did they start?
• How severe are they?
• Any other relevant information?"""

    def _classify_input(self, user_input: str) -> str:
        """Classify user input to determine response type."""
        user_input_lower = user_input.lower()
        
        if any(word in user_input_lower for word in ["fever", "temperature", "hot", "बुखार"]):
            return "fever"
        elif any(word in user_input_lower for word in ["emergency", "urgent", "help", "तत्काल"]):
            return "emergency"
        elif any(word in user_input_lower for word in ["chest", "heart", "सीने"]):
            return "chest_pain"
        elif "voice message" in user_input_lower or "[" in user_input:
            return "voice_message"
        elif any(word in user_input_lower for word in ["diabetes", "blood pressure", "hypertension"]):
            return "medical_advice"
        else:
            return "general"

    def run_interactive_demo(self):
        """Run an interactive demo of the medical chatbot."""
        print("🏥 DeepSeek-V3 Medical Chatbot Demo")
        print("=" * 50)
        print("This demo shows how the fine-tuned model would respond to medical queries.")
        print("Type 'quit' to exit, 'help' for available scenarios.")
        print()
        
        while True:
            try:
                user_input = input("👤 User: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Thank you for trying the medical chatbot demo!")
                    break
                
                if user_input.lower() == 'help':
                    self._show_help()
                    continue
                
                if not user_input:
                    continue
                
                # Generate response
                response = self.simulate_model_response(user_input)
                
                print(f"🤖 Assistant: {response}")
                print()
                
                # Store conversation
                self.conversation_history.append({
                    "user": user_input,
                    "assistant": response
                })
                
            except KeyboardInterrupt:
                print("\n👋 Demo interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

    def run_scenario_demo(self, scenario_name: str = None):
        """Run a demo of specific scenarios."""
        print("🏥 DeepSeek-V3 Medical Chatbot - Scenario Demo")
        print("=" * 60)
        
        if scenario_name and scenario_name in self.demo_scenarios:
            scenarios = {scenario_name: self.demo_scenarios[scenario_name]}
        else:
            scenarios = self.demo_scenarios
        
        for scenario_type, scenario_data in scenarios.items():
            print(f"\n📋 Scenario: {scenario_type.upper()}")
            print(f"📝 Description: {scenario_data['description']}")
            print("-" * 40)
            
            for i, user_input in enumerate(scenario_data['user_inputs'], 1):
                print(f"\n{i}. User: {user_input}")
                response = self.simulate_model_response(user_input, scenario_type)
                print(f"   Assistant: {response}")
                print()
        
        print("✅ Scenario demo completed!")

    def _show_help(self):
        """Show available demo options."""
        print("\n📚 Available Demo Options:")
        print("-" * 30)
        print("• Type any medical symptom or question")
        print("• Try these examples:")
        for scenario_type, scenario_data in self.demo_scenarios.items():
            print(f"  - {scenario_type}: {scenario_data['user_inputs'][0]}")
        print("• Commands:")
        print("  - 'help': Show this help")
        print("  - 'quit': Exit demo")
        print("  - 'scenarios': Run scenario demo")
        print()

    def save_conversation(self, filename: str = "demo_conversation.json"):
        """Save the conversation history to a file."""
        if self.conversation_history:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, indent=2, ensure_ascii=False)
            print(f"💾 Conversation saved to {filename}")

def main():
    """Main function to run the demo."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Medical Chatbot Demo")
    parser.add_argument("--mode", choices=["interactive", "scenarios"], 
                       default="interactive", help="Demo mode")
    parser.add_argument("--scenario", choices=list(MedicalChatbotDemo().demo_scenarios.keys()),
                       help="Specific scenario to demo")
    parser.add_argument("--save", action="store_true", 
                       help="Save conversation to file")
    
    args = parser.parse_args()
    
    demo = MedicalChatbotDemo()
    
    try:
        if args.mode == "interactive":
            demo.run_interactive_demo()
        else:
            demo.run_scenario_demo(args.scenario)
        
        if args.save:
            demo.save_conversation()
            
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted. Goodbye!")

if __name__ == "__main__":
    main() 