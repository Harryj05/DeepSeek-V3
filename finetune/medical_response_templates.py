"""
Medical Response Templates for DeepSeek-V3 Fine-tuning
This module contains structured response templates for medical chatbot responses.
"""

from typing import Dict, List, Optional

class MedicalResponseTemplates:
    """Templates for structured medical responses with emojis and formatting."""
    
    @staticmethod
    def yellow_alert_response(
        conditions: List[str],
        actions: List[str],
        see_doctor_conditions: List[str],
        nearby_options: List[Dict[str, str]],
        web_app_link: str = "https://medical-assistant.app"
    ) -> str:
        """Generate a yellow alert response for non-emergency medical situations."""
        conditions_str = "\n".join([f"• {condition}" for condition in conditions])
        actions_str = "\n".join([f"• {action}" for action in actions])
        doctor_conditions_str = "\n".join([f"• {condition}" for condition in see_doctor_conditions])
        nearby_str = "\n".join([
            f"• {option['name']} - {option['distance']} (₹{option['cost']})" 
            for option in nearby_options
        ])
        
        return f"""⚠
YELLOW ALERT - Medical Attention Recommended
📋
Possible Conditions:
{conditions_str}
🏥
Immediate Actions:
{actions_str}
⚠
See doctor if:
{doctor_conditions_str}
🏥
Nearby Options:
{nearby_str}
Need more detailed analysis? Check our web app: [{web_app_link}]"""

    @staticmethod
    def emergency_response(
        emergency_type: str,
        phone_numbers: List[str],
        nearest_hospitals: List[Dict[str, str]],
        waiting_instructions: List[str]
    ) -> str:
        """Generate an emergency response for critical medical situations."""
        phone_str = "\n".join([f"• {phone}" for phone in phone_numbers])
        hospitals_str = "\n".join([
            f"• {hospital['name']} - {hospital['distance']} \n  {hospital['phone']}" 
            for hospital in nearest_hospitals
        ])
        instructions_str = "\n".join([f"• {instruction}" for instruction in waiting_instructions])
        
        return f"""🚨
{emergency_type.upper()} EMERGENCY - ACT NOW!
🏥
CALL IMMEDIATELY:
{phone_str}
⏰
WHILE WAITING:
{instructions_str}
📍
Share location with family/friends \n  I'm monitoring - reply if condition changes"""

    @staticmethod
    def voice_processing_response(
        understood_text: str,
        is_correct: bool = True
    ) -> str:
        """Generate a response for voice message processing."""
        if is_correct:
            return f"""🎤
Voice received! Processing...
I understood: "{understood_text}" Is this correct?
✅
Yes
❌
No (type correct symptom)"""
        else:
            return f"""🎤
Voice received! Processing...
I understood: "{understood_text}" Is this correct?
✅
Yes
❌
No (type correct symptom)"""

    @staticmethod
    def symptom_analysis_response(
        symptom: str,
        follow_up_questions: List[str]
    ) -> str:
        """Generate a response for symptom analysis."""
        questions_str = "\n".join([f"• {question}" for question in follow_up_questions])
        
        return f"""🤕
{symptom} - Let me help!
When did it start?
{questions_str}"""

    @staticmethod
    def general_medical_advice(
        advice_type: str,
        recommendations: List[str],
        warnings: List[str],
        follow_up: str
    ) -> str:
        """Generate general medical advice responses."""
        rec_str = "\n".join([f"• {rec}" for rec in recommendations])
        warn_str = "\n".join([f"• {warn}" for warn in warnings])
        
        return f"""💊
{advice_type.upper()}
📋
Recommendations:
{rec_str}
⚠
Important Notes:
{warn_str}
🏥
{follow_up}"""

# Predefined response patterns for common medical scenarios
COMMON_RESPONSES = {
    "fever": {
        "conditions": ["Viral fever (most likely)", "Seasonal flu", "COVID-19 (get tested)"],
        "actions": ["Rest and hydrate", "Paracetamol for fever", "Monitor temperature"],
        "see_doctor": ["Fever >101°F for >3 days", "Breathing difficulty", "Severe weakness"],
        "nearby": [
            {"name": "Dr. Sharma Clinic", "distance": "2km", "cost": "200"},
            {"name": "City Hospital", "distance": "5km", "cost": "500"},
            {"name": "Call: 102 (Ambulance)", "distance": "", "cost": ""}
        ]
    },
    "chest_pain": {
        "emergency_type": "HEART EMERGENCY",
        "phone_numbers": ["108 - Emergency Ambulance", "102 - Medical Emergency"],
        "hospitals": [
            {"name": "Apollo Hospital", "distance": "3.2km", "phone": "020-1234-5678"},
            {"name": "Ruby Hall Clinic", "distance": "4.1km", "phone": "020-8765-4321"}
        ],
        "waiting_instructions": [
            "Sit down, don't lie flat",
            "Chew aspirin if available", 
            "Stay calm, help is coming"
        ]
    },
    "stomach_pain": {
        "symptom": "Stomach pain",
        "questions": [
            "Few hours ago",
            "Today", 
            "Yesterday",
            "More than a week ago"
        ]
    }
} 