# 🚀 ForeverFit AI - Setup Guide for Users

## ✅ Your Fine-Tuned Model is LIVE!

Model URL: **https://huggingface.co/Ayanmohd1eight/foreverfit-deepseek-lora**

---

## 📦 Quick Setup (5 Minutes)

### 1. Clone the Repository
```bash
git clone https://github.com/Ayanmohd18/Forever-fit.git
cd Forever-fit/FOREVERFIT
```

### 2. Install Dependencies
```bash
# Create virtual environment
python -m venv venv_py310

# Activate (Windows)
venv_py310\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 3. Setup Environment Variables
```bash
# Copy template
copy .env.example .env

# Edit .env file with your API keys
# Minimum required: DEEPSEEK_API_KEY
```

### 4. Run the App

#### Option A: With Fine-Tuned Model (GPU Required)
```bash
# Terminal 1: Start LLM Server
python llm_api.py
# Model auto-downloads from Hugging Face on first run!
# Wait for: "✅ Local LLM loaded successfully!"

# Terminal 2: Start Streamlit
streamlit run main.py
```

#### Option B: Without GPU (Cloud API)
```bash
# Just run Streamlit (uses DeepSeek cloud API)
streamlit run main.py
```

---

## 🎯 What You Get

- **AI Fitness Chatbot** - Expert training & nutrition advice
- **Voice Trainer** - Real-time form correction with voice feedback
- **Workout Planner** - Personalized workout plans
- **Diet Planner** - Custom meal plans
- **Mental Health Support** - Wellness coaching
- **Progress Tracking** - Track your fitness journey

---

## 💻 System Requirements

### Minimum (Cloud API Mode):
- Python 3.10+
- 4GB RAM
- Internet connection
- DeepSeek API key (free tier available)

### Recommended (Local Model Mode):
- Python 3.10+
- NVIDIA GPU with 8GB+ VRAM
- 16GB RAM
- CUDA 11.8+

---

## 🔑 Getting API Keys

### DeepSeek API (Required)
1. Go to: https://platform.deepseek.com/
2. Sign up (free tier available)
3. Get API key
4. Add to `.env`: `DEEPSEEK_API_KEY=your_key_here`

### ElevenLabs (Optional - for voice feedback)
1. Go to: https://elevenlabs.io/
2. Sign up
3. Get API key
4. Add to `.env`: `ELEVENLABS_API_KEY=your_key_here`

---

## 🆘 Troubleshooting

### Model Not Downloading?
The model auto-downloads from Hugging Face on first run. If it fails:
```bash
# Manual download
pip install huggingface_hub
python -c "from huggingface_hub import snapshot_download; snapshot_download('Ayanmohd1eight/foreverfit-deepseek-lora', local_dir='./output/foreverfit_lora')"
```

### No GPU?
**No problem!** Just use DeepSeek cloud API:
1. Comment out `REMOTE_LLM_URL` in `.env`
2. Make sure `DEEPSEEK_API_KEY` is set
3. Run: `streamlit run main.py`

### Port Already in Use?
```bash
streamlit run main.py --server.port 8502
```

### Import Errors?
```bash
pip install -r requirements.txt --upgrade
```

---

## 📚 Documentation

- **Deployment Guide**: See `DEPLOYMENT_SUMMARY.md`
- **Hugging Face Steps**: See `HUGGINGFACE_DEPLOYMENT_STEPS.md`
- **Quick Start**: See `QUICKSTART.md`

---

## 🌟 Features

### AI Chatbot
- Fine-tuned on fitness & nutrition data
- Expert-level responses (250-500 words)
- Personalized advice
- Natural conversation flow

### Voice Trainer
- Real-time pose detection
- Form correction with voice feedback
- Rep counting (100% accuracy)
- Supports: Bicep Curl, Push-up, Pull-up, Shoulder Press

### Workout & Diet Planning
- Personalized plans based on goals
- Progress tracking
- Meal suggestions
- Exercise library

---

## 🤝 Support

- **Issues**: [GitHub Issues](https://github.com/Ayanmohd18/Forever-fit/issues)
- **Model**: [Hugging Face](https://huggingface.co/Ayanmohd1eight/foreverfit-deepseek-lora)

---

## 📄 License

MIT License - See LICENSE file

---

**Enjoy your AI Fitness Trainer!** 💪

Made with ❤️ by Ayan Mohamed
