"""
MedAssist AI WhatsApp Bot API Server
Flask API for n8n integration with fine-tuned DeepSeek-V3 model
"""

import os
import json
import torch
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import re
from typing import Dict, List, Optional
import time

# Import MedAssist templates
import sys
sys.path.append('..')
from medassist_response_templates import MedAssistResponseTemplates, MEDASSIST_RESPONSES

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for n8n integration

class MedAssistWhatsAppBot:
    """WhatsApp bot using fine-tuned MedAssist AI model."""
    
    def __init__(self, model_path: str = "./medassist_ai_model"):
        self.model_path = model_path
        self.tokenizer = None
        self.model = None
        self.templates = MedAssistResponseTemplates()
        
        # User session management
        self.user_sessions = {}
        
        # Load model
        self.load_model()
    
    def load_model(self):
        """Load the fine-tuned MedAssist AI model."""
        try:
            logger.info("Loading MedAssist AI model...")
            
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
            
            # Load fine-tuned weights
            self.model = PeftModel.from_pretrained(base_model, self.model_path)
            self.model.eval()
            
            logger.info("MedAssist AI model loaded successfully!")
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def classify_user_input(self, user_input: str) -> str:
        """Classify user input to determine response type."""
        user_input_lower = user_input.lower()
        
        # Emergency detection
        if any(word in user_input_lower for word in ["emergency", "urgent", "help", "तत्काल", "जरूरी"]):
            return "emergency"
        
        # Symptom detection
        if any(word in user_input_lower for word in ["fever", "temperature", "hot", "बुखार", "headache", "pain", "दर्द"]):
            return "symptom_checker"
        
        # Voice message detection
        if "[Voice message:" in user_input or "voice" in user_input_lower:
            return "voice_message"
        
        # Medication related
        if any(word in user_input_lower for word in ["medication", "medicine", "pill", "tablet", "💊"]):
            return "medication"
        
        # Health tips
        if any(word in user_input_lower for word in ["tips", "health tips", "wellness", "advice"]):
            return "health_tips"
        
        # Web app transition
        if any(word in user_input_lower for word in ["web", "app", "detailed", "comprehensive"]):
            return "web_app"
        
        # Welcome/greeting
        if any(word in user_input_lower for word in ["hi", "hello", "start", "begin", "नमस्ते"]):
            return "welcome"
        
        return "general"
    
    def generate_response(self, user_input: str, user_id: str = None) -> Dict[str, str]:
        """Generate response using fine-tuned model or templates."""
        try:
            # Get user session
            session = self.user_sessions.get(user_id, {})
            
            # Classify input
            input_type = self.classify_user_input(user_input)
            
            # Handle different input types
            if input_type == "welcome":
                response = self.templates.welcome_message()
                session["onboarding_step"] = 1
                
            elif input_type == "emergency":
                response = self.templates.emergency_mode_activation()
                session["emergency_mode"] = True
                
            elif input_type == "symptom_checker":
                if "fever" in user_input.lower() or "बुखार" in user_input:
                    response = self.templates.yellow_alert_response(
                        conditions=MEDASSIST_RESPONSES["fever"]["conditions"],
                        actions=MEDASSIST_RESPONSES["fever"]["actions"],
                        see_doctor_conditions=MEDASSIST_RESPONSES["fever"]["see_doctor"],
                        nearby_options=MEDASSIST_RESPONSES["fever"]["nearby"]
                    )
                elif "chest" in user_input.lower() or "सीने" in user_input:
                    response = self.templates.emergency_response(
                        emergency_type=MEDASSIST_RESPONSES["chest_pain"]["emergency_type"],
                        phone_numbers=MEDASSIST_RESPONSES["chest_pain"]["phone_numbers"],
                        nearest_hospitals=MEDASSIST_RESPONSES["chest_pain"]["hospitals"],
                        waiting_instructions=MEDASSIST_RESPONSES["chest_pain"]["waiting_instructions"]
                    )
                else:
                    response = self.templates.symptom_checker_intro()
                    
            elif input_type == "voice_message":
                # Extract voice content
                voice_match = re.search(r'\[Voice message: (.+?)\]', user_input)
                if voice_match:
                    voice_content = voice_match.group(1)
                    if "pet mein dard" in voice_content or "stomach" in voice_content.lower():
                        understood_text = "Stomach pain"
                    elif "बुखार" in voice_content or "fever" in voice_content.lower():
                        understood_text = "Fever"
                    else:
                        understood_text = "Medical symptom"
                    
                    response = self.templates.voice_processing_response(understood_text)
                else:
                    response = self.templates.voice_processing_response("Medical symptom")
                    
            elif input_type == "medication":
                response = self.templates.medication_reminder("Vitamin D", "1 tablet", "9:00 AM", 12)
                
            elif input_type == "health_tips":
                response = self.templates.health_tip_daily()
                
            elif input_type == "web_app":
                response = self.templates.web_app_transition()
                
            else:
                # Use fine-tuned model for general responses
                response = self._generate_with_model(user_input, session)
            
            # Update session
            self.user_sessions[user_id] = session
            
            return {
                "response": response,
                "input_type": input_type,
                "session": session,
                "timestamp": time.time()
            }
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                "response": "I'm sorry, I'm having trouble processing your request. Please try again or contact support.",
                "input_type": "error",
                "session": session,
                "timestamp": time.time()
            }
    
    def _generate_with_model(self, user_input: str, session: Dict) -> str:
        """Generate response using the fine-tuned model."""
        try:
            # Prepare input
            if session.get("onboarding_step"):
                # Handle onboarding flow
                if session["onboarding_step"] == 1:
                    prompt = f"User: {user_input}\nAssistant:"
                else:
                    prompt = f"User: {user_input}\nAssistant:"
            else:
                prompt = f"User: {user_input}\nAssistant:"
            
            # Tokenize
            inputs = self.tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
            
            # Generate
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=500,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the assistant part
            if "Assistant:" in response:
                response = response.split("Assistant:")[-1].strip()
            
            return response
            
        except Exception as e:
            logger.error(f"Error in model generation: {e}")
            return "I'm sorry, I'm having trouble processing your request. Please try again."

