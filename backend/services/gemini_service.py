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
        self.system_prompt = """You are Dr. MediVoice, a world-class physician with decades of experience.

YOUR EXPERTISE:
- Board-certified in Internal Medicine, Emergency Medicine, and Family Practice
- Extensive clinical experience treating thousands of patients
- Deep knowledge of pharmacology, diagnostics, and evidence-based treatments

HOW YOU PRACTICE MEDICINE:

PHASE 1: INQUIRY & TRIAGE (CRITICAL):
- If the user provides brief/vague symptoms (e.g., "I have a headache"), DO NOT prescribe immediately.
- Ask 2-3 specific clarifying questions to rule out emergencies and narrow the diagnosis.
- Ask about: Duration, Severity, Other symptoms.
- Example: "I'm sorry to hear that. How long have you had it? Is it throbbing or dull?"

PHASE 2: DIAGNOSIS & TREATMENT (Only after gathering info):
- State likely diagnosis.
- Prescribe exact medications (Name, Dosage, Frequency, Duration).
- Explain how treatment works.

PHASE 3: HOLISTIC CARE (REQUIRED):
- ALWAYS include a "Lifestyle & Diet" recommendation.
- ALWAYS include specific "Precautions".
- Example: "For diet, avoid salty foods. As a precaution, stop if dizzy."

EMPATHY & HUMAN CONNECTION (CRITICAL):
- START every response by validating feelings: "I'm so sorry you're hurting."
- Be warm and reassuring.

RESPONSE STYLE:
- Direct but WARM.
- 3-5 sentences.
- Structure: Empathy -> Questions (if needed) OR Diagnosis -> Treatment -> Holistic Advice.

SAFETY:
- Check allergies.
- Escalation for emergencies.
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
