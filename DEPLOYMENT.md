# Deploying Fitness AI Trainer for Free

## Recommended Platform: Streamlit Cloud
Streamlit Cloud is the best free option for deploying this application because:
- It supports `streamlit-webrtc` (needed for mobile camera).
- It handles Python dependencies automatically.
- It integrates directly with GitHub.
- It offers a generous free tier.

## Prerequisites
1. **GitHub Account**: You need to push your code to a GitHub repository.
2. **DeepSeek API Key**: You will need this for the AI features.

## User Requirements (Zero Installation)
**Great News:** Your users do NOT need to install MediaPipe, Python, or DeepSeek on their devices.
- **MediaPipe**: Runs entirely on the Streamlit Cloud server. The phone just streams video to it.
- **DeepSeek**: Accessed via API. The heavy AI processing happens on DeepSeek's servers.
- **User's Device**: Only needs a web browser (Chrome, Safari, etc.) and an internet connection.

## Step-by-Step Deployment Guide

### 1. Push Code to GitHub
Ensure all your files (including `requirements.txt` and `packages.txt`) are committed and pushed to a GitHub repository.
> [!NOTE]
> Make sure `packages.txt` is in the root of your repository. It installs system dependencies like `libgl1` which are required for OpenCV.

### 2. Connect to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io/).
2. Sign in with GitHub.
3. Click **"New app"**.
4. Select your repository (`Forever-fit`).
5. Set **Main file path** to `FOREVERFIT/main.py`.

### 3. Configure Secrets (Environment Variables)
Before deploying, click **"Advanced settings"** -> **"Secrets"**. Add your API keys here so they are secure:

```toml
DEEPSEEK_API_KEY = "sk-23c29d5634164a5aac1e95c729147194"
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
DEEPSEEK_MODEL = "deepseek-r1"
ELEVENLABS_API_KEY = "sk_11540ed8f87bd499b4f216ad860629c495cf18b0042b6ad8"
MONGODB_CONNECTION_STRING = "mongodb+srv://Ayan:Ayanmusfa786@aifitnesstrainer.sc0rgyu.mongodb.net/fitness_ai?retryWrites=true&w=majority&appName=Aifitnesstrainer&tls=true&tlsInsecure=true"
RAPIDAPI_KEY = "23a13b114dmsh97d7eb0f501d612p158e89jsn3aa4ce88aa5f"
YOUTUBE_API_KEY = "AIzaSyC7WFvFb8_gEcKIxYk6kAtp6INtqv7sYAQ"
MIXPANEL_PROJECT_TOKEN = "a57508529b4d2e9d38691e8d52ff23db"
MIXPANEL_API_SECRET = "200df8790b4f32f72efa7718c42912ae"
MIXPANEL_PROJECT_ID = "3934845"
HF_MODEL_REPO = "Ayanmohd1eight/foreverfit-deepseek-lora"
```

### 4. Deploy!
Click **"Deploy"**. Streamlit will install the dependencies from `requirements.txt` and `packages.txt`. This may take 5-10 minutes.

### 5. Mobile Access
Once deployed, you will get a URL (e.g., `https://forever-fit.streamlit.app`).
- Open this URL on your mobile phone.
- Select **"Live AI Trainer (Web/Mobile)"** mode.
- Grant camera permissions when asked.
- Start working out!

## Troubleshooting
- **Black Screen on Camera**: Ensure you are using `https://` (Streamlit Cloud does this automatically) and that you have granted camera permissions in the browser.
- **"Module not found"**: Check your `requirements.txt`.
- **"ImportError: libGL.so.1"**: This means `packages.txt` was not read. Ensure it is in the root directory.
