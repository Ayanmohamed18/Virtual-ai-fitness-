import cv2
import av
import streamlit as st
from streamlit_webrtc import VideoProcessorBase, webrtc_streamer, WebRtcMode, RTCConfiguration

try:
    from ExerciseAiTrainer import Exercise
except ImportError:
    Exercise = None

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

class ExerciseProcessor(VideoProcessorBase):
    def __init__(self):
        self.trainer = None
        # Initialize trainer lazily to avoid loading heavy models unnecessarily
        
    def recv(self, frame):
        if self.trainer is None:
             if Exercise:
                self.trainer = Exercise()
        
        img = frame.to_ndarray(format="bgr24")
        
        if self.trainer:
            # Process the frame using the refactored method
            img = self.trainer.process_frame(img)
            
        return av.VideoFrame.from_ndarray(img, format="bgr24")

def webrtc_exercise_ui():
    """
    Renders the WebRTC component for exercise tracking.
    """
    if Exercise is None:
        st.error("Exercise module not loaded completely.")
        return

    st.markdown("### 📷 Cloud/Mobile Camera")
    st.info("Ensure you grant camera permissions in your browser.")

    webrtc_ctx = webrtc_streamer(
        key="exercise-trainer",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIGURATION,
        video_processor_factory=ExerciseProcessor,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )
    
    if webrtc_ctx.state.playing:
        st.caption("AI processing active... Perform exercises to see counters.")
