"""
MedAssist AI Demo Script
Comprehensive demo showing all user flows and features of the MedAssist AI platform.
"""

import json
import random
from typing import Dict, List
from medassist_response_templates import MedAssistResponseTemplates, MEDASSIST_RESPONSES

class MedAssistDemo:
    """Comprehensive demo for MedAssist AI platform."""
    
    def __init__(self):
        self.templates = MedAssistResponseTemplates()
        self.conversation_history = []
        
        # Demo scenarios covering all user flows
        self.demo_scenarios = {
            "welcome_onboarding": {
                "name": "Welcome & Onboarding",
                "description": "Complete user onboarding flow with language selection and profile setup",
                "flows": [
                    "Initial greeting and language selection",
                    "Name, age, and location collection",
                    "Feature introduction and next steps"
                ]
            },
            "symptom_checker": {
                "name": "Symptom Checker",
                "description": "Comprehensive symptom analysis with structured medical guidance",
                "flows": [
                    "Text-based symptom input",
                    "Voice message processing",
                    "Photo upload capability",
                    "Structured medical recommendations"
                ]
            },
            "emergency_response": {
                "name": "Emergency Response System",
                "description": "Critical medical situation handling with immediate protocols",
                "flows": [
                    "Emergency mode activation",
                    "Symptom categorization",
                    "Immediate action protocols",
                    "Hospital and ambulance coordination"
                ]
            },
            "medication_management": {
                "name": "Medication Management",
                "description": "Smart medication reminders and adherence tracking",
                "flows": [
                    "Medication reminder notifications",
                    "Confirmation tracking",
                    "Streak maintenance",
                    "Dosage optimization"
                ]
            },
            "health_tips": {
                "name": "Health Tips & Education",
                "description": "Personalized health tips and wellness guidance",
                "flows": [
                    "Daily health tips",
                    "Seasonal health alerts",
                    "Personalized recommendations",
                    "Wellness challenges"
                ]
            },
            "web_app_integration": {
                "name": "Web App Integration",
                "description": "Seamless transition between WhatsApp and web platform",
                "flows": [
                    "WhatsApp to web transition",
                    "Feature comparison",
                    "Data synchronization",
                    "Cross-platform continuity"
                ]
            },
            "family_care": {
                "name": "Family Care Coordination",
                "description": "Family health management and care coordination",
                "flows": [
                    "Family member monitoring",
                    "Care status updates",
                    "Emergency notifications",
                    "Care team coordination"
                ]
            },
            "corporate_wellness": {
                "name": "Corporate Wellness",
                "description": "Employee health management and wellness programs",
                "flows": [
                    "Company health overview",
                    "Employee engagement analytics",
                    "Wellness program management",
                    "ROI tracking"
                ]
            }
        }

    def simulate_model_response(self, user_input: str, scenario_type: str = None) -> str:
        """Simulate the fine-tuned model's response."""
        
        # Determine scenario type if not provided
        if not scenario_type:
            scenario_type = self._classify_input(user_input)
        
        # Generate appropriate response based on scenario
        if scenario_type == "welcome":
            return self.templates.welcome_message()
        
        elif scenario_type == "symptom_checker":
            if "fever" in user_input.lower() or "बुखार" in user_input:
                return self.templates.yellow_alert_response(
                    conditions=MEDASSIST_RESPONSES["fever"]["conditions"],
                    actions=MEDASSIST_RESPONSES["fever"]["actions"],
                    see_doctor_conditions=MEDASSIST_RESPONSES["fever"]["see_doctor"],
                    nearby_options=MEDASSIST_RESPONSES["fever"]["nearby"]
                )
            elif "chest" in user_input.lower() or "सीने" in user_input:
                return self.templates.emergency_response(
                    emergency_type=MEDASSIST_RESPONSES["chest_pain"]["emergency_type"],
                    phone_numbers=MEDASSIST_RESPONSES["chest_pain"]["phone_numbers"],
                    nearest_hospitals=MEDASSIST_RESPONSES["chest_pain"]["hospitals"],
                    waiting_instructions=MEDASSIST_RESPONSES["chest_pain"]["waiting_instructions"]
                )
            else:
                return self.templates.symptom_checker_intro()
        
        elif scenario_type == "emergency":
            return self.templates.emergency_mode_activation()
        
        elif scenario_type == "voice_message":
            if "pet mein dard" in user_input or "stomach" in user_input.lower():
                understood_text = "Stomach pain"
            elif "बुखार" in user_input or "fever" in user_input.lower():
                understood_text = "Fever"
            else:
                understood_text = "Medical symptom"
            
            return self.templates.voice_processing_response(understood_text)
        
        elif scenario_type == "medication_reminder":
            medication = random.choice(["Vitamin D", "Blood pressure medicine", "Diabetes medicine"])
            dosage = random.choice(["1 tablet", "2 tablets", "1 capsule"])
            time = random.choice(["9:00 AM", "2:00 PM", "8:00 PM"])
            streak = random.randint(1, 30)
            
            return self.templates.medication_reminder(medication, dosage, time, streak)
        
        elif scenario_type == "health_tips":
            return self.templates.health_tip_daily()
        
        elif scenario_type == "web_app":
            return self.templates.web_app_transition()
        
        elif scenario_type == "family_care":
            return self.templates.family_care_update(
                "Rahul", "stable", "Apollo Hospital", "Sharma", "2 minutes ago"
            )
        
        elif scenario_type == "corporate_wellness":
            return self.templates.corporate_wellness_summary(
                "TechCorp Ltd", 250, 7.4,
                ["23% reduction in sick days", "67 employees completed health assessments"],
                ["Flu season approaching", "12 employees with high stress indicators"]
            )
        
        # Default response
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
        
        if any(word in user_input_lower for word in ["hi", "hello", "start", "begin", "नमस्ते"]):
            return "welcome"
        elif any(word in user_input_lower for word in ["fever", "temperature", "hot", "बुखार"]):
            return "symptom_checker"
        elif any(word in user_input_lower for word in ["emergency", "urgent", "help", "तत्काल"]):
            return "emergency"
        elif any(word in user_input_lower for word in ["chest", "heart", "सीने"]):
            return "symptom_checker"
        elif "voice message" in user_input_lower or "[" in user_input:
            return "voice_message"
        elif any(word in user_input_lower for word in ["medication", "medicine", "pill", "tablet"]):
            return "medication_reminder"
        elif any(word in user_input_lower for word in ["tips", "health tips", "wellness"]):
            return "health_tips"
        elif any(word in user_input_lower for word in ["web", "app", "detailed", "comprehensive"]):
            return "web_app"
        elif any(word in user_input_lower for word in ["family", "care", "update"]):
            return "family_care"
        elif any(word in user_input_lower for word in ["corporate", "company", "employee"]):
            return "corporate_wellness"
        else:
            return "general"

    def run_comprehensive_demo(self):
        """Run a comprehensive demo of all MedAssist AI features."""
        print("🏥 MedAssist AI - Comprehensive Healthcare Intelligence Platform")
        print("=" * 80)
        print("This demo showcases the complete MedAssist AI platform capabilities.")
        print()
        
        for scenario_key, scenario_data in self.demo_scenarios.items():
            print(f"📋 {scenario_data['name']}")
            print(f"📝 {scenario_data['description']}")
            print("-" * 60)
            
            # Run scenario-specific demos
            if scenario_key == "welcome_onboarding":
                self._demo_welcome_flow()
            elif scenario_key == "symptom_checker":
                self._demo_symptom_checker()
            elif scenario_key == "emergency_response":
                self._demo_emergency_response()
            elif scenario_key == "medication_management":
                self._demo_medication_management()
            elif scenario_key == "health_tips":
                self._demo_health_tips()
            elif scenario_key == "web_app_integration":
                self._demo_web_app_integration()
            elif scenario_key == "family_care":
                self._demo_family_care()
            elif scenario_key == "corporate_wellness":
                self._demo_corporate_wellness()
            
            print()
        
        print("✅ Comprehensive demo completed!")
        print("\n🎯 Key Features Demonstrated:")
        print("• WhatsApp Bot Integration")
        print("• Emergency Response System")
        print("• Voice Message Processing")
        print("• Medication Reminders")
        print("• Health Tips & Education")
        print("• Web App Transition")
        print("• Family Care Coordination")
        print("• Corporate Wellness Management")
        print("• Multilingual Support")

    def _demo_welcome_flow(self):
        """Demo welcome and onboarding flow."""
        print("👤 User: Hi")
        response = self.templates.welcome_message()
        print(f"🤖 Assistant: {response}")
        
        print("\n👤 User: 1")
        response = self.templates.onboarding_flow(1)
        print(f"🤖 Assistant: {response}")
        
        print("\n👤 User: Rahul")
        response = self.templates.onboarding_flow(2, {"name": "Rahul"})
        print(f"🤖 Assistant: {response}")
        
        print("\n👤 User: 28")
        response = self.templates.onboarding_flow(3)
        print(f"🤖 Assistant: {response}")
        
        print("\n👤 User: Pune")
        response = self.templates.onboarding_flow(4)
        print(f"🤖 Assistant: {response}")

    def _demo_symptom_checker(self):
        """Demo symptom checker functionality."""
        print("👤 User: symptoms")
        response = self.templates.symptom_checker_intro()
        print(f"🤖 Assistant: {response}")
        
        print("\n👤 User: I have fever and headache")
        response = self.templates.yellow_alert_response(
            conditions=MEDASSIST_RESPONSES["fever"]["conditions"],
            actions=MEDASSIST_RESPONSES["fever"]["actions"],
            see_doctor_conditions=MEDASSIST_RESPONSES["fever"]["see_doctor"],
            nearby_options=MEDASSIST_RESPONSES["fever"]["nearby"]
        )
        print(f"🤖 Assistant: {response}")

    def _demo_emergency_response(self):
        """Demo emergency response system."""
        print("👤 User: emergency")
        response = self.templates.emergency_mode_activation()
        print(f"🤖 Assistant: {response}")
        
        print("\n👤 User: 1")
        response = self.templates.emergency_response(
            emergency_type=MEDASSIST_RESPONSES["chest_pain"]["emergency_type"],
            phone_numbers=MEDASSIST_RESPONSES["chest_pain"]["phone_numbers"],
            nearest_hospitals=MEDASSIST_RESPONSES["chest_pain"]["hospitals"],
            waiting_instructions=MEDASSIST_RESPONSES["chest_pain"]["waiting_instructions"]
        )
        print(f"🤖 Assistant: {response}")

    def _demo_medication_management(self):
        """Demo medication management system."""
        print("🤖 Assistant: [Medication Reminder]")
        response = self.templates.medication_reminder("Vitamin D", "1 tablet", "9:00 AM", 12)
        print(f"🤖 Assistant: {response}")
        
        print("\n👤 User: ✅")
        response = self.templates.medication_confirmation("Vitamin D", 13)
        print(f"🤖 Assistant: {response}")

    def _demo_health_tips(self):
        """Demo health tips functionality."""
        print("👤 User: tips")
        response = self.templates.health_tip_daily()
        print(f"🤖 Assistant: {response}")

    def _demo_web_app_integration(self):
        """Demo web app integration."""
        print("👤 User: web")
        response = self.templates.web_app_transition()
        print(f"🤖 Assistant: {response}")

    def _demo_family_care(self):
        """Demo family care coordination."""
        print("🤖 Assistant: [Family Care Update]")
        response = self.templates.family_care_update(
            "Rahul", "stable", "Apollo Hospital", "Sharma", "2 minutes ago"
        )
        print(f"🤖 Assistant: {response}")

    def _demo_corporate_wellness(self):
        """Demo corporate wellness features."""
        print("🤖 Assistant: [Corporate Wellness Report]")
        response = self.templates.corporate_wellness_summary(
            "TechCorp Ltd", 250, 7.4,
            ["23% reduction in sick days", "67 employees completed health assessments"],
            ["Flu season approaching", "12 employees with high stress indicators"]
        )
        print(f"🤖 Assistant: {response}")

    def run_interactive_demo(self):
        """Run an interactive demo of MedAssist AI."""
        print("🏥 MedAssist AI - Interactive Demo")
        print("=" * 50)
        print("Experience the MedAssist AI platform interactively.")
        print("Type 'quit' to exit, 'help' for available scenarios.")
        print()
        
        while True:
            try:
                user_input = input("👤 User: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Thank you for experiencing MedAssist AI!")
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

    def _show_help(self):
        """Show available demo options."""
        print("\n📚 Available Demo Scenarios:")
        print("-" * 40)
        for scenario_key, scenario_data in self.demo_scenarios.items():
            print(f"• {scenario_data['name']}: {scenario_data['description']}")
        print("\n💡 Try these examples:")
        print("• 'Hi' - Start onboarding")
        print("• 'symptoms' - Check symptoms")
        print("• 'emergency' - Emergency help")
        print("• 'tips' - Health tips")
        print("• 'web' - Web app features")
        print("• 'medication' - Medication reminders")
        print("• 'family' - Family care updates")
        print("• 'corporate' - Corporate wellness")
        print("\nCommands:")
        print("• 'help' - Show this help")
        print("• 'quit' - Exit demo")
        print()

    def save_conversation(self, filename: str = "medassist_demo_conversation.json"):
        """Save the conversation history to a file."""
        if self.conversation_history:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, indent=2, ensure_ascii=False)
            print(f"💾 Conversation saved to {filename}")

def main():
    """Main function to run the MedAssist AI demo."""
    import argparse
    
    parser = argparse.ArgumentParser(description="MedAssist AI Demo")
    parser.add_argument("--mode", choices=["comprehensive", "interactive"], 
                       default="comprehensive", help="Demo mode")
    parser.add_argument("--save", action="store_true", 
                       help="Save conversation to file")
    
    args = parser.parse_args()
    
    demo = MedAssistDemo()
    
    try:
        if args.mode == "comprehensive":
            demo.run_comprehensive_demo()
        else:
            demo.run_interactive_demo()
        
        if args.save:
            demo.save_conversation()
            
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted. Goodbye!")

if __name__ == "__main__":
    main() 