# MediVoice AI - Deployment Guide

This guide details the deployment of MediVoice AI to **Google Cloud Run**. 
We separate the application into two services:
1. **`medivoice-api`**: The Python FastAPI Backend.
2. **`medivoice-web`**: The React Frontend (served via Nginx or a lightweight Node server).

## Current Production Deployment

**Project ID**: `root-furnace-428717-f6`  
**Region**: `us-central1`

**Services**:
- **Backend**: `medivoice-api`
  - URL: https://medivoice-api-409417803362.us-central1.run.app/
  - Latest Revision: medivoice-api-00011-rnv
  
- **Frontend**: `medivoice-web`  
  - URL: https://medivoice-web-409417803362.us-central1.run.app/
  - Latest Revision: medivoice-web-00001-tz5

---

## Prerequisites

1. **Google Cloud SDK** installed and authenticated.
2. **Docker** installed (optional, but recommended for local testing).
3. **API Keys** for Google Gemini and ElevenLabs.

---

## 1. Setup Google Cloud Project

```bash
# Login to Google Cloud
gcloud auth login

# Set your project ID
gcloud config set project YOUR_PROJECT_ID

# Enable necessary services
gcloud services enable run.googleapis.com \
    cloudbuild.googleapis.com \
    artifactregistry.googleapis.com
```

---

## 2. Deploy Backend (`medivoice-api`)

The backend hosts the API logic, AI integration, and voice synthesis.

### Configure & Deploy

1. Navigate to the project root:
   ```bash
   cd medivoice-ai
   ```

2. Deploy using `gcloud run`:
   ```bash
   gcloud run deploy medivoice-api \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars GOOGLE_API_KEY=your_gemini_key \
     --set-env-vars ELEVENLABS_API_KEY=your_elevenlabs_key \
     --set-env-vars ALLOWED_ORIGINS="*"
   ```
   
   *Note: In production, replace `ALLOWED_ORIGINS="*"` with your actual frontend URL once deployed.*

3. **Save the Backend URL**: 
   Output will look like: `https://medivoice-api-xyz123-uc.a.run.app`
   You will need this for the frontend deployment.

---

## 3. Deploy Frontend (`medivoice-web`)

The frontend is a React application that needs to know where the backend is located.

### Configure & Deploy

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Create/Update `.env.production`:
   ```bash
   # Replace with the URL from Step 2
   echo "VITE_BACKEND_URL=https://medivoice-api-xyz123-uc.a.run.app" > .env.production
   ```

3. Deploy using `gcloud run`:
   ```bash
   gcloud run deploy medivoice-web \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

4. **Access the Application**:
   Output will look like: `https://medivoice-web-xyz123-uc.a.run.app`
   Open this URL in your browser.

---

## 4. Post-Deployment Verification

1. **Visit the Frontend URL**: Ensure the UI loads.
2. **Check Connectivity**: 
   - Open Developer Tools (F12) -> Network Tab.
   - Send a message.
   - Verify requests are going to `https://medivoice-api-...` and returning `200 OK`.
3. **CORS Update** (Recommended):
   - Once you have the final `medivoice-web` URL, update the backend's `ALLOWED_ORIGINS`.
   ```bash
   gcloud run services update medivoice-api \
     --update-env-vars ALLOWED_ORIGINS="https://medivoice-web-xyz123-uc.a.run.app"
   ```

---

## Troubleshooting

### "Connection Refused" or Network Errors
- Ensure `VITE_BACKEND_URL` in `frontend/.env.production` **does not** have a trailing slash (unless your code handles it) and starts with `https://`.
- Check if the backend service is running and healthy in the Google Cloud Console.

### 500 Internal Server Error
- Check Backend Logs:
  ```bash
  gcloud run services logs read medivoice-api
  ```
- Verify API Keys are correct in the Backend Environment variables.

### CORS Errors
- Ensure the backend's `ALLOWED_ORIGINS` includes the frontend's origin (protocol + domain).
