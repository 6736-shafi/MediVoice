"""
ElevenLabs Service - Voice Synthesis
Handles text-to-speech conversion using ElevenLabs API
"""

import os
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
import logging
import base64
from typing import Dict

logger = logging.getLogger(__name__)

class ElevenLabsService:
    def __init__(self):
        """Initialize ElevenLabs service"""
        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            raise ValueError("ELEVENLABS_API_KEY not found in environment variables")
        
        self.client = ElevenLabs(api_key=api_key)
        
        # Voice configurations for different languages
        # Using multilingual voices from ElevenLabs
        self.voice_configs = {
            "en": {
                "voice_id": "pNInz6obpgDQGcFmaJgB",  # Adam - warm, professional
                "name": "Adam"
            },
            "es": {
                "voice_id": "pNInz6obpgDQGcFmaJgB",  # Multilingual voice
                "name": "Adam"
            },
            "hi": {
                "voice_id": "pNInz6obpgDQGcFmaJgB",
                "name": "Adam"
            },
            "ar": {
                "voice_id": "pNInz6obpgDQGcFmaJgB",
                "name": "Adam"
            },
            "zh": {
                "voice_id": "pNInz6obpgDQGcFmaJgB",
                "name": "Adam"
            },
            "fr": {
                "voice_id": "pNInz6obpgDQGcFmaJgB",
                "name": "Adam"
            },
            "de": {
                "voice_id": "pNInz6obpgDQGcFmaJgB",
                "name": "Adam"
            },
            "pt": {
                "voice_id": "pNInz6obpgDQGcFmaJgB",
                "name": "Adam"
            },
            "ru": {
                "voice_id": "pNInz6obpgDQGcFmaJgB",
                "name": "Adam"
            },
            "ja": {
                "voice_id": "pNInz6obpgDQGcFmaJgB",
                "name": "Adam"
            }
        }
    
    async def text_to_speech(
        self,
        text: str,
        language: str = "en",
        voice_id: str = None
    ) -> Dict:
        """
        Convert text to speech using ElevenLabs
        
        Args:
            text: Text to convert to speech
            language: Language code
            voice_id: Optional specific voice ID to use
            
        Returns:
            Dictionary with audio data and metadata
        """
        try:
            # Get voice configuration for language
            voice_config = self.voice_configs.get(language, self.voice_configs["en"])
            selected_voice_id = voice_id or voice_config["voice_id"]
            
            logger.info(f"Generating speech for language: {language} with voice: {voice_config['name']}")
            
            # Generate audio using ElevenLabs
            audio_generator = self.client.text_to_speech.convert(
                voice_id=selected_voice_id,
                text=text,
                model_id="eleven_multilingual_v2",  # Multilingual model
                voice_settings=VoiceSettings(
                    stability=0.4,  # Lower stability = more expressive/variable
                    similarity_boost=0.75,
                    style=0.6,      # Higher style = more natural intonation
                    use_speaker_boost=True
                )
            )
            
            # Collect audio bytes
            audio_bytes = b""
            for chunk in audio_generator:
                audio_bytes += chunk
            
            # Convert to base64 for easy transmission
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
            
            return {
                "audio_url": f"data:audio/mpeg;base64,{audio_base64}",
                "audio_bytes": audio_bytes,
                "language": language,
                "voice_name": voice_config["name"],
                "format": "mp3"
            }
            
        except Exception as e:
            logger.error(f"Error generating speech with ElevenLabs: {str(e)}")
            raise Exception(f"Failed to generate speech: {str(e)}")
    
    async def get_available_voices(self) -> Dict:
        """Get list of available voices from ElevenLabs"""
        try:
            voices = self.client.voices.get_all()
            return {
                "voices": [
                    {
                        "voice_id": voice.voice_id,
                        "name": voice.name,
                        "category": voice.category if hasattr(voice, 'category') else "general"
                    }
                    for voice in voices.voices
                ]
            }
        except Exception as e:
            logger.error(f"Error fetching voices: {str(e)}")
            return {"voices": [], "error": str(e)}
