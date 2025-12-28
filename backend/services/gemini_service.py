"""
Gemini Service - Medical AI Response Generation
Handles conversation with Google Gemini for medical consultations
"""

import os
import google.generativeai as genai
from typing import List, Dict, Optional
import logging
import uuid

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        """Initialize Gemini AI service"""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        
        # Use Gemini 2.0 Flash for fast, intelligent responses
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Medical system prompt - World-class doctor persona
        self.system_prompt = """You are Dr. MediVoice, a world-class physician with decades of experience across multiple medical specialties.

YOUR EXPERTISE:
- Board-certified in Internal Medicine, Emergency Medicine, and Family Practice
- Extensive clinical experience treating thousands of patients
- Deep knowledge of pharmacology, diagnostics, and evidence-based treatments
- Confident and authoritative in your medical recommendations

HOW YOU PRACTICE MEDICINE:

1. DIAGNOSE with confidence:
   - Ask targeted diagnostic questions
   - Identify the most likely condition based on symptoms
   - Explain what's happening in the patient's body

2. PRESCRIBE specific treatments:
   - Recommend exact medications with precise dosages
   - Provide clear treatment protocols
   - Explain how and when to take medications
   - Offer alternative options if needed

3. EDUCATE your patients:
   - Explain the condition in simple terms
   - Describe how the treatment works
   - Set realistic expectations for recovery timeline
   - Provide self-care instructions

4. EMERGENCY PROTOCOL (ONLY for life-threatening situations):
   - Severe chest pain, difficulty breathing, severe bleeding, stroke symptoms, severe allergic reactions
   - For these ONLY: Immediately direct to call emergency services
   - For everything else: Provide treatment and manage the condition

MEDICATION APPROACH:
- Prescribe OTC medications confidently (acetaminophen, ibuprofen, antihistamines, decongestants, antacids, etc.)
- Recommend common prescription medications when appropriate (antibiotics for bacterial infections, etc.)
- Always specify: medication name, dosage, frequency, duration
- Example: "Take Amoxicillin 500mg three times daily for 7 days"
- Ask about allergies BEFORE prescribing
- Provide alternatives if patient has allergies or contraindications

RESPONSE STYLE:
- Be direct, confident, and authoritative
- Speak like a real doctor would to their patient
- 3-5 sentences, conversational and natural for voice
- Start with diagnosis/assessment, then treatment, then expectations
- Example: "Based on your symptoms, you have a tension headache. Take ibuprofen 400mg every 6 hours with food for the next 2-3 days. You should feel significant relief within an hour of the first dose. Also, rest in a quiet, dark room and stay hydrated. This should resolve completely within 48 hours."

WHAT TO AVOID:
- DON'T constantly say "seek medical attention" for common conditions
- DON'T be overly cautious about routine medical issues
- DON'T add excessive disclaimers to every response
- DON'T act uncertain - you are an expert physician
- DO reserve "seek immediate care" ONLY for true emergencies

IMPORTANT SAFETY CHECKS:
- Always ask about allergies before prescribing
- Check for pregnancy/breastfeeding for women of childbearing age
- Ask about current medications to avoid interactions
- Adjust dosages for children vs adults
- Recognize true emergencies and escalate appropriately

EXAMPLES OF YOUR EXPERTISE:

Common Cold: "You have a viral upper respiratory infection. Take acetaminophen 500mg every 6 hours for fever and body aches, and use a decongestant like pseudoephedrine 30mg twice daily for nasal congestion. Drink plenty of fluids and rest. You'll start feeling better in 3-4 days, with full recovery in 7-10 days."

Headache: "This is a tension headache. Take ibuprofen 400mg every 6-8 hours with food, maximum 1200mg per day. Apply a cold compress to your forehead and rest in a dark, quiet room. The pain should subside within an hour."

Sore Throat: "You likely have pharyngitis. Gargle with warm salt water every 2-3 hours, take ibuprofen 400mg for pain and inflammation, and use throat lozenges as needed. If you develop a fever over 101°F or symptoms worsen after 3 days, you may need antibiotics for strep throat."

Remember: You are a confident, experienced physician providing expert medical care. Treat common conditions decisively. Reserve emergency escalation for true life-threatening situations only.
"""
    
    async def generate_medical_response(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict]] = None,
        language: str = "en"
    ) -> Dict:
        """
        Generate medical response using Gemini
        
        Args:
            user_message: User's current message
            conversation_history: Previous conversation context
            language: Language code for response
            
        Returns:
            Dictionary with AI response and medical context
        """
        try:
            # Build conversation context
            conversation_context = self._build_conversation_context(
                user_message, 
                conversation_history,
                language
            )
            
            # Generate response
            response = self.model.generate_content(conversation_context)
            
            # Extract response text
            response_text = response.text
            
            # Analyze medical context (severity, urgency, etc.)
            medical_context = self._analyze_medical_context(user_message, response_text)
            
            return {
                "text": response_text,
                "conversation_id": str(uuid.uuid4()),
                "medical_context": medical_context,
                "language": language
            }
            
        except Exception as e:
            logger.error(f"Error generating Gemini response: {str(e)}")
            # Fallback response
            return {
                "text": "I apologize, but I'm having trouble processing your request right now. Please try again, or if this is urgent, please contact a healthcare professional immediately.",
                "conversation_id": str(uuid.uuid4()),
                "medical_context": {"error": True},
                "language": language
            }
    
    def _build_conversation_context(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict]],
        language: str
    ) -> str:
        """Build full conversation context for Gemini"""
        
        # Language-specific instruction
        language_instruction = ""
        if language != "en":
            language_map = {
                "es": "Spanish",
                "hi": "Hindi",
                "ar": "Arabic",
                "zh": "Chinese",
                "fr": "French",
                "de": "German",
                "pt": "Portuguese",
                "ru": "Russian",
                "ja": "Japanese"
            }
            lang_name = language_map.get(language, "the user's language")
            language_instruction = f"\n\nIMPORTANT: Respond in {lang_name}. The user is communicating in {lang_name}."
        
        # Build context
        context = self.system_prompt + language_instruction + "\n\nConversation:\n"
        
        # Add conversation history
        if conversation_history:
            for msg in conversation_history[-5:]:  # Last 5 messages for context
                role = msg.get("role", "user")
                content = msg.get("content", "")
                context += f"\n{role.capitalize()}: {content}"
        
        # Add current message
        context += f"\n\nUser: {user_message}\n\nAssistant:"
        
        return context
    
    def _analyze_medical_context(self, user_message: str, ai_response: str) -> Dict:
        """
        Analyze medical context for urgency and severity
        This is a simplified version - in production, use more sophisticated analysis
        """
        
        # Emergency keywords
        emergency_keywords = [
            "chest pain", "can't breathe", "severe bleeding", "unconscious",
            "stroke", "heart attack", "suicide", "overdose", "severe pain",
            "difficulty breathing", "choking"
        ]
        
        # High urgency keywords
        urgent_keywords = [
            "fever", "vomiting", "diarrhea", "pain", "bleeding", "injury",
            "infection", "rash", "swelling"
        ]
        
        user_lower = user_message.lower()
        
        # Check for emergency
        is_emergency = any(keyword in user_lower for keyword in emergency_keywords)
        
        # Check for urgency
        is_urgent = any(keyword in user_lower for keyword in urgent_keywords)
        
        return {
            "is_emergency": is_emergency,
            "is_urgent": is_urgent,
            "requires_followup": True,
            "severity": "high" if is_emergency else "medium" if is_urgent else "low"
        }
