# MedAssist AI + n8n WhatsApp Bot Integration Guide

This guide shows you how to integrate your fine-tuned MedAssist AI model with n8n to create a comprehensive WhatsApp bot for healthcare assistance.

## 🏗️ Architecture Overview

```
WhatsApp Business API → n8n Workflow → MedAssist AI API → Fine-tuned DeepSeek-V3 Model
```

### Components:
1. **MedAssist AI API Server** - Flask server serving the fine-tuned model
2. **n8n Workflow** - Handles WhatsApp webhooks and message routing
3. **WhatsApp Business API** - Official WhatsApp messaging platform
4. **Fine-tuned DeepSeek-V3 Model** - Your MedAssist AI model

## 📋 Prerequisites

### 1. Fine-tuned MedAssist AI Model
- Complete the fine-tuning process using the scripts in the parent directory
- Ensure your model is saved in `./medassist_ai_model/`

### 2. WhatsApp Business API Setup
- Meta Developer Account
- WhatsApp Business API access
- Phone Number ID
- Access Token

### 3. n8n Installation
- n8n installed and running
- Webhook access configured

### 4. Python Environment
- Python 3.8+
- Required packages (see requirements.txt)

## 🚀 Step-by-Step Setup

### Step 1: Start the MedAssist AI API Server

```bash
cd finetune/n8n_integration

# Install additional requirements
pip install flask flask-cors

# Start the API server
python medassist_whatsapp_bot.py
```

The server will start on `http://localhost:5000` with these endpoints:
- `GET /health` - Health check
- `POST /chat` - Main chat endpoint
- `POST /webhook` - WhatsApp webhook endpoint
- `GET /session/<user_id>` - Get user session
- `DELETE /session/<user_id>` - Clear user session

### Step 2: Configure WhatsApp Business API

1. **Get Your Credentials:**
   - Phone Number ID: From Meta Developer Console
   - Access Token: From Meta Developer Console
   - Webhook Verify Token: Create a secure token

2. **Set Up Webhook:**
   - URL: `https://your-n8n-domain.com/webhook/medassist-webhook`
   - Verify Token: Your secure token
   - Subscribe to: `messages`, `message_deliveries`

### Step 3: Import n8n Workflow

1. **Open n8n:**
   - Go to your n8n instance
   - Click "Import from file"

2. **Import Workflow:**
   - Select `medassist_whatsapp_workflow.json`
   - Update the configuration

3. **Configure Credentials:**
   - Update `YOUR_PHONE_NUMBER_ID` with your actual Phone Number ID
   - Update `YOUR_ACCESS_TOKEN` with your actual Access Token
   - Update API URLs if needed

### Step 4: Test the Integration

1. **Test Health Check:**
```bash
curl http://localhost:5000/health
```

2. **Test Chat Endpoint:**
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hi", "user_id": "test_user"}'
```

3. **Test WhatsApp Integration:**
   - Send a message to your WhatsApp Business number
   - Check n8n execution logs
   - Verify response in WhatsApp

## 🔧 Configuration Details

### Environment Variables

```bash
# MedAssist AI API Server
export MEDASSIST_MODEL_PATH="./medassist_ai_model"
export PORT=5000

# WhatsApp Business API
export WHATSAPP_PHONE_NUMBER_ID="your_phone_number_id"
export WHATSAPP_ACCESS_TOKEN="your_access_token"
export WHATSAPP_WEBHOOK_VERIFY_TOKEN="your_webhook_verify_token"
```

### n8n Workflow Configuration

#### Webhook Node
- **Path:** `webhook`
- **HTTP Method:** `POST`
- **Response Mode:** `responseNode`

#### HTTP Request Nodes
- **MedAssist API:** `http://localhost:5000/chat`
- **WhatsApp API:** `https://graph.facebook.com/v17.0/{PHONE_NUMBER_ID}/messages`

#### Authentication
- **Type:** `Header Auth`
- **Name:** `Authorization`
- **Value:** `Bearer {YOUR_ACCESS_TOKEN}`

## 📱 WhatsApp Message Flow

### 1. User Sends Message
```
User → WhatsApp → Meta Webhook → n8n Webhook Node
```

### 2. Message Processing
```
n8n → Extract Message Data → Call MedAssist API → Generate Response
```

### 3. Response Delivery
```
n8n → Format Response → Send to WhatsApp → User Receives Response
```

## 🎯 Supported Message Types

### Text Messages
- Symptom descriptions
- Health questions
- Emergency requests
- General inquiries

### Voice Messages
- Automatic transcription
- Symptom analysis
- Confirmation flow

### Images
- Photo analysis prompts
- Web app redirection

### Documents
- Medical report handling
- Web app redirection

## 🔄 User Session Management

The bot maintains user sessions for:
- Onboarding progress
- Emergency mode status
- Conversation context
- Medication reminders

