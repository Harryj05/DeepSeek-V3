"""
Test Script for Fine-tuned Medical Chatbot
Tests the model with various medical scenarios.
"""

import torch
import json
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
from medical_response_templates import MedicalResponseTemplates

class MedicalChatbotTester:
    """Test class for the fine-tuned medical chatbot."""
    
    def __init__(self, model_path: str = "./medical_chatbot_model"):
        self.model_path = model_path
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = None
        self.model = None
        self.templates = MedicalResponseTemplates()

    def load_model(self):
        """Load the fine-tuned model."""
        print("Loading fine-tuned model...")
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_path,
            trust_remote_code=True
        )
        
        # Load base model
        base_model = AutoModelForCausalLM.from_pretrained(
            "deepseek-ai/DeepSeek-V3",
            torch_dtype=torch.bfloat16,
            device_map="auto",
            trust_remote_code=True,
            load_in_8bit=True
        )
        
        # Load LoRA weights
        self.model = PeftModel.from_pretrained(base_model, self.model_path)
        self.model.eval()
        
        print("Model loaded successfully!")

    def generate_response(self, prompt: str, max_length: int = 512, temperature: float = 0.7) -> str:
        """Generate a response for the given prompt."""
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Extract only the generated part (after the prompt)
        response = response[len(prompt):].strip()
        return response

    def test_fever_scenario(self):
        """Test fever symptom scenario."""
        print("\n" + "="*50)
        print("TESTING FEVER SCENARIO")
        print("="*50)
        
        prompt = "User: I have fever\nAssistant:"
        response = self.generate_response(prompt)
        print(f"Prompt: {prompt}")
        print(f"Response: {response}")
        
        # Test Hindi input
        prompt_hindi = "User: मुझे बुखार है\nAssistant:"
        response_hindi = self.generate_response(prompt_hindi)
        print(f"\nPrompt (Hindi): {prompt_hindi}")
        print(f"Response: {response_hindi}")

    def test_emergency_scenario(self):
        """Test emergency scenario."""
        print("\n" + "="*50)
        print("TESTING EMERGENCY SCENARIO")
        print("="*50)
        
        # Emergency activation
        prompt = "User: emergency\nAssistant:"
        response = self.generate_response(prompt)
        print(f"Prompt: {prompt}")
        print(f"Response: {response}")
        
        # Emergency with chest pain selection
        prompt_chest = "User: emergency\nAssistant: 🚨\nEMERGENCY MODE ACTIVATED\nAre you experiencing:\n• Chest pain/Heart attack\n• Breathing difficulty\n• Severe bleeding\n• Unconsciousness\n• Other emergency\nUser: 1\nAssistant:"
        response_chest = self.generate_response(prompt_chest)
        print(f"\nPrompt (Chest Pain): {prompt_chest[:100]}...")
        print(f"Response: {response_chest}")

    def test_voice_scenario(self):
        """Test voice message processing scenario."""
        print("\n" + "="*50)
        print("TESTING VOICE MESSAGE SCENARIO")
        print("="*50)
        
        prompt = "User: [Voice message: Mujhe pet mein dard hai]\nAssistant:"
        response = self.generate_response(prompt)
        print(f"Prompt: {prompt}")
        print(f"Response: {response}")
        
        # Voice confirmation flow
        prompt_confirm = "User: [Voice message: Mujhe pet mein dard hai]\nAssistant: 🎤\nVoice received! Processing...\nI understood: \"Stomach pain\" Is this correct?\n✅\nYes\n❌\nNo (type correct symptom)\nUser: Yes\nAssistant:"
        response_confirm = self.generate_response(prompt_confirm)
        print(f"\nPrompt (Confirmation): {prompt_confirm[:100]}...")
        print(f"Response: {response_confirm}")

    def test_medical_advice(self):
        """Test general medical advice scenarios."""
        print("\n" + "="*50)
        print("TESTING MEDICAL ADVICE SCENARIOS")
        print("="*50)
        
        # Diabetes advice
        prompt_diabetes = "User: I have diabetes, what should I do?\nAssistant:"
        response_diabetes = self.generate_response(prompt_diabetes)
        print(f"Prompt: {prompt_diabetes}")
        print(f"Response: {response_diabetes}")
        
        # Hypertension advice
        prompt_hypertension = "User: I have high blood pressure, what should I do?\nAssistant:"
        response_hypertension = self.generate_response(prompt_hypertension)
        print(f"\nPrompt: {prompt_hypertension}")
        print(f"Response: {response_hypertension}")

    def test_custom_scenarios(self):
        """Test custom medical scenarios."""
        print("\n" + "="*50)
        print("TESTING CUSTOM SCENARIOS")
        print("="*50)
        
        test_cases = [
            "I have a severe headache",
            "My chest hurts and I can't breathe properly",
            "I have been vomiting for the past 2 hours",
            "I have a cut that won't stop bleeding",
            "I feel dizzy and lightheaded"
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            prompt = f"User: {test_case}\nAssistant:"
            response = self.generate_response(prompt)
            print(f"\nTest Case {i}: {test_case}")
            print(f"Response: {response}")

    def compare_with_templates(self):
        """Compare model responses with template responses."""
        print("\n" + "="*50)
        print("COMPARING WITH TEMPLATES")
        print("="*50)
        
        # Fever template
        template_response = self.templates.yellow_alert_response(
            conditions=["Viral fever (most likely)", "Seasonal flu", "COVID-19 (get tested)"],
            actions=["Rest and hydrate", "Paracetamol for fever", "Monitor temperature"],
            see_doctor_conditions=["Fever >101°F for >3 days", "Breathing difficulty", "Severe weakness"],
            nearby_options=[
                {"name": "Dr. Sharma Clinic", "distance": "2km", "cost": "200"},
                {"name": "City Hospital", "distance": "5km", "cost": "500"},
                {"name": "Call: 102 (Ambulance)", "distance": "", "cost": ""}
            ]
        )
        
        print("Template Response (Fever):")
        print(template_response)
        
        # Model response for fever
        prompt = "User: I have fever\nAssistant:"
        model_response = self.generate_response(prompt)
        print(f"\nModel Response (Fever):")
        print(model_response)

    def run_all_tests(self):
        """Run all test scenarios."""
        try:
            self.load_model()
            
            self.test_fever_scenario()
            self.test_emergency_scenario()
            self.test_voice_scenario()
            self.test_medical_advice()
            self.test_custom_scenarios()
            self.compare_with_templates()
            
            print("\n" + "="*50)
            print("ALL TESTS COMPLETED")
            print("="*50)
            
        except Exception as e:
            print(f"Testing failed: {e}")
            raise

def main():
    """Main function to run tests."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test fine-tuned medical chatbot")
    parser.add_argument("--model_path", default="./medical_chatbot_model",
                       help="Path to fine-tuned model")
    
    args = parser.parse_args()
    
    tester = MedicalChatbotTester(model_path=args.model_path)
    tester.run_all_tests()

if __name__ == "__main__":
    main() 