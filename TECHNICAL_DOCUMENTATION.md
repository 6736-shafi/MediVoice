# MediVoice AI - Technical Documentation

**Version:** 1.1.0  
**Last Updated:** December 29, 2025  
**Author:** MediVoice AI Team

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Architecture](#2-architecture)
3. [Technology Stack](#3-technology-stack)
4. [Backend Implementation](#4-backend-implementation)
5. [Frontend Implementation](#5-frontend-implementation)
6. [API Reference](#6-api-reference)
7. [Deployment](#10-deployment)

---

## 1. System Overview

### 1.1 Purpose
MediVoice AI is a multilingual voice medical assistant designed to provide accessible healthcare guidance through natural language conversations. The system combines advanced AI capabilities with voice synthesis to break language barriers in healthcare.

---

## 2. Architecture

### 2.1 High-Level Architecture (Cloud Native)

```
┌─────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                       │
│           (React SPA on Cloud Run: medivoice-web)            │
│  Components:                                                 │
│  • Language Selector    • Voice Input Module                │
│  • Conversation Display • Audio Player                       │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            │ HTTPS / REST
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    APPLICATION LAYER                         │
│           (FastAPI on Cloud Run: medivoice-api)              │
│  endpoints: /api/conversation, /api/voice-input, etc.        │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            │ API Calls
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                   EXTERNAL SERVICES                          │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │ Google Gemini    │  │   ElevenLabs     │                │
│  │ 2.0 Flash API    │  │   Voice API      │                │
│  └──────────────────┘  └──────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Request Flow

#### Text Conversation Flow
1. **User Input** -> Frontend Validation
2. **POST** to `medivoice-api` endpoint `/api/conversation`
3. **Backend Processing**:
   - `GeminiService` constructs prompt and calls Google Gemini.
   - `ElevenLabsService` synthesizes the text response to audio.
4. **Response**: Backend returns JSON with text and Base64 audio URL.
5. **Frontend**: Displays text and plays audio.

---

## 3. Technology Stack

### 3.1 Backend
- **Python 3.11+**
- **FastAPI**: High-performance async web framework.
- **Uvicorn**: ASGI server.
- **Google Generative AI SDK**: For Gemini 2.0 Flash.

### 3.2 Frontend
- **React 18**: UI Library.
- **Vite**: Build tool.
- **Axios**: API Client.

### 3.3 Infrastructure
- **Google Cloud Run**: Serverless platform for stateless containers.
- **Docker**: Containerization for both frontend and backend.

---

## 4. Backend Implementation

### 4.1 Services
- **GeminiService** (`services/gemini_service.py`): Manages prompt engineering (`System Prompt` + `Conversation History`) and calls the Gemini API.
- **ElevenLabsService** (`services/elevenlabs_service.py`): Handles voice selection based on language and calls the Text-to-Speech API.

### 4.2 Configuration
Configuration is handled via Environment Variables (managed in Cloud Run revisions):
- `GOOGLE_API_KEY`
- `ELEVENLABS_API_KEY`
- `ALLOWED_ORIGINS`

---

## 10. Deployment

Deployment is managed via Google Cloud Run. See [DEPLOYMENT.md](DEPLOYMENT.md) for step-by-step instructions.

### Service Names
- **Backend**: `medivoice-api`
- **Frontend**: `medivoice-web`