### Session Data Structure
```json
{
  "user_id": "1234567890",
  "onboarding_step": 1,
  "emergency_mode": false,
  "last_interaction": "2024-01-01T12:00:00Z",
  "preferences": {
    "language": "English",
    "location": "Mumbai"
  }
}
```

## 📊 Monitoring & Logging

### n8n Execution Logs
- Message processing status
- API call results
- Error handling
- Performance metrics

### MedAssist AI Logs
- Model inference logs
- Session management
- Error tracking
- Response generation

### WhatsApp Delivery Status
- Message delivery confirmations
- Read receipts
- Failed deliveries

## 🛠️ Advanced Features

### 1. Multi-language Support
```javascript
// In n8n Code Node
const userLanguage = detectLanguage(userMessage);
const localizedResponse = translateResponse(response, userLanguage);
```

### 2. Emergency Escalation
```javascript
// Emergency detection and escalation
if (isEmergency(userMessage)) {
  // Send immediate response
  // Notify healthcare providers
  // Log emergency details
}
```

### 3. Medication Reminders
```javascript
// Scheduled reminders
const reminders = getScheduledReminders();
for (const reminder of reminders) {
  sendWhatsAppMessage(reminder.user_id, reminder.message);
}
```

### 4. Analytics Integration
```javascript
// Track user interactions
const analytics = {
  user_id: user_id,
  message_type: input_type,
  response_time: responseTime,
  satisfaction_score: null
};
saveAnalytics(analytics);
```

## 🔒 Security Considerations

### 1. API Security
- Use HTTPS for all communications
- Implement rate limiting
- Validate webhook signatures
- Secure credential storage

### 2. Data Privacy
- Encrypt sensitive data
- Implement data retention policies
- Comply with healthcare regulations
- User consent management

### 3. Access Control
- Role-based access control
- API key management
- Audit logging
- Secure deployment

## 🚨 Error Handling

### Common Issues & Solutions

1. **Model Loading Errors**
   ```bash
   # Check model path
   ls -la ./medassist_ai_model/
   
   # Verify model files
   python -c "from transformers import AutoTokenizer; AutoTokenizer.from_pretrained('./medassist_ai_model')"
   ```

2. **WhatsApp API Errors**
   ```bash
   # Check credentials
   curl -H "Authorization: Bearer YOUR_TOKEN" \
        https://graph.facebook.com/v17.0/YOUR_PHONE_NUMBER_ID
   ```

3. **n8n Connection Issues**
   ```bash
   # Test API connectivity
   curl http://localhost:5000/health
   
   # Check n8n logs
   docker logs n8n-container
   ```

## 📈 Performance Optimization

### 1. Model Optimization
- Use model quantization
- Implement caching
- Batch processing
- GPU acceleration

### 2. API Optimization
- Response caching
- Connection pooling
- Load balancing
- CDN integration

### 3. n8n Optimization
- Workflow optimization
- Resource allocation
- Database indexing
- Monitoring setup

## 🔄 Deployment Options

### 1. Local Development
```bash
# Run locally for testing
python medassist_whatsapp_bot.py
n8n start
```

### 2. Docker Deployment
```dockerfile
# Dockerfile for MedAssist API
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "medassist_whatsapp_bot.py"]
```

### 3. Cloud Deployment
- **AWS:** ECS + API Gateway
- **Google Cloud:** Cloud Run + Cloud Functions
- **Azure:** Container Instances + Functions
- **Heroku:** Container deployment

## 📞 Support & Troubleshooting

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python medassist_whatsapp_bot.py
```

### Health Monitoring
```bash
# Check system health
curl http://localhost:5000/health

# Monitor n8n status
curl http://localhost:5678/healthz
```

### Common Commands
```bash
# Restart services
sudo systemctl restart n8n
sudo systemctl restart medassist-api

# Check logs
tail -f /var/log/n8n.log
tail -f /var/log/medassist-api.log

# Test endpoints
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "test", "user_id": "test"}'
```

## 🎉 Success Metrics

### Key Performance Indicators
- **Response Time:** < 2 seconds
- **Uptime:** > 99.9%
- **User Satisfaction:** > 4.5/5
- **Message Delivery Rate:** > 99%

### Business Metrics
- **Daily Active Users**
- **Conversation Completion Rate**
- **Emergency Detection Accuracy**
- **User Retention Rate**

---

## 🚀 Quick Start Checklist

- [ ] Fine-tune MedAssist AI model
- [ ] Start API server
- [ ] Configure WhatsApp Business API
- [ ] Import n8n workflow
- [ ] Test integration
- [ ] Monitor performance
- [ ] Deploy to production

**Your MedAssist AI WhatsApp bot is now ready to provide healthcare assistance to users worldwide! 🏥🤖** 