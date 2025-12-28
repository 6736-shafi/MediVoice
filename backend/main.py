"""
MediVoice AI - Multilingual Voice Medical Assistant
Main FastAPI application entry point
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="MediVoice AI",
    description="Multilingual Voice Medical Assistant powered by Google Gemini and ElevenLabs",
    version="1.0.0"
)

# CORS Configuration
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class ReportRequest(BaseModel):
    conversation_history: List[dict]
    language: str = "en"

class ConversationRequest(BaseModel):
    message: str
    language: str = "en"
    patient_id: Optional[str] = None
    conversation_history: Optional[List[dict]] = []

class ConversationResponse(BaseModel):
    text_response: str
    audio_url: Optional[str] = None
    conversation_id: str
    language: str
    medical_context: Optional[dict] = None

class HealthCheckResponse(BaseModel):
    status: str
    version: str
    services: dict

# Health Check Endpoint
@app.get("/", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "services": {
            "gemini": "configured" if os.getenv("GOOGLE_API_KEY") else "not_configured",
            "elevenlabs": "configured" if os.getenv("ELEVENLABS_API_KEY") else "not_configured"
        }
    }

@app.get("/api/health")
async def api_health():
    """API health check"""
    return {"status": "ok", "message": "MediVoice AI is running"}

@app.post("/api/conversation", response_model=ConversationResponse)
async def create_conversation(request: ConversationRequest):
    """
    Main conversation endpoint
    Processes user message, generates AI response, and returns voice audio
    """
    try:
        logger.info(f"Received conversation request in language: {request.language}")
        
        # Import services (lazy loading to avoid startup issues)
        from services.gemini_service import GeminiService
        from services.elevenlabs_service import ElevenLabsService
        
        # Initialize services
        gemini_service = GeminiService()
        elevenlabs_service = ElevenLabsService()
        
        # Generate AI response using Gemini
        ai_response = await gemini_service.generate_medical_response(
            user_message=request.message,
            conversation_history=request.conversation_history,
            language=request.language
        )
        
        # Generate voice audio using ElevenLabs
        audio_data = await elevenlabs_service.text_to_speech(
            text=ai_response["text"],
            language=request.language
        )
        
        # Return response
        return ConversationResponse(
            text_response=ai_response["text"],
            audio_url=audio_data["audio_url"],
            conversation_id=ai_response.get("conversation_id", "default"),
            language=request.language,
            medical_context=ai_response.get("medical_context")
        )
        
    except Exception as e:
        logger.error(f"Error in conversation endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/report")
async def generate_report(request: ReportRequest):
    """Generate medical report from conversation"""
    try:
        from services.gemini_service import GeminiService
        service = GeminiService()
        report = await service.generate_consultation_report(request.conversation_history)
        return {"report": report}
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/voice-input")
async def process_voice_input(audio: UploadFile = File(...), language: str = "en"):
    """
    Process voice input from user
    Converts speech to text and processes the conversation
    """
    try:
        logger.info(f"Received voice input in language: {language}")
        
        # Import services
        from services.speech_service import SpeechService
        
        # Initialize speech service
        speech_service = SpeechService()
        
        # Read audio file
        audio_content = await audio.read()
        
        # Convert speech to text
        transcription = await speech_service.speech_to_text(
            audio_content=audio_content,
            language=language
        )
        
        return {
            "transcription": transcription,
            "language": language
        }
        
    except Exception as e:
        logger.error(f"Error in voice input endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/languages")
async def get_supported_languages():
    """Get list of supported languages"""
    return {
        "languages": [
            {"code": "en", "name": "English", "flag": "🇺🇸"},
            {"code": "es", "name": "Spanish", "flag": "🇪🇸"},
            {"code": "hi", "name": "Hindi", "flag": "🇮🇳"},
            {"code": "ar", "name": "Arabic", "flag": "🇸🇦"},
            {"code": "zh", "name": "Chinese", "flag": "🇨🇳"},
            {"code": "fr", "name": "French", "flag": "🇫🇷"},
            {"code": "de", "name": "German", "flag": "🇩🇪"},
            {"code": "pt", "name": "Portuguese", "flag": "🇧🇷"},
            {"code": "ru", "name": "Russian", "flag": "🇷🇺"},
            {"code": "ja", "name": "Japanese", "flag": "🇯🇵"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