# Initialize bot
bot = None

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for n8n."""
    return jsonify({
        "status": "healthy",
        "service": "MedAssist AI WhatsApp Bot",
        "model_loaded": bot is not None
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Main chat endpoint for n8n integration."""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({"error": "Message is required"}), 400
        
        user_message = data['message']
        user_id = data.get('user_id', 'default_user')
        
        # Generate response
        result = bot.generate_response(user_message, user_id)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/webhook', methods=['POST'])
def webhook():
    """Webhook endpoint for WhatsApp Business API integration."""
    try:
        data = request.get_json()
        
        # Extract message from WhatsApp webhook
        if 'entry' in data and len(data['entry']) > 0:
            entry = data['entry'][0]
            if 'changes' in entry and len(entry['changes']) > 0:
                change = entry['changes'][0]
                if 'value' in change and 'messages' in change['value']:
                    message = change['value']['messages'][0]
                    
                    user_id = message.get('from', 'unknown')
                    user_message = message.get('text', {}).get('body', '')
                    
                    # Generate response
                    result = bot.generate_response(user_message, user_id)
                    
                    # Return response for n8n to send back to WhatsApp
                    return jsonify({
                        "user_id": user_id,
                        "response": result["response"],
                        "input_type": result["input_type"]
                    })
        
        return jsonify({"status": "no message processed"})
        
    except Exception as e:
        logger.error(f"Error in webhook endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/session/<user_id>', methods=['GET'])
def get_session(user_id):
    """Get user session data."""
    session = bot.user_sessions.get(user_id, {})
    return jsonify({"user_id": user_id, "session": session})

@app.route('/session/<user_id>', methods=['DELETE'])
def clear_session(user_id):
    """Clear user session data."""
    if user_id in bot.user_sessions:
        del bot.user_sessions[user_id]
    return jsonify({"status": "session cleared"})

def initialize_bot():
    """Initialize the MedAssist bot."""
    global bot
    try:
        model_path = os.getenv('MEDASSIST_MODEL_PATH', './medassist_ai_model')
        bot = MedAssistWhatsAppBot(model_path)
        logger.info("MedAssist WhatsApp Bot initialized successfully!")
    except Exception as e:
        logger.error(f"Failed to initialize bot: {e}")
        raise

if __name__ == '__main__':
    # Initialize bot
    initialize_bot()
    
    # Run server
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 