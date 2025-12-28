import { useState, useEffect, useRef } from 'react'
import { Mic, MicOff, Volume2, Globe, Heart, Activity, Phone, PhoneOff, FileDown } from 'lucide-react'
import { jsPDF } from "jspdf"
import ReactMarkdown from 'react-markdown'
import './App.css'

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'


// Language options
const LANGUAGES = [
  { code: 'en', name: 'English', flag: '🇺🇸' },
  { code: 'es', name: 'Spanish', flag: '🇪🇸' },
  { code: 'hi', name: 'Hindi', flag: '🇮🇳' },
  { code: 'ar', name: 'Arabic', flag: '🇸🇦' },
  { code: 'zh', name: 'Chinese', flag: '🇨🇳' },
  { code: 'fr', name: 'French', flag: '🇫🇷' },
  { code: 'de', name: 'German', flag: '🇩🇪' },
  { code: 'pt', name: 'Portuguese', flag: '🇧🇷' },
  { code: 'ru', name: 'Russian', flag: '🇷🇺' },
  { code: 'ja', name: 'Japanese', flag: '🇯🇵' }
]

function App() {
  const [selectedLanguage, setSelectedLanguage] = useState('en')
  const [isListening, setIsListening] = useState(false)
  const [isSpeaking, setIsSpeaking] = useState(false)
  const [conversation, setConversation] = useState([])
  // Use ref to track conversation state for event listeners
  const conversationRef = useRef([])
  
  // Sync ref with state
  useEffect(() => {
    conversationRef.current = conversation
  }, [conversation])

  const [status, setStatus] = useState('Ready to start')
  const [currentTranscript, setCurrentTranscript] = useState('')
  
  const recognitionRef = useRef(null)
  const audioRef = useRef(null)

  // Initialize Web Speech API
  useEffect(() => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
      recognitionRef.current = new SpeechRecognition()
      
      recognitionRef.current.continuous = true
      recognitionRef.current.interimResults = true
      
      // Language mapping for Web Speech API
      const languageCodes = {
        'en': 'en-US',
        'es': 'es-ES',
        'hi': 'hi-IN',
        'ar': 'ar-SA',
        'zh': 'zh-CN',
        'fr': 'fr-FR',
        'de': 'de-DE',
        'pt': 'pt-BR',
        'ru': 'ru-RU',
        'ja': 'ja-JP'
      }
      
      recognitionRef.current.lang = languageCodes[selectedLanguage] || 'en-US'
      
      recognitionRef.current.onresult = async (event) => {
        const lastResultIndex = event.results.length - 1
        const transcript = event.results[lastResultIndex][0].transcript
        
        setCurrentTranscript(transcript)
        
        // If final result, send to backend
        if (event.results[lastResultIndex].isFinal) {
          await handleUserSpeech(transcript)
          setCurrentTranscript('')
        }
      }
      
      recognitionRef.current.onerror = (event) => {
        console.error('Speech recognition error:', event.error)
        setStatus(`Error: ${event.error}`)
      }
      
      recognitionRef.current.onend = () => {
        if (isListening) {
          // Restart if still supposed to be listening
          recognitionRef.current.start()
        }
      }
    } else {
      setStatus('Speech recognition not supported in this browser')
    }
  }, [selectedLanguage]) // Only depend on language

  // Handle user speech
  const handleUserSpeech = async (transcript) => {
    if (!transcript.trim()) return

    // Create updated conversation history immediately to avoid stale state
    const newMessage = { role: 'user', content: transcript }
    // USE REF TO GET LATEST STATE
    const currentHistory = conversationRef.current
    const updatedHistory = [...currentHistory, newMessage]
    
    // Add user message to conversation state
    setConversation(prev => [...prev, newMessage])

    setStatus('AI is thinking...')

    try {
      // Send to backend
      const response = await fetch(`${BACKEND_URL}/api/conversation`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: transcript,
          language: selectedLanguage,
          conversation_history: updatedHistory // Send immediate history from REF
        })
      })

      const data = await response.json()
      
      // Add AI response to conversation
      setConversation(prev => [...prev, {
        role: 'assistant',
        content: data.text_response
      }])

      // Play audio response
      if (data.audio_url) {
        setStatus('AI is speaking...')
        await playAudio(data.audio_url)
      }

      // Check for emergency
      if (data.medical_context?.is_emergency) {
        alert('⚠️ EMERGENCY DETECTED: Please seek immediate medical attention or call emergency services!')
      }

      setStatus('Listening...')

    } catch (error) {
      console.error('Error:', error)
      setStatus('Error occurred')
      setConversation(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.'
      }])
    }
  }

  // Sync isListening ref with state
  const isListeningRef = useRef(false)
  useEffect(() => {
    isListeningRef.current = isListening
  }, [isListening])

  // Play audio
  const playAudio = (audioUrl) => {
    return new Promise((resolve) => {
      if (audioRef.current) {
        // IMPORTANT: Stop speech recognition to prevent feedback loop
        if (recognitionRef.current && isListeningRef.current) {
          recognitionRef.current.stop()
        }
        
        setIsSpeaking(true)
        audioRef.current.src = audioUrl
        audioRef.current.onended = () => {
          setIsSpeaking(false)
          
          // Resume speech recognition after AI finishes speaking
          // Use REF to check true state
          if (recognitionRef.current && isListeningRef.current) {
            try {
              recognitionRef.current.start()
            } catch (e) {
              console.log('Recognition already started')
            }
          }
          
          resolve()
        }
        audioRef.current.play()
      } else {
        resolve()
      }
    })
  }

  // Start listening
  const startListening = () => {
    if (recognitionRef.current) {
      setIsListening(true)
      setStatus('Listening...')
      recognitionRef.current.start()
    }
  }

  // Stop listening
  const stopListening = () => {
    if (recognitionRef.current) {
      setIsListening(false)
      setStatus('Ready to start')
      recognitionRef.current.stop()
    }
  }

  const generateReport = async () => {
    if (conversation.length === 0) return
    setStatus('Generating Report...')
    try {
      const response = await fetch(`${BACKEND_URL}/api/report`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ conversation_history: conversation, language: selectedLanguage })
      })
      const data = await response.json()
      let reportData = {}
      try {
          reportData = JSON.parse(data.report)
      } catch (e) {
          console.error("Failed to parse report JSON", e)
          reportData = { diagnosis: "Error parsing report", patient_symptoms: "N/A" }
      }

      const doc = new jsPDF()
      doc.setFontSize(22)
      doc.setTextColor(0, 102, 204)
      doc.text("MediVoice AI - Medical Report", 20, 20)
      doc.setFontSize(10)
      doc.setTextColor(100)
      doc.text(`Generated on: ${new Date().toLocaleString()}`, 20, 30)

      let y = 45
      const addSection = (title, content) => {
          if (!content) return
          doc.setFontSize(14)
          doc.setTextColor(0, 51, 102)
          doc.text(title, 20, y)
          y += 8
          doc.setFontSize(11)
          doc.setTextColor(0)
          const lines = doc.splitTextToSize(content, 170)
          doc.text(lines, 20, y)
          y += (lines.length * 6) + 10
          if (y > 270) { doc.addPage(); y = 20; }
      }

      addSection("Patient Symptoms", reportData.patient_symptoms)
      addSection("Diagnosis", reportData.diagnosis)
      
      doc.setFontSize(14)
      doc.setTextColor(0, 51, 102)
      doc.text("Medications", 20, y)
      y += 8
      doc.setFontSize(11)
      doc.setTextColor(0)
      if (Array.isArray(reportData.medications)) {
          reportData.medications.forEach(m => {
              doc.text(`• ${m}`, 25, y)
              y += 6
          })
      } else {
          doc.text(reportData.medications || "None", 25, y)
      }
      y += 10
      
      addSection("Lifestyle & Diet", reportData.lifestyle_advice)
      addSection("Precautions", reportData.precautions)
      addSection("Follow Up", reportData.follow_up)

      doc.save("MediVoice_Report.pdf")
      setStatus('Report Downloaded')
    } catch (error) {
      console.error(error)
      setStatus('Report Gen Error')
    }
  }

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <Heart className="logo-icon" />
            <h1>MediVoice AI</h1>
          </div>
          <p className="tagline">Real-Time Voice Medical Assistant</p>
        </div>
      </header>

      {/* Main Container */}
      <div className="container">
        {/* Language Selector */}
        <div className="language-selector">
          <Globe className="icon" />
          <select 
            value={selectedLanguage} 
            onChange={(e) => setSelectedLanguage(e.target.value)}
            className="language-select"
            disabled={isListening}
          >
            {LANGUAGES.map(lang => (
              <option key={lang.code} value={lang.code}>
                {lang.flag} {lang.name}
              </option>
            ))}
          </select>
        </div>

        {/* Status Display */}
        <div className={`status-bar ${isListening ? 'connected' : ''}`}>
          <Activity className={`status-icon ${isListening ? 'pulse' : ''}`} />
          <span>{status}</span>
        </div>

        {/* Current Transcript */}
        {currentTranscript && (
          <div className="current-transcript">
            <p>🎤 {currentTranscript}</p>
          </div>
        )}

        {/* Conversation Area */}
        <div className="conversation-container">
          {conversation.length === 0 ? (
            <div className="welcome-message">
              <Phone className="welcome-icon" />
              <h2>Voice Medical Consultation</h2>
              <p>Click "Start Call" to begin speaking with your AI medical assistant</p>
              <div className="features">
                <div className="feature">
                  <Globe /> <span>10+ Languages</span>
                </div>
                <div className="feature">
                  <Volume2 /> <span>Real-Time Voice</span>
                </div>
                <div className="feature">
                  <Heart /> <span>24/7 Available</span>
                </div>
              </div>
            </div>
          ) : (
            <div className="messages">
              {conversation.map((msg, index) => (
                <div key={index} className={`message ${msg.role}`}>
                  <div className="message-content">
                    <ReactMarkdown>{msg.content}</ReactMarkdown>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Voice Visualizer */}
        {isListening && (
          <div className="voice-visualizer-container">
            <div className={`voice-visualizer ${isSpeaking ? 'speaking' : 'listening'}`}>
              <div className="wave"></div>
              <div className="wave"></div>
              <div className="wave"></div>
              <div className="wave"></div>
              <div className="wave"></div>
            </div>
            <p className="voice-status">
              {isSpeaking ? '🔊 AI is speaking...' : '🎤 Listening...'}
            </p>
          </div>
        )}

        {/* Text Input Fallback (for testing) */}
        {isListening && (
          <div className="input-container">
            <input
              type="text"
              placeholder="Or type your message here for testing..."
              className="text-input"
              onKeyPress={(e) => {
                if (e.key === 'Enter' && e.target.value.trim()) {
                  handleUserSpeech(e.target.value)
                  e.target.value = ''
                }
              }}
            />
            <button
              className="send-button"
              onClick={(e) => {
                const input = e.target.previousSibling
                if (input.value.trim()) {
                  handleUserSpeech(input.value)
                  input.value = ''
                }
              }}
            >
              Send
            </button>
          </div>
        )}

        {/* Call Control */}
        <div className="call-control">
          {!isListening ? (
            <button 
              className="call-button start"
              onClick={startListening}
            >
              <Phone />
              <span>Start Call</span>
            </button>
          ) : (
            <button 
              className="call-button end"
              onClick={stopListening}
            >
              <PhoneOff />
              <span>End Call</span>
            </button>
          )}
        </div>

        {/* Report Download */}
        {conversation.length > 0 && (
          <div className="report-action">
            <button 
              className="download-button"
              onClick={generateReport}
            >
              <FileDown className="icon-sm" />
              <span>Download Medical Report</span>
            </button>
          </div>
        )}

        {/* Disclaimer */}
        <div className="disclaimer">
          <p>⚠️ This is an AI assistant for informational purposes only. Always consult a healthcare professional for medical advice.</p>
        </div>
      </div>

      {/* Hidden audio element */}
      <audio 
        ref={audioRef}
        style={{ display: 'none' }}
      />
    </div>
  )
}

export default App
