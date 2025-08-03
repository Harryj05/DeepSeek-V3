"""
MedAssist AI Response Templates for DeepSeek-V3 Fine-tuning
Comprehensive templates for the dual-platform healthcare intelligence system.
"""

from typing import Dict, List, Optional
import random

class MedAssistResponseTemplates:
    """Templates for MedAssist AI structured responses with emojis and formatting."""
    
    @staticmethod
    def welcome_message(user_name: str = None) -> str:
        """Generate welcome message for new users."""
        if user_name:
            return f"""🏥 Welcome to MedAssist AI!

Hi {user_name}! I'm your Health Buddy 🤖

Choose your language:
1️⃣ English
2️⃣ हिंदी
3️⃣ தமிழ்
4️⃣ বাংলা

Type your choice (1-4) to get started!"""
        else:
            return """🏥 Welcome to MedAssist AI!

I'm your Health Buddy 🤖 - Your AI-powered healthcare companion!

Choose your language:
1️⃣ English
2️⃣ हिंदी
3️⃣ தமிழ்
4️⃣ বাংলা

Type your choice (1-4) to get started!"""

    @staticmethod
    def onboarding_flow(step: int, user_data: Dict = None) -> str:
        """Generate onboarding flow messages."""
        if step == 1:
            return """👋 Great! Let's set up your profile:

What's your name?"""
        elif step == 2:
            return f"""Hi {user_data.get('name', 'there')}! 

What's your age?"""
        elif step == 3:
            return f"""📍 Which city/district are you in?"""
        elif step == 4:
            return f"""Perfect! Your Health Buddy is ready! ✅

🔹 Type 'symptoms' - Check symptoms
🚨 Type 'emergency' - Get emergency help
💡 Type 'tips' - Daily health tips
🌐 Type 'web' - Access full features

💡 Pro tip: For detailed health analysis, try our web app: [medassist.ai]"""

    @staticmethod
    def symptom_checker_intro() -> str:
        """Generate symptom checker introduction."""
        return """🤖 I'm here to help!

Tell me what you're feeling. You can:
📝 Type your symptoms
🎤 Send voice message
📷 Send photo if visible

What's bothering you today?"""

    @staticmethod
    def yellow_alert_response(
        conditions: List[str],
        actions: List[str],
        see_doctor_conditions: List[str],
        nearby_options: List[Dict[str, str]],
        web_app_link: str = "medassist.ai"
    ) -> str:
        """Generate a yellow alert response for moderate medical situations."""
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
🏥
NEAREST CARDIAC CARE:
{hospitals_str}
⏰
WHILE WAITING:
{instructions_str}
📍
Share location with family/friends \n  I'm monitoring - reply if condition changes"""

    @staticmethod
    def emergency_mode_activation() -> str:
        """Generate emergency mode activation message."""
        return """🚨
EMERGENCY MODE ACTIVATED
Are you experiencing:
• Chest pain/Heart attack
• Breathing difficulty
• Severe bleeding
• Unconsciousness
• Other emergency

Reply with the number (1-5) or describe your emergency."""

    @staticmethod
    def voice_processing_response(
        understood_text: str,
        is_correct: bool = True
    ) -> str:
        """Generate a response for voice message processing."""
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
    def medication_reminder(
        medication_name: str,
        dosage: str,
        time: str,
        streak_days: int = 0
    ) -> str:
        """Generate medication reminder message."""
        if streak_days > 0:
            return f"""💊
Medication Reminder
Time for your {medication_name} ({dosage})!

Reply ✅ when taken or ⏰ to snooze 1 hour

Streak: {streak_days} days 🎉"""
        else:
            return f"""💊
Medication Reminder
Time for your {medication_name} ({dosage})!

Reply ✅ when taken or ⏰ to snooze 1 hour"""

    @staticmethod
    def medication_confirmation(
        medication_name: str,
        streak_days: int,
        next_dose_time: str = None
    ) -> str:
        """Generate medication confirmation message."""
        if next_dose_time:
            return f"""Great! {medication_name} logged ✅
Streak: {streak_days} days 🎉
Keep it up! Your health is improving.

Next dose: {next_dose_time}"""
        else:
            return f"""Great! {medication_name} logged ✅
Streak: {streak_days} days 🎉
Keep it up! Your health is improving."""

    @staticmethod
    def health_tip_daily() -> str:
        """Generate daily health tip."""
        tips = [
            "💧 Stay hydrated! Drink 8-10 glasses of water daily",
            "🚶‍♂️ Take a 30-minute walk today for better heart health",
            "😴 Get 7-8 hours of quality sleep tonight",
            "🥗 Include more vegetables in your meals today",
            "🧘‍♀️ Practice 10 minutes of meditation for stress relief",
            "☀️ Get 15 minutes of sunlight for Vitamin D",
            "📱 Take a 5-minute break from screens every hour",
            "🏃‍♂️ Do some light stretching exercises"
        ]
        return f"""💡 Daily Health Tip:

{random.choice(tips)}

Want personalized tips? Try our web app: [medassist.ai]"""

    @staticmethod
    def web_app_transition(symptoms: str = None) -> str:
        """Generate web app transition message."""
        if symptoms:
            return f"""🌐 For detailed analysis of your symptoms, try our web app:

medassist.ai/analysis?ref=wa_bot&symptoms={symptoms}

Features you'll get:
📊 Comprehensive health analysis
📈 Symptom tracking over time
🏥 Doctor recommendations
💊 Medication management
📋 Health reports storage"""
        else:
            return """🌐 Access full MedAssist AI features on our web app:

medassist.ai

Features:
📊 Comprehensive health analysis
📈 Symptom tracking over time
🏥 Doctor recommendations
💊 Medication management
📋 Health reports storage
🎯 Personalized health goals"""

    @staticmethod
    def family_care_update(
        patient_name: str,
        status: str,
        location: str,
        doctor: str,
        last_update: str
    ) -> str:
        """Generate family care update message."""
        return f"""📱 MedAssist Update:

{patient_name} is {status} and under medical care at {location}.

Attending: Dr. {doctor}
Last Update: {last_update}

Track status: [medassist.ai/family]"""

    @staticmethod
    def corporate_wellness_summary(
        company_name: str,
        employee_count: int,
        health_score: float,
        achievements: List[str],
        alerts: List[str]
    ) -> str:
        """Generate corporate wellness summary."""
        achievements_str = "\n".join([f"✅ {achievement}" for achievement in achievements])
        alerts_str = "\n".join([f"⚠ {alert}" for alert in alerts])
        
        return f"""🏢 {company_name} - Health Overview

📊 Health Metrics:
• Overall Score: {health_score}/10
• Active Users: {employee_count} employees
• Platform Usage: 72% engagement

Monthly Highlights:
{achievements_str}

Alerts:
{alerts_str}

View full report: [medassist.ai/corporate]"""

# Predefined response patterns for common medical scenarios
MEDASSIST_RESPONSES = {
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
    "headache": {
        "conditions": ["Tension headache", "Migraine", "Sinus headache", "Stress-related"],
        "actions": ["Rest in quiet, dark room", "Stay hydrated", "Avoid triggers"],
        "see_doctor": ["Severe sudden headache", "Headache with fever", "Vision changes"],
        "nearby": [
            {"name": "Neurology Clinic", "distance": "3km", "cost": "300"},
            {"name": "General Hospital", "distance": "4km", "cost": "400"}
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
    },
    "diabetes": {
        "advice_type": "DIABETES MANAGEMENT",
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
        "advice_type": "HYPERTENSION MANAGEMENT",
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