# 🏥 MediVoice AI - Multilingual Voice Medical Assistant

**Winning Solution for ElevenLabs + Google Cloud AI Hackathon**

MediVoice AI is an intelligent, multilingual voice medical assistant that combines the power of Google Gemini AI with ElevenLabs' natural voice synthesis to provide accessible healthcare guidance in 10+ languages.

![MediVoice AI](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![React](https://img.shields.io/badge/React-18.3-61dafb)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📑 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Roadmap](#-roadmap)
- [License](#-license)

---

## 🌟 Features

### 🗣️ **Multilingual Voice Conversations**
- Support for **10+ languages**: English, Spanish, Hindi, Arabic, Chinese, French, German, Portuguese, Russian, Japanese
- Natural, empathetic voice responses using **ElevenLabs** text-to-speech
- Real-time audio visualization and playback
- Voice input processing with speech-to-text

### 🤖 **Intelligent Medical AI**
- Powered by **Google Gemini 2.0 Flash** for fast, accurate medical guidance
- **Diagnostic Flow**: Asks clarifying questions before prescribing (duration, severity, symptoms)
- **Holistic Care**: Provides lifestyle, diet, and precautionary advice with every consultation
- Context-aware conversations with medical history tracking
- Emergency detection and urgent care recommendations
- Symptom analysis and preliminary health assessments
- Medication information with specific dosages and instructions

### 🎨 **Premium User Experience**
- Modern, responsive dark-mode interface
- Smooth animations and transitions
- Intuitive voice-first design
- Real-time conversation display with message history
- Language switcher with flag indicators
- **PDF Report Generation**: Download professional medical consultation summaries
- One-click report export with diagnosis, medications, and lifestyle advice

### 🔒 **Safety & Privacy**
- Clear disclaimers about AI limitations
- Automatic emergency detection with immediate alerts
- HIPAA-compliant design principles
- No permanent storage of personal health information
- Secure API key management

---

## 🏗️ Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                           │
│                  (React + Vite - Port 5173)                  │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │  Language  │  │ Voice Input  │  │ Conversation │        │
│  │  Selector  │  │   Module     │  │   Display    │        │
│  └────────────┘  └──────────────┘  └──────────────┘        │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            │ REST API (HTTP/JSON)
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                   FASTAPI BACKEND                            │
│                    (Python 3.11 - Port 8000)                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              API Layer (main.py)                      │  │
│  │  • /api/conversation  • /api/voice-input             │  │
│  │  • /api/health        • /api/languages               │  │
│  │  • /api/report        (PDF Generation)               │  │
│  └──────────────┬───────────────────┬───────────────────┘  │
│                 │                   │                       │
│  ┌──────────────▼─────────┐  ┌─────▼──────────────┐       │
│  │   Gemini Service       │  │ ElevenLabs Service │       │
│  │  (gemini_service.py)   │  │(elevenlabs_service)│       │
│  └──────────────┬─────────┘  └─────┬──────────────┘       │
│                 │                   │                       │
│  ┌──────────────▼─────────────────┐ │                      │
│  │     Speech Service              │ │                      │
│  │   (speech_service.py)           │ │                      │
│  └─────────────────────────────────┘ │                      │
└──────────────────┬────────────────────┼──────────────────────┘
                   │                    │
        ┌──────────▼─────────┐  ┌──────▼──────────┐
        │  Google Gemini     │  │   ElevenLabs    │
        │  2.0 Flash API     │  │   Voice API     │
        │  (Medical AI)      │  │  (Multilingual) │
        └────────────────────┘  └─────────────────┘
```

### Data Flow

**Text Conversation Flow:**
```
User Input → Frontend → POST /api/conversation → Backend
  → Gemini AI (Medical Response) → ElevenLabs (Voice Synthesis)
  → Backend Response (Text + Audio) → Frontend Display + Playback
```

**Voice Input Flow:**
```
Voice Recording → Frontend → POST /api/voice-input → Backend
  → Speech-to-Text → Text Conversation Flow
```

## 🚀 Quick Start

### Prerequisites

Ensure you have the following installed:
- **Python 3.11+** ([Download](https://www.python.org/downloads/))
- **Node.js 20.19+ or 22.12+** ([Download](https://nodejs.org/))
- **Google Cloud Account** with Gemini API access
- **ElevenLabs API Key** ([Get API Key](https://elevenlabs.io/))

### Installation & Setup

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd medivoice-ai
```

#### 2. Backend Setup

**Step 2.1: Create Virtual Environment**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows
```

**Step 2.2: Install Dependencies**
```bash
pip install -r requirements.txt
```

**Step 2.3: Configure Environment Variables**

Create a `.env` file in the root directory:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```env
# Google Gemini API
GOOGLE_API_KEY=your_google_api_key_here

# ElevenLabs API
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Optional Configuration
PORT=8000
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

**Step 2.4: Start Backend Server**
```bash
cd backend
python main.py
```

✅ Backend will run on `http://localhost:8000`

#### 3. Frontend Setup

**Step 3.1: Navigate to Frontend Directory**
```bash
cd frontend
```

**Step 3.2: Install Dependencies**
```bash
npm install
```

**Step 3.3: Start Development Server**
```bash
npm run dev
```

✅ Frontend will run on `http://localhost:5173`

### Verify Installation

1. Open your browser and navigate to `http://localhost:5173`
2. You should see the MediVoice AI interface
3. Select a language and start a conversation
4. Check the browser console for any errors

---


## 📖 Usage

1. **Select Your Language**: Choose from 10+ supported languages
2. **Start Conversation**: Type or speak your symptoms
3. **Get AI Response**: Receive intelligent medical guidance with voice
4. **Continue Dialogue**: Ask follow-up questions naturally
5. **Emergency Detection**: Automatic alerts for urgent situations

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework
- **Google Gemini 2.0 Flash**: Advanced AI for medical reasoning
- **ElevenLabs API**: Multilingual voice synthesis
- **Python 3.11**: Core programming language

### Frontend
- **React 18**: UI framework
- **Vite**: Build tool and dev server
- **Axios**: HTTP client
- **Lucide React**: Icon library

### Cloud Infrastructure
- **Google Cloud Platform**: Hosting and AI services
- **Vertex AI**: AI model deployment
- **Cloud Run**: Serverless deployment (planned)

## 🎯 Hackathon Criteria

### ✅ Technological Implementation
- Full integration of Google Cloud (Gemini AI, Vertex AI)
- ElevenLabs multilingual voice synthesis
- Production-ready FastAPI backend
- Modern React frontend with real-time features

### ✅ Design
- Premium, accessible medical UI
- Intuitive voice-first interface
- Responsive across devices
- Professional medical aesthetics

### ✅ Potential Impact
- Breaks language barriers in healthcare
- 24/7 medical guidance availability
- Serves underserved communities
- Reduces healthcare access inequality

### ✅ Quality of Idea
- Novel combination of voice AI + medical expertise
- Addresses real-world healthcare challenges
- Scalable and extensible architecture
- Clear value proposition

## 🔐 Security & Privacy

- No personal health information stored permanently
- Secure API key management
- HTTPS encryption (in production)
- Clear user consent and disclaimers

## 📝 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Health Check

**GET /**
```bash
curl http://localhost:8000/
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "services": {
    "gemini": "configured",
    "elevenlabs": "configured"
  }
}
```

#### 2. API Health Check

**GET /api/health**
```bash
curl http://localhost:8000/api/health
```

**Response:**
```json
{
  "status": "ok",
  "message": "MediVoice AI is running"
}
```

#### 3. Create Conversation

**POST /api/conversation**

Generate AI medical response with voice synthesis.

**Request Body:**
```json
{
  "message": "I have a headache and feel dizzy",
  "language": "en",
  "patient_id": "optional_patient_id",
  "conversation_history": [
    {
      "role": "user",
      "content": "Previous message"
    },
    {
      "role": "assistant",
      "content": "Previous response"
    }
  ]
}
```

**Response:**
```json
{
  "text_response": "Based on your symptoms...",
  "audio_url": "data:audio/mpeg;base64,...",
  "conversation_id": "conv_123",
  "language": "en",
  "medical_context": {
    "is_emergency": false,
    "symptoms_detected": ["headache", "dizziness"]
  }
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I have a fever",
    "language": "en",
    "conversation_history": []
  }'
```

#### 4. Voice Input Processing

**POST /api/voice-input**

Convert voice audio to text transcription.

**Request:**
- Content-Type: `multipart/form-data`
- Parameters:
  - `audio`: Audio file (File)
  - `language`: Language code (string, default: "en")

**Response:**
```json
{
  "transcription": "I have a headache",
  "language": "en"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/voice-input \
  -F "audio=@recording.wav" \
  -F "language=en"
```

#### 5. Get Supported Languages

**GET /api/languages**

**Response:**
```json
{
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
```

#### 6. Generate Medical Report

**POST /api/report**

Generate a downloadable PDF medical report from conversation history.

**Request Body:**
```json
{
  "conversation_history": [
    {
      "role": "user",
      "content": "I have a headache"
    },
    {
      "role": "assistant",
      "content": "I'm sorry to hear that. How long have you had it?"
    }
  ],
  "language": "en"
}
```

**Response:**
```json
{
  "report": "{\"patient_symptoms\":\"Headache\",\"diagnosis\":\"Tension headache\",\"medications\":[\"Ibuprofen 400mg\"],\"lifestyle_advice\":\"Rest and hydration\",\"precautions\":\"Avoid bright lights\",\"follow_up\":\"If persists >3 days\"}"
}
```

**Frontend Usage:**
The frontend uses `jsPDF` to parse this JSON and generate a professional PDF document with:
- Patient symptoms summary
- Diagnosis
- Prescribed medications with dosages
- Lifestyle and diet recommendations
- Precautions and warnings
- Follow-up care instructions

---

## 📁 Project Structure

```
medivoice-ai/
├── backend/
│   ├── main.py                    # FastAPI application entry point
│   ├── services/
│   │   ├── __init__.py
│   │   ├── gemini_service.py      # Google Gemini AI integration
│   │   ├── elevenlabs_service.py  # ElevenLabs voice synthesis
│   │   └── speech_service.py      # Speech-to-text processing
│   └── __pycache__/
├── frontend/
│   ├── src/
│   │   ├── App.jsx                # Main React component
│   │   ├── App.css                # Application styles
│   │   ├── main.jsx               # React entry point
│   │   └── index.css              # Global styles
│   ├── public/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── node_modules/
├── venv/                          # Python virtual environment
├── .env                           # Environment variables (not in git)
├── .env.example                   # Environment template
├── .gitignore
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Description | Default |
|----------|----------|-------------|----------|
| `GOOGLE_API_KEY` | ✅ Yes | Google Gemini API key | - |
| `ELEVENLABS_API_KEY` | ✅ Yes | ElevenLabs API key | - |
| `PORT` | ❌ No | Backend server port | `8000` |
| `ALLOWED_ORIGINS` | ❌ No | CORS allowed origins | `http://localhost:3000,http://localhost:5173` |

### Getting API Keys

#### Google Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file

#### ElevenLabs API Key
1. Sign up at [ElevenLabs](https://elevenlabs.io/)
2. Navigate to Profile → API Keys
3. Generate a new API key
4. Copy the key to your `.env` file

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Backend fails to start with "python-multipart" error

**Error:**
```
ERROR: Form data requires "python-multipart" to be installed
```

**Solution:**
```bash
source venv/bin/activate
pip install python-multipart
```

#### 2. "API key not valid" error

**Solution:**
- Verify your `.env` file exists in the root directory
- Check that API keys are correctly copied (no extra spaces)
- Ensure you're using valid, active API keys
- Restart the backend server after updating `.env`

#### 3. CORS errors in browser console

**Error:**
```
Access to fetch at 'http://localhost:8000' has been blocked by CORS policy
```

**Solution:**
- Ensure backend is running on port 8000
- Check `ALLOWED_ORIGINS` in `.env` includes `http://localhost:5173`
- Restart both frontend and backend servers

#### 4. Frontend not connecting to backend

**Solution:**
1. Verify backend is running: `curl http://localhost:8000/api/health`
2. Check frontend API URL configuration
3. Ensure no firewall is blocking port 8000
4. Check browser console for error messages

#### 5. Voice synthesis not working

**Solution:**
- Verify ElevenLabs API key is valid
- Check ElevenLabs account has available credits
- Review backend logs for ElevenLabs API errors
- Test with a simple text message first

#### 6. Virtual environment activation issues

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

### Debug Mode

Enable detailed logging:

**Backend:**
```python
# In backend/main.py, logging is already configured
# Check terminal output for detailed logs
```

**Frontend:**
```javascript
// Open browser DevTools (F12)
// Check Console tab for errors
// Check Network tab for API requests
```

### Getting Help

- Check the [Issues](https://github.com/your-repo/issues) page
- Review backend logs in terminal
- Check browser console for frontend errors
- Verify all prerequisites are installed

---

## 🚧 Roadmap

- [ ] Web Speech API integration for voice input
- [ ] Patient dashboard with health tracking
- [ ] Medication reminders
- [ ] Doctor appointment scheduling
- [ ] Integration with health records
- [ ] Mobile app (iOS/Android)
- [ ] Telemedicine video calls

## 📄 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines.

## 👥 Team

Built for the Google Cloud AI Accelerate Hackathon 2025

## 📞 Support

For issues and questions, please open a GitHub issue.

## ⚠️ Disclaimer

MediVoice AI is an AI-powered informational tool and is NOT a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.

---

**Made with ❤️ using Google Cloud AI and ElevenLabs**
