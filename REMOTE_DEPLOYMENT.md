# Remote AI Model Deployment Guide

This guide explains how to host the fine-tuned fitness model on a powerful machine (Host) and access it from other devices (Clients) running the Streamlit app.

## 🖥️ Server Setup (High-Performance Machine)

1.  **Prerequisites**: Ensure you have the fine-tuned model in `output/foreverfit_lora` and the GPU environment set up.
2.  **Find IP Address**: Open a terminal and run `ipconfig`. Note your IPv4 Address (e.g., `192.168.1.50`).
3.  **Start the API Server**:
    *   Double-click `run_api.bat`
    *   Wait until you see "Application startup complete" and "Uvicorn running on http://0.0.0.0:8000".

## 📱 Client Setup (Laptop / Streamlit App)

1.  **Install Application**: Copy the project files to your laptop or other device.
2.  **Configure Connection**:
    *   Open the `.env` file.
    *   Add or update the `REMOTE_LLM_URL` variable:
        ```ini
        REMOTE_LLM_URL=http://<SERVER_IP_ADDRESS>:8000
        # Example: REMOTE_LLM_URL=http://192.168.1.50:8000
        ```
3.  **Run the App**:
    *   Run `streamlit run main.py`.
    *   The app will detect the remote variable and connect to your server automatically.

## 🔍 Verification

1.  Check the Server terminal: You should see "Using Local Fine-Tuned Model" logs.
2.  Check the Client terminal: It will say "📡 Using Remote LLM API at ...".
