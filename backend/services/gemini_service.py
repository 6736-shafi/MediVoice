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
        
    def _get_system_prompt(self, conversation_history: List[Dict]) -> str:
        """
        Get the appropriate system prompt based on conversation state
        """
        # Check if AI has already greeted/spoken
        has_ai_spoken = False
        if conversation_history:
            for msg in conversation_history:
                if msg.get("role") == "model" or msg.get("role") == "assistant":
                    has_ai_spoken = True
                    break
        
        # STATE 1: INITIAL CONTACT (AI hasn't spoken yet)
        if not has_ai_spoken:
            return """You are Dr. MediVoice, a friendly and empathetic AI doctor.

YOUR GOAL:
- Greet the user warmly ONCE.
- Ask ONE open-ended question to understand their concern.
- Example: "Hello! I'm Dr. MediVoice. How can I help you today?"

RULES:
- DO NOT give medical advice yet.
- DO NOT ask specific diagnostic questions yet.
- JUST GREET and LISTEN.
"""

        # STATE 2: CONSULTATION (AI has already spoken)
        return """You are Dr. MediVoice, a world-class physician.

*** STRICT CONSTRAINTS - READ CAREFULLY ***
1. NO GREETINGS: You have ALREADY greeted the user. DO NOT say "Hello" again.
2. NO REFERRALS: DO NOT say "please see a doctor" or "go to the nearest hospital" unless it is a life-threatening emergency (heart attack, stroke, severe bleeding).
3. BE DECISIVE: You are the doctor. Diagnose and treat RIGHT NOW.

MEMORY & CONTEXT:
- IF USER ALREADY GAVE SYMPTOMS/DURATION, DO NOT ASK AGAIN.
- IF USER SAID "NO SYMPTOMS", ACCEPT IT AND MOVE TO DIAGNOSIS.

DIAGNOSTIC FLOW:
1. GATHER DATA: If (Duration OR Severity) is missing, ask for it.
2. DIAGNOSE & TREAT: If you have basic info, GIVE THE PLAN.

RESPONSE STRUCTURE (Use Markdown):
1. **Diagnosis**: [State likely condition]
2. **Medication**: [Name] [Dosage] [Frequency] [Duration] (Explain reasoning)
3. **Diet & Lifestyle**: [Specific food/exercise recommendations]
4. **Precautions**: [Side effects/Warnings]

EXAMPLE RESPONSE:
"Since your headache is dull and started a month ago, it is likely a Tension Headache.
**RX:** Ibuprofen 400mg, take 1 tablet every 6 hours with food for 3 days.
**Diet:** Drink 3L of water daily. Avoid caffeine.
**Exercise:** Do neck stretches twice daily.
**Note:** If vision changes occur, seek urgent care."
"""

    async def generate_medical_response(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict]] = None,
        language: str = "en"
    ) -> Dict:
        """
        Generate medical response using Gemini
        """
        try:
            # Build conversation context with DYNAMIC prompt
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

    async def generate_consultation_report(self, conversation_history: List[Dict]) -> Dict:
        """
        Generate a structured medical report from conversation history
        """
        try:
            # Create a transcript string
            transcript = "\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in conversation_history])
            
            prompt = f"""
            Analyze this medical consultation transcript and generate a structured summary report.
            
            TRANSCRIPT:
            {transcript}
            
            OUTPUT IN JSON FORMAT ONLY:
            {{
                "patient_symptoms": "Summary of symptoms reported",
                "diagnosis": "Likely diagnosis provided",
                "medications": ["List of medications prescribed"],
                "lifestyle_advice": "Diet and lifestyle recommendations given",
                "precautions": "Safety warnings and precautions mentioned",
                "follow_up": "When to seek further care"
            }}
            """
            
            response = self.model.generate_content(prompt)
            # Clean up response to ensure valid JSON (remove markdown code blocks if present)
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:-3]
            elif text.startswith("```"):
                text = text[3:-3]
                
            return text  # It's a JSON string, user can parse it
            
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            return '{"error": "Failed to generate report"}'
    
    def _build_conversation_context(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict]],
        language: str
    ) -> str:
        """Build full conversation context for Gemini"""
        
        # Get DYNAMIC system prompt based on history state
        current_system_prompt = self._get_system_prompt(conversation_history)
        
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
        context = current_system_prompt + language_instruction + "\n\nConversation:\n"
        
        # Add conversation history
        if conversation_history:
            for msg in conversation_history[-10:]:  # Last 10 messages
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
