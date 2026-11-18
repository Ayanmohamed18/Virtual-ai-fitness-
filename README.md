# 🏋️ Forever Fit: The Future of AI Fitness

![Forever Fit Banner](https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=1470&auto=format&fit=crop)

> "Your Personal AI Trainer, Nutritionist, and Wellness Coach – All in One."

[![Conference Paper](https://img.shields.io/badge/IJERT_Publication-IJERTCONV14IS060098-blue?style=for-the-badge&logo=adobeacrobatreader)](https://www.ijert.org/research/IJERTCONV14IS060098.pdf)
[![Conference](https://img.shields.io/badge/Conference-ACSCON--2026-green?style=for-the-badge)](https://www.ijert.org/research/IJERTCONV14IS060098.pdf)
[![Institution](https://img.shields.io/badge/ACS_College_of_Engineering-Data_Science-orange?style=for-the-badge)](#)

**Forever Fit** is a comprehensive, AI-powered fitness and wellness ecosystem developed as a final-year Data Science project at **ACS College of Engineering, Bengaluru**. By leveraging computer vision, BiLSTM temporal sequence modeling, voice guidance, and generative AI, the platform delivers real-time exercise classification, posture correction, personalized nutrition and workout blueprints, and mental wellness support directly through a unified web interface.

---

## 📄 Research Publication & Documentation

This project was formally published and presented at **ACSCON-2026** (International Journal of Engineering Research & Technology - IJERT):

- **Paper Title:** *Virtual AI Fitness Coach for Exercise Classification and Form Correction*
- **Conference:** ACSCON-2026 (Paper ID: 423)
- **Published Paper (PDF):** [Read Full Research Paper on IJERT (`IJERTCONV14IS060098.pdf`)](https://www.ijert.org/research/IJERTCONV14IS060098.pdf)
- **Project Report (PDF):** [View Project Report (`docs/Forever_Fit_Project_Report.pdf`)](./docs/Forever_Fit_Project_Report.pdf) *(upload your report PDF to the `docs/` folder in your repository to activate this link)*

---

## 👨‍💻 Project Team & Supervision

Developed by a 4-member team from the Department of Computer Science & Engineering (Data Science), **ACS College of Engineering, Bengaluru**, under the supervision of **Dr. D. Gandhimathi**:

| Role | Name | USN / Designation | Email ID |
| :--- | :--- | :--- | :--- |
| **Team Lead** | **Ayan Mohamed** | `1AH22CD010` | `1AH22CD010@acsce.edu.in` |
| **Team Member** | **Duggeni Mahesh** | `1AH22CD018` | `1AH22CD018@acsce.edu.in` |
| **Team Member** | **Polisetti Aravind Kumar** | `1AH22CD038` | `1AH22CD038@acsce.edu.in` |
| **Team Member** | **Umesh Reddy C H** | `1AH22CD057` | `1AH22CD057@acsce.edu.in` |
| **Project Guide** | **Dr. D. Gandhimathi** | Associate Professor, Dept. of CSE – Data Science | `gandhimathid@acsce.edu.in` |

---

## 📸 Application Screenshots

### 1. System Dashboard & Real-Time Module Status
Displays live status indicators for **MediaPipe**, **Voice AI**, **Exercise AI**, and **DeepSeek R1**, alongside theme controls and exercise mode selection.

![System Dashboard](https://drive.google.com/uc?export=view&id=1sB29AdplGXpuGryAq2aqMW-TJomSlHfM)

### 2. Voice-Guided Exercise Trainer
Form-first training interface supporting exercise selection (e.g., Squat, Push-Up, Shoulder Press, Bicep Curl), camera feed toggles, rep counter resets, and real-time voice coaching powered by **ElevenLabs**.

> *Tip: Add your Google Drive direct link (`https://drive.google.com/uc?export=view&id=YOUR_FILE_ID`) or local path (`./screenshots/02_voice_trainer_setup.png`) here once uploaded.*

### 3. Live Computer Vision Pose Tracking & Form Correction
Real-time 33-point skeletal landmark overlay via **MediaPipe BlazePose** evaluating posture depth, form accuracy (`100%`), repetition count, and instant corrective prompts (*"Perfect depth! Explode up!"*).

![Live Pose Detection](https://drive.google.com/uc?export=view&id=1W5kqNrxiqx3Yf3PFyAhv6CqxUEmzpPXc)

### 4. Advanced Diet Planner
Generates personalized nutrition blueprints, daily caloric targets, and macro-nutrient distributions through a 15-question dietary, lifestyle, and budget assessment.

![Advanced Diet Planner](https://drive.google.com/uc?export=view&id=1ut8YU7oc-two6xKjNALpS0mRhC6RwNhM)

### 5. Mental Health Support Assistant
Dedicated wellness companion featuring quick-support modules (**Anxiety Help**, **Feeling Down**, **Motivation**, **Sleep Issues**) and empathetic AI chat.

![Mental Health Support Assistant](https://drive.google.com/uc?export=view&id=12tYtzZYfQzBFASTF1Ar3kyrNze_0qLfY)

### 6. Smart Workout Planner
Interactive 15-question onboarding flow that builds tailored 3-to-6-month training regimens aligned with user goals, schedules, available equipment, and fitness levels.

![Smart Workout Planner](https://drive.google.com/uc?export=view&id=1xNwpenk54CTCJ9tjC6UkF0hgIntWpnpz)

### 7. Personal Trainer AI Assistant
Fine-tuned **DeepSeek R1** conversational fitness coach with voice input and quick-start topics for **Workout Plans**, **Nutrition Guide**, **Muscle Building**, and **Weight Loss**.

![AI Personal Trainer](https://drive.google.com/uc?export=view&id=131ltED79XR6nnjSm5P8v48bkkQcbLj3E)

---

## 🚀 Why Forever Fit?

- **BiLSTM Temporal Classification (>96% Test Accuracy)**: Processes 30-frame sliding windows combining 3D BlazePose coordinates with 12 calculated joint angles to generalize across body types, lighting, and camera angles.
- **Form-First Real-Time Correction**: Repetitions are counted only when proper biomechanical form is maintained, preventing injury and maximizing training efficiency.
- **Multimodal Coaching**: Combines live skeleton overlays with **ElevenLabs** voice feedback and **DeepSeek R1** reasoning under 200 ms end-to-end latency.
- **Holistic Ecosystem**: Integrates physical training, 15-point personalized diet and workout assessments, and mental wellness support in a single application.

---

## ✨ Key Features

### 🤖 Voice-Guided AI Form Correction
Powered by **MediaPipe BlazePose**, a 2-layer **BiLSTM** network, and **ElevenLabs**, our computer vision pipeline tracks body landmarks in real time:
- **Instant Visual & Audio Cues**: Real-time posture status (`CORRECT FORM`), form score percentages, and spoken coaching prompts.
- **Precision Rep Counting**: Counts repetitions strictly upon meeting joint-angle depth and alignment thresholds across squats, push-ups, shoulder presses, and bicep curls.
- **Skeleton Overlay**: Live joint-and-limb tracking directly over the webcam feed.

### 🥗 Advanced Diet Planner & Nutrition AI
- **15-Question Scientific Assessment**: Tailors BMR/TDEE calorie and macro targets to your body metrics, dietary preferences, cooking skills, and budget.
- **Custom Meal Blueprints**: Actionable nutrition plans with downloadable PDF summaries built for long-term adherence.

### 🏋️ Smart Workout Planner
- **15-Question Foundational Profiling**: Designs structured weekly training splits based on 3–6 month outcomes, available equipment, and experience level.

### 🧠 Mental Health Support Assistant
- **Specialized Support Modes**: One-click prompts for anxiety relief, low mood, motivation, and sleep issues.
- **Safe Conversational Space**: Supportive, non-judgmental AI dialogue with crisis resource disclaimers.

### 💬 Personal Trainer AI Assistant
- **Voice & Text Interaction**: Ask fitness, nutrition, or recovery questions via text or voice input with quick-topic shortcuts.

---

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/) — Responsive dark/light theme UI with custom styling and interactive charts.
- **Computer Vision & Deep Learning**: [MediaPipe BlazePose](https://developers.google.com/mediapipe), OpenCV, and TensorFlow/Keras (BiLSTM) — Real-time pose estimation, joint-angle extraction, and exercise classification.
- **LLM & Reasoning Engine**: [DeepSeek R1](https://www.deepseek.com/) — Fine-tuned fitness, nutrition, and wellness intelligence.
- **Voice Synthesis**: [ElevenLabs API](https://elevenlabs.io/) — Real-time spoken exercise cues and feedback.
- **Backend & Database**: Python 3.10+ & [MongoDB Atlas](https://www.mongodb.com/) — Scalable user profiles, workout logs, and chat history storage.

---

## 🏁 Getting Started

### Prerequisites
- Python 3.10 or higher
- Webcam (for live pose detection and form correction)
- MongoDB connection URI, DeepSeek API key, and ElevenLabs API key

### Installation

1. **Clone the Repository**
   ```bash
   git clone [https://github.com/Ayanmohd18/Forever-fit.git](https://github.com/Ayanmohd18/Forever-fit.git)
   cd Forever-fit
   Install Dependencies

Bash
pip install -r requirements.txt
Set Up Environment Variables
Create a .env file in the root directory and configure your API keys:

Code snippet
MONGODB_CONNECTION_STRING=your_mongodb_connection_string
DEEPSEEK_API_KEY=your_deepseek_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
Run the Application

Bash
streamlit run main.py
📂 Repository Structure
Plaintext
Forever-fit/
├── docs/
│   └── Forever_Fit_Project_Report.pdf      # Project report PDF
├── screenshots/
│   └── 02_voice_trainer_setup.png          # Optional local backup screenshots
├── main.py
├── requirements.txt
├── .env
└── README.md
🤝 Contributing
Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request

📄 License
Distributed under the MIT License. See LICENSE for more information.

Made with ❤️ by Ayan Mohamed & Team | ACS College of Engineering, Bengaluru
