# MediVoice AI - Deployment Guide

## 🚀 Quick Deployment Options

This guide provides step-by-step instructions for deploying MediVoice AI to production.

---

## Option 1: Render (Recommended - Free Tier Available)

### Backend Deployment on Render

1. **Sign up at [Render](https://render.com)**

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `https://github.com/6736-shafi/MediVoice`

3. **Configure Service**
   ```
   Name: medivoice-backend
   Region: Choose closest to your users
   Branch: main
   Root Directory: (leave empty)
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
   ```

4. **Add Environment Variables**
   - Click "Environment" tab
   - Add the following:
   ```
   GOOGLE_API_KEY=your_google_gemini_api_key
   ELEVENLABS_API_KEY=your_elevenlabs_api_key
   ALLOWED_ORIGINS=https://your-frontend-url.vercel.app
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Copy your backend URL: `https://medivoice-backend.onrender.com`

### Frontend Deployment on Vercel

1. **Sign up at [Vercel](https://vercel.com)**

2. **Import Project**
   - Click "Add New" → "Project"
   - Import from GitHub: `https://github.com/6736-shafi/MediVoice`

3. **Configure Project**
   ```
   Framework Preset: Vite
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist
   Install Command: npm install
   ```

4. **Add Environment Variable**
   - Click "Environment Variables"
   - Add:
   ```
   VITE_BACKEND_URL=https://medivoice-backend.onrender.com
   ```

5. **Deploy**
   - Click "Deploy"
   - Wait for deployment (2-3 minutes)
   - Your app will be live at: `https://medivoice.vercel.app`

---

## Option 2: Railway (Easy Deployment)

### Backend on Railway

1. **Sign up at [Railway](https://railway.app)**

2. **New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `6736-shafi/MediVoice`

3. **Configure**
   - Railway auto-detects Python
   - Add environment variables:
   ```
   GOOGLE_API_KEY=your_key
   ELEVENLABS_API_KEY=your_key
   PORT=8000
   ```

4. **Deploy**
   - Railway automatically deploys
   - Get your URL from the deployment

### Frontend on Netlify

1. **Sign up at [Netlify](https://netlify.com)**

2. **Import Project**
   - "Add new site" → "Import an existing project"
   - Connect GitHub repository

3. **Build Settings**
   ```
   Base directory: frontend
   Build command: npm run build
   Publish directory: frontend/dist
   ```

4. **Environment Variables**
   ```
   VITE_BACKEND_URL=https://your-railway-backend.up.railway.app
   ```

5. **Deploy**

---

## Option 3: Google Cloud Platform (Production Grade)

### Backend on Cloud Run

1. **Install Google Cloud CLI**
   ```bash
   # Install gcloud CLI
   # https://cloud.google.com/sdk/docs/install
   ```

2. **Authenticate**
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

3. **Build and Deploy**
   ```bash
   cd /path/to/medivoice-ai
   
   # Build Docker image
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/medivoice-backend
   
   # Deploy to Cloud Run
   gcloud run deploy medivoice-backend \
     --image gcr.io/YOUR_PROJECT_ID/medivoice-backend \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars GOOGLE_API_KEY=your_key,ELEVENLABS_API_KEY=your_key
   ```

4. **Get Service URL**
   ```bash
   gcloud run services describe medivoice-backend --region us-central1
   ```

### Frontend on Firebase Hosting

1. **Install Firebase CLI**
   ```bash
   npm install -g firebase-tools
   ```

2. **Initialize Firebase**
   ```bash
   cd frontend
   firebase login
   firebase init hosting
   ```

3. **Configure**
   - Select your project
   - Public directory: `dist`
   - Single-page app: Yes
   - GitHub integration: Optional

4. **Build and Deploy**
   ```bash
   # Create .env.production
   echo "VITE_BACKEND_URL=https://your-cloud-run-url.run.app" > .env.production
   
   # Build
   npm run build
   
   # Deploy
   firebase deploy --only hosting
   ```

---

## Option 4: Docker Compose (Self-Hosted)

### Prerequisites
- Docker and Docker Compose installed
- VPS or server with public IP

### Create docker-compose.yml

```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - ELEVENLABS_API_KEY=${ELEVENLABS_API_KEY}
      - ALLOWED_ORIGINS=http://localhost:5173,https://yourdomain.com
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "80:80"
    environment:
      - VITE_BACKEND_URL=http://your-server-ip:8000
    depends_on:
      - backend
    restart: unless-stopped
```

### Deploy

```bash
# On your server
git clone https://github.com/6736-shafi/MediVoice.git
cd MediVoice

# Create .env file
cp .env.example .env
# Edit .env with your API keys

# Start services
docker-compose up -d

# Check logs
docker-compose logs -f
```

---

## Post-Deployment Checklist

### ✅ Backend Verification

1. **Health Check**
   ```bash
   curl https://your-backend-url.com/api/health
   ```
   
   Expected response:
   ```json
   {"status": "ok", "message": "MediVoice AI is running"}
   ```

2. **Test Conversation Endpoint**
   ```bash
   curl -X POST https://your-backend-url.com/api/conversation \
     -H "Content-Type: application/json" \
     -d '{
       "message": "I have a headache",
       "language": "en",
       "conversation_history": []
     }'
   ```

### ✅ Frontend Verification

1. **Open in Browser**
   - Navigate to your frontend URL
   - Check console for errors (F12)

2. **Test Features**
   - Select different languages
   - Start a voice call
   - Send a text message
   - Verify audio playback

### ✅ Integration Testing

1. **CORS Configuration**
   - Ensure backend `ALLOWED_ORIGINS` includes frontend URL
   - Check browser console for CORS errors

2. **API Keys**
   - Verify Gemini API key is working
   - Verify ElevenLabs API key is working
   - Check API usage/quotas

3. **Performance**
   - Test response times
   - Check audio quality
   - Verify voice synthesis in multiple languages

---

## Environment Variables Reference

### Backend (.env)

```bash
# Required
GOOGLE_API_KEY=your_google_gemini_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Optional
PORT=8000
ALLOWED_ORIGINS=https://your-frontend-url.com,https://www.your-frontend-url.com
```

### Frontend (.env.production)

```bash
VITE_BACKEND_URL=https://your-backend-url.com
```

---

## Troubleshooting

### Backend Issues

**Problem: API key errors**
```
Solution: Verify environment variables are set correctly in deployment platform
```

**Problem: CORS errors**
```
Solution: Add frontend URL to ALLOWED_ORIGINS environment variable
```

**Problem: 502 Bad Gateway**
```
Solution: Check if backend is running, verify PORT configuration
```

### Frontend Issues

**Problem: Cannot connect to backend**
```
Solution: Verify VITE_BACKEND_URL is set correctly
```

**Problem: Build fails**
```
Solution: Run 'npm install' and check for dependency issues
```

**Problem: Voice not working**
```
Solution: Ensure HTTPS is enabled (required for Web Speech API)
```

---

## Monitoring & Maintenance

### Logs

**Render:**
- Dashboard → Your Service → Logs

**Railway:**
- Project → Deployments → View Logs

**Vercel:**
- Project → Deployments → Function Logs

**Google Cloud:**
```bash
gcloud run services logs read medivoice-backend --region us-central1
```

### Scaling

**Render:**
- Free tier: Auto-sleeps after inactivity
- Paid tier: Always on, auto-scaling

**Railway:**
- Auto-scales based on traffic
- Configure in service settings

**Google Cloud Run:**
- Auto-scales 0 to N instances
- Configure max instances in deployment

---

## Cost Estimates

### Free Tier (Recommended for Testing)

| Service | Backend | Frontend | Total |
|---------|---------|----------|-------|
| Render + Vercel | Free | Free | **$0/month** |
| Railway + Netlify | Free | Free | **$0/month** |

**Limitations:**
- Backend sleeps after 15 min inactivity
- Limited build minutes
- Shared resources

### Production Tier

| Service | Backend | Frontend | Total |
|---------|---------|----------|-------|
| Render + Vercel | $7/mo | $20/mo | **$27/month** |
| Railway + Netlify | $5/mo | $19/mo | **$24/month** |
| GCP Cloud Run + Firebase | ~$10/mo | ~$5/mo | **~$15/month** |

**Plus API costs:**
- Google Gemini: Pay per request
- ElevenLabs: Pay per character

---

## Security Best Practices

1. **Never commit .env files**
   - Already in .gitignore
   - Use platform environment variables

2. **Use HTTPS in production**
   - All platforms provide free SSL
   - Required for Web Speech API

3. **Rotate API keys regularly**
   - Update in deployment platform
   - Redeploy services

4. **Monitor API usage**
   - Set up billing alerts
   - Monitor quotas

5. **Enable rate limiting**
   - Implement in backend if needed
   - Use platform features

---

## Next Steps

1. ✅ Choose deployment platform
2. ✅ Deploy backend
3. ✅ Deploy frontend
4. ✅ Configure environment variables
5. ✅ Test deployment
6. ✅ Set up custom domain (optional)
7. ✅ Enable monitoring
8. ✅ Share with users!

---

## Support

- **Documentation**: See README.md and TECHNICAL_DOCUMENTATION.md
- **Issues**: https://github.com/6736-shafi/MediVoice/issues
- **Deployment Help**: Check platform-specific documentation

---

**Happy Deploying! 🚀**
