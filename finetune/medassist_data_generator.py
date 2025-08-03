"""
MedAssist AI Data Generator for DeepSeek-V3 Fine-tuning
Generates comprehensive training data covering all user flows and scenarios.
"""

import json
import random
from typing import List, Dict, Tuple
from medassist_response_templates import MedAssistResponseTemplates, MEDASSIST_RESPONSES

class MedAssistDataGenerator:
    """Generates comprehensive training data for MedAssist AI fine-tuning."""
    
    def __init__(self):
        self.templates = MedAssistResponseTemplates()
        
        # User demographics and languages
        self.languages = ["English", "हिंदी", "தமிழ்", "বাংলা"]
        self.cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad", "Pune", "Ahmedabad", "Surat", "Jaipur", "Lucknow"]
        
        # Common symptoms and their variations
        self.symptoms = {
            "fever": [
                "I have fever", "I'm running a temperature", "I feel hot", 
                "My body temperature is high", "I have a high fever",
                "मुझे बुखार है", "I have fever and headache", "बुखार आ रहा है"
            ],
            "chest_pain": [
                "I have chest pain", "My chest hurts", "Pain in my chest",
                "Chest discomfort", "Heart pain", "Pain in heart area",
                "मेरे सीने में दर्द है", "Chest pain and shortness of breath", "सीने में दर्द"
            ],
            "headache": [
                "I have headache", "My head hurts", "Head pain",
                "Migraine", "Severe headache", "Head pounding",
                "सिर दर्द", "Headache and dizziness", "माथे में दर्द"
            ],
            "stomach_pain": [
                "I have stomach pain", "My stomach hurts", "Abdominal pain",
                "Belly ache", "Stomach ache", "Pain in abdomen",
                "मुझे पेट में दर्द है", "Stomach pain and nausea", "पेट दर्द"
            ],
            "emergency": [
                "emergency", "help urgent", "urgent medical help",
                "emergency situation", "need immediate help",
                "तत्काल सहायता", "emergency medical attention", "जरूरी मदद"
            ]
        }
        
        # Voice message scenarios
        self.voice_scenarios = [
            "Mujhe pet mein dard hai", "मुझे बुखार है", "I have fever",
            "Chest pain", "Headache", "Stomach ache", "सिर दर्द है"
        ]
        
        # Medication scenarios
        self.medications = [
            "Vitamin D", "Blood pressure medicine", "Diabetes medicine",
            "Pain reliever", "Antibiotic", "Multivitamin"
        ]

    def generate_welcome_conversation(self) -> List[Dict[str, str]]:
        """Generate welcome and onboarding conversation."""
        conversation = []
        
        # Initial greeting
        user_input = random.choice(["Hi", "Hello", "Start", "Begin", "नमस्ते"])
        conversation.append({"role": "user", "content": user_input})
        
        # Bot welcome
        welcome_response = self.templates.welcome_message()
        conversation.append({"role": "assistant", "content": welcome_response})
        
        # Language selection
        language_choice = random.choice(["1", "2", "3", "4"])
        conversation.append({"role": "user", "content": language_choice})
        
        # Onboarding step 1
        step1_response = self.templates.onboarding_flow(1)
        conversation.append({"role": "assistant", "content": step1_response})
        
        # User provides name
        user_name = random.choice(["Rahul", "Priya", "Amit", "Neha", "Raj", "Sita"])
        conversation.append({"role": "user", "content": user_name})
        
        # Onboarding step 2
        step2_response = self.templates.onboarding_flow(2, {"name": user_name})
        conversation.append({"role": "assistant", "content": step2_response})
        
        # User provides age
        age = random.choice(["25", "28", "32", "35", "42", "45"])
        conversation.append({"role": "user", "content": age})
        
        # Onboarding step 3
        step3_response = self.templates.onboarding_flow(3)
        conversation.append({"role": "assistant", "content": step3_response})
        
        # User provides city
        city = random.choice(self.cities)
        conversation.append({"role": "user", "content": city})
        
        # Onboarding completion
        step4_response = self.templates.onboarding_flow(4)
        conversation.append({"role": "assistant", "content": step4_response})
        
        return conversation

    def generate_symptom_checker_conversation(self) -> List[Dict[str, str]]:
        """Generate symptom checker conversation flow."""
        conversation = []
        
        # User requests symptom check
        user_input = random.choice(["symptoms", "check symptoms", "I'm not feeling well", "मुझे बीमार लग रहा है"])
        conversation.append({"role": "user", "content": user_input})
        
        # Bot symptom checker intro
        intro_response = self.templates.symptom_checker_intro()
        conversation.append({"role": "assistant", "content": intro_response})
        
        # User describes symptoms
        symptom_type = random.choice(list(self.symptoms.keys()))
        user_symptom = random.choice(self.symptoms[symptom_type])
        conversation.append({"role": "user", "content": user_symptom})
        
        # Bot provides appropriate response based on symptom type
        if symptom_type == "fever":
            response = self.templates.yellow_alert_response(
                conditions=MEDASSIST_RESPONSES["fever"]["conditions"],
                actions=MEDASSIST_RESPONSES["fever"]["actions"],
                see_doctor_conditions=MEDASSIST_RESPONSES["fever"]["see_doctor"],
                nearby_options=MEDASSIST_RESPONSES["fever"]["nearby"]
            )
        elif symptom_type == "chest_pain":
            response = self.templates.emergency_response(
                emergency_type=MEDASSIST_RESPONSES["chest_pain"]["emergency_type"],
                phone_numbers=MEDASSIST_RESPONSES["chest_pain"]["phone_numbers"],
                nearest_hospitals=MEDASSIST_RESPONSES["chest_pain"]["hospitals"],
                waiting_instructions=MEDASSIST_RESPONSES["chest_pain"]["waiting_instructions"]
            )
        elif symptom_type == "headache":
            response = self.templates.yellow_alert_response(
                conditions=MEDASSIST_RESPONSES["headache"]["conditions"],
                actions=MEDASSIST_RESPONSES["headache"]["actions"],
                see_doctor_conditions=MEDASSIST_RESPONSES["headache"]["see_doctor"],
                nearby_options=MEDASSIST_RESPONSES["headache"]["nearby"]
            )
        else:
            response = self.templates.symptom_analysis_response(
                symptom="Stomach pain",
                follow_up_questions=MEDASSIST_RESPONSES["stomach_pain"]["questions"]
            )
        
        conversation.append({"role": "assistant", "content": response})
        
        return conversation

    def generate_emergency_conversation(self) -> List[Dict[str, str]]:
        """Generate emergency conversation flow."""
        conversation = []
        
        # User says emergency
        user_input = random.choice(self.symptoms["emergency"])
        conversation.append({"role": "user", "content": user_input})
        
        # Bot activates emergency mode
        emergency_response = self.templates.emergency_mode_activation()
        conversation.append({"role": "assistant", "content": emergency_response})
        
        # User selects emergency type
        emergency_choice = random.choice(["1", "2", "3", "4", "5"])
        conversation.append({"role": "user", "content": emergency_choice})
        
        # Bot responds with appropriate emergency protocol
        if emergency_choice == "1":  # Chest pain
            response = self.templates.emergency_response(
                emergency_type=MEDASSIST_RESPONSES["chest_pain"]["emergency_type"],
                phone_numbers=MEDASSIST_RESPONSES["chest_pain"]["phone_numbers"],
                nearest_hospitals=MEDASSIST_RESPONSES["chest_pain"]["hospitals"],
                waiting_instructions=MEDASSIST_RESPONSES["chest_pain"]["waiting_instructions"]
            )
        else:
            response = """🚨
EMERGENCY - ACT NOW!
🏥
CALL IMMEDIATELY:
• 108 - Emergency Ambulance
• 102 - Medical Emergency

⏰
WHILE WAITING:
• Stay calm
• Don't move if injured
• Keep airway clear if needed

📍
Share location with family/friends
  I'm monitoring - reply if condition changes"""
        
        conversation.append({"role": "assistant", "content": response})
        
        return conversation

    def generate_voice_message_conversation(self) -> List[Dict[str, str]]:
        """Generate voice message processing conversation flow."""
        conversation = []
        
        # User sends voice message
        voice_text = random.choice(self.voice_scenarios)
        conversation.append({"role": "user", "content": f"[Voice message: {voice_text}]"})
        
        # Bot processes voice
        if "pet mein dard" in voice_text or "stomach" in voice_text.lower():
            understood_text = "Stomach pain"
        elif "बुखार" in voice_text or "fever" in voice_text.lower():
            understood_text = "Fever"
        elif "सिर दर्द" in voice_text or "headache" in voice_text.lower():
            understood_text = "Headache"
        else:
            understood_text = "Medical symptom"
        
        voice_response = self.templates.voice_processing_response(understood_text)
        conversation.append({"role": "assistant", "content": voice_response})
        
        # User confirms
        conversation.append({"role": "user", "content": "Yes"})
        
        # Bot continues with symptom analysis
        if "stomach" in understood_text.lower():
            symptom_response = self.templates.symptom_analysis_response(
                symptom="Stomach pain",
                follow_up_questions=MEDASSIST_RESPONSES["stomach_pain"]["questions"]
            )
        elif "fever" in understood_text.lower():
            symptom_response = self.templates.yellow_alert_response(
                conditions=MEDASSIST_RESPONSES["fever"]["conditions"],
                actions=MEDASSIST_RESPONSES["fever"]["actions"],
                see_doctor_conditions=MEDASSIST_RESPONSES["fever"]["see_doctor"],
                nearby_options=MEDASSIST_RESPONSES["fever"]["nearby"]
            )
        else:
            symptom_response = """🤕
Let me help you with your symptoms!
Please describe what you're feeling in detail."""
        
        conversation.append({"role": "assistant", "content": symptom_response})
        
        return conversation

    def generate_medication_reminder_conversation(self) -> List[Dict[str, str]]:
        """Generate medication reminder conversation flow."""
        conversation = []
        
        # Bot sends medication reminder
        medication = random.choice(self.medications)
        dosage = random.choice(["1 tablet", "2 tablets", "1 capsule", "1 spoon"])
        time = random.choice(["9:00 AM", "2:00 PM", "8:00 PM", "10:00 PM"])
        streak = random.randint(1, 30)
        
        reminder_response = self.templates.medication_reminder(medication, dosage, time, streak)
        conversation.append({"role": "assistant", "content": reminder_response})
        
        # User confirms taking medication
        conversation.append({"role": "user", "content": "✅"})
        
        # Bot confirms and encourages
        confirmation_response = self.templates.medication_confirmation(medication, streak + 1)
        conversation.append({"role": "assistant", "content": confirmation_response})
        
        return conversation

    def generate_health_tips_conversation(self) -> List[Dict[str, str]]:
        """Generate health tips conversation."""
        conversation = []
        
        # User requests health tips
        user_input = random.choice(["tips", "health tips", "daily tip", "स्वास्थ्य टिप्स"])
        conversation.append({"role": "user", "content": user_input})
        
        # Bot provides health tip
        tip_response = self.templates.health_tip_daily()
        conversation.append({"role": "assistant", "content": tip_response})
        
        return conversation

    def generate_web_app_transition_conversation(self) -> List[Dict[str, str]]:
        """Generate web app transition conversation."""
        conversation = []
        
        # User requests web app or detailed analysis
        user_input = random.choice([
            "web", "web app", "detailed analysis", "more features",
            "full analysis", "comprehensive check"
        ])
        conversation.append({"role": "user", "content": user_input})
        
        # Bot provides web app transition message
        transition_response = self.templates.web_app_transition()
        conversation.append({"role": "assistant", "content": transition_response})
        
        return conversation

    def generate_family_care_conversation(self) -> List[Dict[str, str]]:
        """Generate family care update conversation."""
        conversation = []
        
        # Bot sends family care update
        patient_name = random.choice(["Rahul", "Priya", "Amit", "Neha"])
        status = random.choice(["stable", "improving", "under observation", "recovering"])
        location = random.choice(["Apollo Hospital", "City Hospital", "Ruby Hall Clinic"])
        doctor = random.choice(["Dr. Sharma", "Dr. Patel", "Dr. Singh", "Dr. Kumar"])
        last_update = random.choice(["2 minutes ago", "5 minutes ago", "10 minutes ago"])
        
        update_response = self.templates.family_care_update(
            patient_name, status, location, doctor, last_update
        )
        conversation.append({"role": "assistant", "content": update_response})
        
        # User acknowledges
        conversation.append({"role": "user", "content": "Thanks for the update"})
        
        return conversation

    def generate_corporate_wellness_conversation(self) -> List[Dict[str, str]]:
        """Generate corporate wellness conversation."""
        conversation = []
        
        # Bot sends corporate wellness summary
        company_name = random.choice(["TechCorp Ltd", "Innovate Solutions", "Global Systems"])
        employee_count = random.randint(100, 500)
        health_score = round(random.uniform(6.5, 8.5), 1)
        achievements = [
            "23% reduction in sick days",
            "67 employees completed health assessments",
            "15 chronic conditions identified early"
        ]
        alerts = [
            "Flu season approaching - vaccination drive recommended",
            "12 employees with high stress indicators",
            "8 employees overdue for annual checkups"
        ]
        
        wellness_response = self.templates.corporate_wellness_summary(
            company_name, employee_count, health_score, achievements, alerts
        )
        conversation.append({"role": "assistant", "content": wellness_response})
        
        return conversation

    def generate_medical_advice_conversation(self) -> List[Dict[str, str]]:
        """Generate medical advice conversation."""
        conversation = []
        
        # User asks about medical condition
        condition = random.choice(["diabetes", "hypertension", "blood pressure", "diabetes management"])
        user_input = f"I have {condition}, what should I do?"
        conversation.append({"role": "user", "content": user_input})
        
        # Bot provides medical advice
        if "diabetes" in condition.lower():
            advice_response = f"""💊
{MEDASSIST_RESPONSES['diabetes']['advice_type']}
📋
Recommendations:
{chr(10).join([f'• {rec}' for rec in MEDASSIST_RESPONSES['diabetes']['recommendations']])}
⚠
Important Notes:
{chr(10).join([f'• {warn}' for warn in MEDASSIST_RESPONSES['diabetes']['warnings']])}
🏥
{MEDASSIST_RESPONSES['diabetes']['follow_up']}"""
        else:
            advice_response = f"""💊
{MEDASSIST_RESPONSES['hypertension']['advice_type']}
📋
Recommendations:
{chr(10).join([f'• {rec}' for rec in MEDASSIST_RESPONSES['hypertension']['recommendations']])}
⚠
Important Notes:
{chr(10).join([f'• {warn}' for warn in MEDASSIST_RESPONSES['hypertension']['warnings']])}
🏥
{MEDASSIST_RESPONSES['hypertension']['follow_up']}"""
        
        conversation.append({"role": "assistant", "content": advice_response})
        
        return conversation

    def generate_training_dataset(self, num_examples: int = 3000) -> List[Dict[str, str]]:
        """Generate a complete training dataset for MedAssist AI."""
        dataset = []
        
        conversation_types = [
            "welcome", "symptom_checker", "emergency", "voice_message",
            "medication_reminder", "health_tips", "web_app_transition",
            "family_care", "corporate_wellness", "medical_advice"
        ]
        
        for i in range(num_examples):
            # Randomly choose conversation type
            conv_type = random.choice(conversation_types)
            
            if conv_type == "welcome":
                conversation = self.generate_welcome_conversation()
            elif conv_type == "symptom_checker":
                conversation = self.generate_symptom_checker_conversation()
            elif conv_type == "emergency":
                conversation = self.generate_emergency_conversation()
            elif conv_type == "voice_message":
                conversation = self.generate_voice_message_conversation()
            elif conv_type == "medication_reminder":
                conversation = self.generate_medication_reminder_conversation()
            elif conv_type == "health_tips":
                conversation = self.generate_health_tips_conversation()
            elif conv_type == "web_app_transition":
                conversation = self.generate_web_app_transition_conversation()
            elif conv_type == "family_care":
                conversation = self.generate_family_care_conversation()
            elif conv_type == "corporate_wellness":
                conversation = self.generate_corporate_wellness_conversation()
            else:
                conversation = self.generate_medical_advice_conversation()
            
            # Convert to training format
            training_example = {
                "messages": conversation,
                "category": conv_type
            }
            dataset.append(training_example)
        
        return dataset

    def save_dataset(self, dataset: List[Dict], filename: str):
        """Save the generated dataset to a JSON file."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(dataset, f, indent=2, ensure_ascii=False)
        print(f"MedAssist AI dataset saved to {filename} with {len(dataset)} examples")

def main():
    """Generate and save MedAssist AI training dataset."""
    generator = MedAssistDataGenerator()
    
    # Generate dataset
    print("Generating MedAssist AI training dataset...")
    dataset = generator.generate_training_dataset(num_examples=3000)
    
    # Save dataset
    generator.save_dataset(dataset, "medassist_ai_dataset.json")
    
    # Print some examples
    print("\nExample conversations:")
    for i, example in enumerate(dataset[:3]):
        print(f"\n--- Example {i+1} ({example['category']}) ---")
        for message in example['messages']:
            print(f"{message['role'].upper()}: {message['content'][:100]}...")

if __name__ == "__main__":
    main() 