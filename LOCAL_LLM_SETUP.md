# ForeverFit AI - Local LLM Integration Guide

## Current Setup
Your fine-tuned DeepSeek model (DeepSeek-R1-Distill-Qwen-7B + LoRA) is configured but not running.

## Option 1: Run the Local API Server (Recommended for Production)

### Start the Server:
```powershell
# In a separate terminal/PowerShell window:
cd d:\Fitness-AI-Trainer-....V1\FOREVERFIT
.\venv_py310\Scripts\python.exe llm_api.py
```

This will:
- Load your fine-tuned model
- Start FastAPI server on http://localhost:8000
- Enable streaming responses
- Work with both chatbot.py and mental_health_chatbot.py

### Verify Server is Running:
```powershell
# Test health endpoint:
curl http://localhost:8000/health
```

## Option 2: Direct Local Model (For Development/Testing)

### Modify .env:
Remove or comment out the REMOTE_LLM_URL line:
```
# REMOTE_LLM_URL=http://localhost:8000
```

This will make the app load the model directly (slower startup, but no separate server needed).

## Current Status
- ✅ Fine-tuned model exists at: `./output/foreverfit_lora`
- ✅ Base model: `deepseek-ai/DeepSeek-R1-Distill-Qwen-7B`
- ⚠️  API Server: Not running (causing "Skipping local model load" message)
- ⚠️  Chatbots: Falling back to simple responses

## To Fix Now:
Run this command in a NEW terminal window (keep it open):
```powershell
cd d:\Fitness-AI-Trainer-....V1\FOREVERFIT
.\venv_py310\Scripts\python.exe llm_api.py
```

Then refresh your Streamlit app. The chatbots will now use your fine-tuned model!
