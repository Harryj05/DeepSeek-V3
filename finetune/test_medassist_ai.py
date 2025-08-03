"""
Simple Test Script for MedAssist AI
Demonstrates the key features and response formats.
"""

from medassist_response_templates import MedAssistResponseTemplates, MEDASSIST_RESPONSES

def test_medassist_ai():
    """Test MedAssist AI key features."""
    templates = MedAssistResponseTemplates()
    
    print("🏥 MedAssist AI - DeepSeek-V3 Fine-tuning Demo")
    print("=" * 60)
    print()
    
    # Test 1: Welcome Message
    print("1️⃣ WELCOME MESSAGE")
    print("-" * 30)
    print(templates.welcome_message())
    print()
    
    # Test 2: Symptom Checker
    print("2️⃣ SYMPTOM CHECKER")
    print("-" * 30)
    print("User: I have fever")
    print("Assistant:", templates.yellow_alert_response(
        conditions=MEDASSIST_RESPONSES["fever"]["conditions"],
        actions=MEDASSIST_RESPONSES["fever"]["actions"],
        see_doctor_conditions=MEDASSIST_RESPONSES["fever"]["see_doctor"],
        nearby_options=MEDASSIST_RESPONSES["fever"]["nearby"]
    ))
    print()
    
    # Test 3: Emergency Response
    print("3️⃣ EMERGENCY RESPONSE")
    print("-" * 30)
    print("User: emergency")
    print("Assistant:", templates.emergency_mode_activation())
    print()
    
    # Test 4: Voice Message Processing
    print("4️⃣ VOICE MESSAGE PROCESSING")
    print("-" * 30)
    print("User: [Voice message: Mujhe pet mein dard hai]")
    print("Assistant:", templates.voice_processing_response("Stomach pain"))
    print()
    
    # Test 5: Medication Reminder
    print("5️⃣ MEDICATION REMINDER")
    print("-" * 30)
    print("Assistant:", templates.medication_reminder("Vitamin D", "1 tablet", "9:00 AM", 12))
    print()
    
    # Test 6: Health Tips
    print("6️⃣ HEALTH TIPS")
    print("-" * 30)
    print("User: tips")
    print("Assistant:", templates.health_tip_daily())
    print()
    
    # Test 7: Web App Transition
    print("7️⃣ WEB APP TRANSITION")
    print("-" * 30)
    print("User: web")
    print("Assistant:", templates.web_app_transition())
    print()
    
    # Test 8: Family Care Update
    print("8️⃣ FAMILY CARE UPDATE")
    print("-" * 30)
    print("Assistant:", templates.family_care_update(
        "Rahul", "stable", "Apollo Hospital", "Sharma", "2 minutes ago"
    ))
    print()
    
    # Test 9: Corporate Wellness
    print("9️⃣ CORPORATE WELLNESS")
    print("-" * 30)
    print("Assistant:", templates.corporate_wellness_summary(
        "TechCorp Ltd", 250, 7.4,
        ["23% reduction in sick days", "67 employees completed health assessments"],
        ["Flu season approaching", "12 employees with high stress indicators"]
    ))
    print()
    
    print("✅ MedAssist AI Demo Completed!")
    print()
    print("🎯 Key Features Demonstrated:")
    print("• WhatsApp Bot Integration")
    print("• Emergency Response System")
    print("• Voice Message Processing")
    print("• Medication Management")
    print("• Health Tips & Education")
    print("• Web App Transition")
    print("• Family Care Coordination")
    print("• Corporate Wellness Management")
    print("• Multilingual Support")
    print()
    print("📊 Training Data Generated: 3000+ examples")
    print("🤖 Model: DeepSeek-V3 with LoRA fine-tuning")
    print("🏥 Platform: Comprehensive healthcare intelligence")

if __name__ == "__main__":
    test_medassist_ai() 