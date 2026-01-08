# 🚀 Quick Start Guide for Users

## Setup (One-Time)

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/Forever-fit.git
cd Forever-fit/FOREVERFIT
```

### 2. Install Dependencies
```bash
# Create virtual environment
python -m venv venv_py310

# Activate it
# Windows:
venv_py310\Scripts\activate
# Mac/Linux:
source venv_py310/bin/activate

# Install packages
pip install -r requirements.txt
```

### 3. Setup Environment Variables
Create a `.env` file:
```env
# Option A: Use Fine-Tuned Model (Requires GPU)
HF_MODEL_REPO=YOUR_USERNAME/foreverfit-deepseek-lora
# Model will auto-download on first run!

# Option B: Use DeepSeek Cloud API (No GPU needed)
DEEPSEEK_API_KEY=your_api_key_here
# Get free key at: https://platform.deepseek.com/

# Other APIs (Optional)
ELEVENLABS_API_KEY=your_key_here
MONGODB_URI=your_mongodb_uri
```

### 4. Run the Application

#### Option A: With Fine-Tuned Model (GPU Required)
```bash
# Start LLM server (in separate terminal)
python llm_api.py
# Wait for "✅ Local LLM loaded successfully!"

# Start Streamlit app (in another terminal)
streamlit run main.py
```

#### Option B: Without GPU (Cloud API)
```bash
# Just run Streamlit (uses DeepSeek API)
streamlit run main.py
```

## 🎯 Features
- **AI Chatbot**: Fitness and nutrition advice
- **Voice Trainer**: Real-time form correction with voice feedback
- **Workout Planner**: Personalized workout plans
- **Diet Planner**: Custom meal plans
- **Mental Health Support**: Wellness coaching
- **Progress Tracking**: Track your fitness journey

## 📋 Requirements

### Minimum (Cloud API Mode):
- Python 3.10+
- 4GB RAM
- Internet connection

### Recommended (Local Model Mode):
- Python 3.10+
- NVIDIA GPU with 8GB+ VRAM
- 16GB RAM
- CUDA 11.8+

## 🆘 Troubleshooting

### Model Not Downloading?
```bash
# Install Hugging Face Hub
pip install huggingface_hub

# Manually download
python -c "
from huggingface_hub import snapshot_download
snapshot_download('YOUR_USERNAME/foreverfit-deepseek-lora', local_dir='./output/foreverfit_lora')
"
```

### No GPU?
Use DeepSeek API instead! Just set `DEEPSEEK_API_KEY` in `.env` and skip the LLM server.

### Port Already in Use?
```bash
# Change port in command
streamlit run main.py --server.port 8502
```

## 📞 Support
- Issues: [GitHub Issues](https://github.com/YOUR_USERNAME/Forever-fit/issues)
- Docs: See `DEPLOYMENT_OPTIONS.md` for advanced setup

---

**Enjoy your AI Fitness Trainer!** 💪
