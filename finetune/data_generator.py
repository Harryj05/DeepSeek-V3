"""
Data Generator for Medical Chatbot Fine-tuning
Generates training data with the specific medical response format.
"""

import json
import random
from typing import List, Dict, Tuple
from medical_response_templates import MedicalResponseTemplates, COMMON_RESPONSES

class MedicalDataGenerator:
    """Generates training data for medical chatbot fine-tuning."""
    
    def __init__(self):
        self.templates = MedicalResponseTemplates()
        
        # Common medical symptoms and their variations
        self.symptoms = {
            "fever": [
                "I have fever", "I'm running a temperature", "I feel hot", 
                "My body temperature is high", "I have a high fever",
                "मुझे बुखार है", "I have fever and headache"
            ],
            "chest_pain": [
                "I have chest pain", "My chest hurts", "Pain in my chest",
                "Chest discomfort", "Heart pain", "Pain in heart area",
                "मेरे सीने में दर्द है", "Chest pain and shortness of breath"
            ],
            "stomach_pain": [
                "I have stomach pain", "My stomach hurts", "Abdominal pain",
                "Belly ache", "Stomach ache", "Pain in abdomen",
                "मुझे पेट में दर्द है", "Stomach pain and nausea"
            ],
            "headache": [
                "I have headache", "My head hurts", "Head pain",
                "Migraine", "Severe headache", "Head pounding",
                "सिर दर्द", "Headache and dizziness"
            ],
            "emergency": [
                "emergency", "help urgent", "urgent medical help",
                "emergency situation", "need immediate help",
                "तत्काल सहायता", "emergency medical attention"
            ]
        }
        
        # Emergency scenarios
        self.emergency_scenarios = {
            "chest_pain": "HEART EMERGENCY",
            "breathing_difficulty": "RESPIRATORY EMERGENCY", 
            "severe_bleeding": "TRAUMA EMERGENCY",
            "unconsciousness": "NEUROLOGICAL EMERGENCY"
        }
        
        # Voice message scenarios
        self.voice_scenarios = [
            "Mujhe pet mein dard hai", "मुझे बुखार है", "I have fever",
            "Chest pain", "Headache", "Stomach ache"
        ]

    def generate_fever_conversation(self) -> List[Dict[str, str]]:
        """Generate a conversation about fever symptoms."""
        conversation = []
        
        # User reports fever
        user_input = random.choice(self.symptoms["fever"])
        conversation.append({"role": "user", "content": user_input})
        
        # Bot responds with yellow alert
        response = self.templates.yellow_alert_response(
            conditions=COMMON_RESPONSES["fever"]["conditions"],
            actions=COMMON_RESPONSES["fever"]["actions"],
            see_doctor_conditions=COMMON_RESPONSES["fever"]["see_doctor"],
            nearby_options=COMMON_RESPONSES["fever"]["nearby"]
        )
        conversation.append({"role": "assistant", "content": response})
        
        return conversation

    def generate_emergency_conversation(self) -> List[Dict[str, str]]:
        """Generate an emergency conversation flow."""
        conversation = []
        
        # User says emergency
        user_input = random.choice(self.symptoms["emergency"])
        conversation.append({"role": "user", "content": user_input})
        
        # Bot activates emergency mode
        emergency_response = """🚨
EMERGENCY MODE ACTIVATED
Are you experiencing:
• Chest pain/Heart attack
• Breathing difficulty
• Severe bleeding
• Unconsciousness
• Other emergency"""
        conversation.append({"role": "assistant", "content": emergency_response})
        
        # User selects chest pain
        conversation.append({"role": "user", "content": "1"})
        
        # Bot responds with heart emergency
        heart_response = self.templates.emergency_response(
            emergency_type=COMMON_RESPONSES["chest_pain"]["emergency_type"],
            phone_numbers=COMMON_RESPONSES["chest_pain"]["phone_numbers"],
            nearest_hospitals=COMMON_RESPONSES["chest_pain"]["hospitals"],
            waiting_instructions=COMMON_RESPONSES["chest_pain"]["waiting_instructions"]
        )
        conversation.append({"role": "assistant", "content": heart_response})
        
        return conversation

    def generate_voice_conversation(self) -> List[Dict[str, str]]:
        """Generate a voice message conversation flow."""
        conversation = []
        
        # User sends voice message
        voice_text = random.choice(self.voice_scenarios)
        conversation.append({"role": "user", "content": f"[Voice message: {voice_text}]"})
        
        # Bot processes voice
        voice_response = self.templates.voice_processing_response(voice_text)
        conversation.append({"role": "assistant", "content": voice_response})
        
        # User confirms
        conversation.append({"role": "user", "content": "Yes"})
        
        # Bot continues with symptom analysis
        if "pet mein dard" in voice_text or "stomach" in voice_text.lower():
            symptom_response = self.templates.symptom_analysis_response(
                symptom="Stomach pain",
                follow_up_questions=COMMON_RESPONSES["stomach_pain"]["questions"]
            )
            conversation.append({"role": "assistant", "content": symptom_response})
        
        return conversation

    def generate_general_medical_advice(self) -> List[Dict[str, str]]:
        """Generate general medical advice conversations."""
        advice_topics = {
            "diabetes": {
                "recommendations": [
                    "Monitor blood sugar regularly",
                    "Follow prescribed diet",
                    "Exercise regularly",
                    "Take medications as prescribed"
                ],
                "warnings": [
                    "Avoid high sugar foods",
                    "Check feet daily for wounds",
                    "Keep emergency contacts handy"
                ],
                "follow_up": "Schedule regular check-ups with your doctor"
            },
            "hypertension": {
                "recommendations": [
                    "Reduce salt intake",
                    "Exercise regularly",
                    "Manage stress",
                    "Monitor blood pressure"
                ],
                "warnings": [
                    "Avoid excessive salt",
                    "Limit alcohol consumption",
                    "Don't skip medications"
                ],
                "follow_up": "Visit your doctor for blood pressure monitoring"
            }
        }
        
        topic = random.choice(list(advice_topics.keys()))
        conversation = []
        
        # User asks about medical condition
        user_input = f"I have {topic}, what should I do?"
        conversation.append({"role": "user", "content": user_input})
        
        # Bot provides advice
        advice_response = self.templates.general_medical_advice(
            advice_type=topic.upper(),
            recommendations=advice_topics[topic]["recommendations"],
            warnings=advice_topics[topic]["warnings"],
            follow_up=advice_topics[topic]["follow_up"]
        )
        conversation.append({"role": "assistant", "content": advice_response})
        
        return conversation

    def generate_training_dataset(self, num_examples: int = 1000) -> List[Dict[str, str]]:
        """Generate a complete training dataset."""
        dataset = []
        
        for i in range(num_examples):
            # Randomly choose conversation type
            conv_type = random.choice([
                "fever", "emergency", "voice", "general_advice"
            ])
            
            if conv_type == "fever":
                conversation = self.generate_fever_conversation()
            elif conv_type == "emergency":
                conversation = self.generate_emergency_conversation()
            elif conv_type == "voice":
                conversation = self.generate_voice_conversation()
            else:
                conversation = self.generate_general_medical_advice()
            
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
        print(f"Dataset saved to {filename} with {len(dataset)} examples")

def main():
    """Generate and save training dataset."""
    generator = MedicalDataGenerator()
    
    # Generate dataset
    print("Generating medical chatbot training dataset...")
    dataset = generator.generate_training_dataset(num_examples=2000)
    
    # Save dataset
    generator.save_dataset(dataset, "medical_chatbot_dataset.json")
    
    # Print some examples
    print("\nExample conversations:")
    for i, example in enumerate(dataset[:3]):
        print(f"\n--- Example {i+1} ({example['category']}) ---")
        for message in example['messages']:
            print(f"{message['role'].upper()}: {message['content'][:100]}...")

if __name__ == "__main__":
    main() 