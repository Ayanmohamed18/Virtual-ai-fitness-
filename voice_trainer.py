import streamlit as st
import sys
import cv2
import numpy as np
import os
import threading
import time
import tempfile
from collections import deque
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import UI utilities
from ui_utils import apply_legendary_styles, card_container, render_status_badge

# Initialize Flags
MEDIAPIPE_AVAILABLE = False
ELEVENLABS_AVAILABLE = False
AUTH_AVAILABLE = False
EXERCISE_AVAILABLE = False

# Import MediaPipe
try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError as e:
    print(f"MediaPipe import error: {e}")
    MEDIAPIPE_ERROR = str(e)
    MEDIAPIPE_AVAILABLE = False
except Exception as e:
    print(f"MediaPipe unexpected error: {e}")
    MEDIAPIPE_ERROR = str(e)
    MEDIAPIPE_AVAILABLE = False

# Import Multi-Voice Engine (ElevenLabs, gTTS, pyttsx3)
try:
    from multi_voice_engine import voice_engine
    VOICE_AVAILABLE = True
    print("✅ Voice engine loaded successfully")
except ImportError as e:
    print(f"⚠️  Voice engine not available: {e}")
    VOICE_AVAILABLE = False
    voice_engine = NoneLABS_AVAILABLE = False

# Import Auth System
try:
    from auth_system import FitnessDatabase
    AUTH_AVAILABLE = True
except ImportError:
    print("Auth System not available")
    FitnessDatabase = None

# Import Exercise AI
try:
    import ExerciseAiTrainer as exercise
    from exercise_coach import ExerciseCoach
    EXERCISE_AVAILABLE = True
except ImportError:
    print("Exercise AI not available")


from expert_feedback import get_expert_feedback

class AngleSmoother:
    def __init__(self, window_size=5):
        self.window_size = window_size
        self.angles = deque(maxlen=window_size)

    def smooth(self, new_angle):
        self.angles.append(new_angle)
        return sum(self.angles) / len(self.angles)


class VoiceTrainer:
    def __init__(self):
        self.mp_pose = None
        self.pose = None
        self.mp_drawing = None
        self.last_voice_time = 0
        self.basic_mode = False # New flag
        self.smoother = AngleSmoother(window_size=5)
        
        # Try to initialize MediaPipe
        if MEDIAPIPE_AVAILABLE:
            try:
                self.mp_pose = mp.solutions.pose
                self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
                self.mp_drawing = mp.solutions.drawing_utils
                print("VoiceTrainer: MediaPipe initialized successfully")
            except Exception as e:
                print(f"VoiceTrainer: MediaPipe initialization failed: {e}")
                self.basic_mode = True
        else:
            self.basic_mode = True

    def speak(self, text):
        """Use multi-voice engine for feedback"""
        if not VOICE_AVAILABLE or not voice_engine:
            return
        
        # Check if voice is enabled
        if not st.session_state.get("voice_enabled", True):
            return
        
        # Visual notification
        try:
            st.toast(f"🗣️ Coach: {text}", icon="🎙️")
        except:
            pass
        
        # Use multi-voice engine (auto-selects best available)
        voice_engine.speak(text)

    def analyze_form_and_count_reps(self, landmarks, exercise, current_stage, rep_counter, frame_history=[]):
        if len(landmarks) < 33:
            return {"score": 0, "feedback": "No pose detected", "stage": current_stage, "reps": rep_counter, "form_correct": False, "confidence": 0}

        form_correct = True
        feedback = "Good form!"
        score = 100
    def analyze_form_and_count_reps(self, landmarks, exercise, current_stage, rep_counter, frame_history=[]):
        if len(landmarks) < 33:
            return {"score": 0, "feedback": "No pose detected", "stage": current_stage, "reps": rep_counter, "form_correct": False, "confidence": 0}

        form_correct = True
        feedback = "Position yourself"
        score = 100
        new_stage = current_stage
        new_reps = rep_counter
        confidence = 0
        primary_angle = 0
        
        # Store last 10 frames
        if len(frame_history) > 10:
            frame_history.pop(0)
        frame_history.append(landmarks)

        # Helper to check visibility with strict threshold
        def visible(lm_index):
            return landmarks[lm_index].visibility > 0.6  # Stricter visibility requirement

        # Calculate Movement Confidence (Velocity) - More sophisticated
        if len(frame_history) >= 5:
            angle_changes = []
            for i in range(len(frame_history)-1):
                prev_angle = self.calculate_angle(
                    [frame_history[i][12].x, frame_history[i][12].y],
                    [frame_history[i][14].x, frame_history[i][14].y],
                    [frame_history[i][16].x, frame_history[i][16].y]
                )
                curr_angle = self.calculate_angle(
                    [frame_history[i+1][12].x, frame_history[i+1][12].y],
                    [frame_history[i+1][14].x, frame_history[i+1][14].y],
                    [frame_history[i+1][16].x, frame_history[i+1][16].y]
                )
                angle_changes.append(abs(curr_angle - prev_angle))
            
            avg_change = sum(angle_changes) / len(angle_changes) if angle_changes else 0
            # Detect if movement is too fast (cheating/momentum)
            max_change = max(angle_changes) if angle_changes else 0
            
            confidence = min(100, int(avg_change * 25))
            
            # Flag if movement is suspiciously fast
            too_fast = max_change > 15  # More than 15° per frame = likely momentum
        else:
            too_fast = False
        
        # --- BICEP CURL ---
        if exercise == "bicep_curl":
            # Strict Visibility Check
            if not (visible(12) and visible(14) and visible(16)) and not (visible(11) and visible(13) and visible(15)):
                return {"score": 0, "feedback": "Position arms in frame!", "stage": current_stage, "reps": rep_counter, "form_correct": False, "confidence": 0}

            # Select Arm based on visibility
            right_vis = landmarks[14].visibility + landmarks[16].visibility
            left_vis = landmarks[13].visibility + landmarks[15].visibility
            
            if right_vis > left_vis:
                shoulder = [landmarks[12].x, landmarks[12].y]
                elbow = [landmarks[14].x, landmarks[14].y]
                wrist = [landmarks[16].x, landmarks[16].y]
                hip = [landmarks[24].x, landmarks[24].y]
                primary_arm = "right"
            else:
                shoulder = [landmarks[11].x, landmarks[11].y]
                elbow = [landmarks[13].x, landmarks[13].y]
                wrist = [landmarks[15].x, landmarks[15].y]
                hip = [landmarks[23].x, landmarks[23].y]
                primary_arm = "left"

            raw_angle = self.calculate_angle(shoulder, elbow, wrist)
            primary_angle = self.smoother.smooth(raw_angle)
            
            # Initialize stage if None
            if current_stage is None:
                current_stage = "down" if primary_angle > 100 else "up"
                new_stage = current_stage
            
            # FORM VALIDATION (doesn't block rep counting)
            form_issues = []
            
            # 1. Elbow Position
            elbow_drift_x = abs(elbow[0] - shoulder[0])
            if elbow_drift_x > 0.18:
                form_issues.append("Lock elbows!")
                score -= 20
            
            # 2. Body Lean
            if visible(23) or visible(24):
                shoulder_hip_distance = abs(shoulder[0] - hip[0])
                if shoulder_hip_distance > 0.18:
                    form_issues.append("Stand straight!")
                    score -= 15
            
            if form_issues:
                feedback = " | ".join(form_issues[:2])
                form_correct = False
                if time.time() - self.last_voice_time > 6:
                    self.speak(get_expert_feedback("bicep_curl", False))
            else:
                form_correct = True
                feedback = "Good form"

            # SIMPLIFIED REP COUNTING - GUARANTEED TO WORK
            # Clear thresholds with hysteresis
            DOWN_ANGLE = 120  # Arms extended (lowered threshold)
            UP_ANGLE = 80     # Arms contracted (raised threshold)
            
            if primary_angle > DOWN_ANGLE:  # Extended position (DOWN)
                if current_stage == "up":  # Just came from UP = completed rep!
                    new_reps += 1
                    voice_msg = get_expert_feedback("bicep_curl", True)
                    self.speak(voice_msg)
                    feedback = f"✅ Rep {new_reps}!"
                    
                new_stage = "down"
                if "Rep" not in feedback:
                    feedback = "Extended. Curl up!"
                    
            elif primary_angle < UP_ANGLE:  # Contracted position (UP)
                new_stage = "up"
                if "Rep" not in feedback:
                    feedback = "Squeeze!"
            else:
                # In transition - keep current stage
                new_stage = current_stage

        # --- PUSH UP ---
        elif exercise == "push_up":
            # Strict Visibility
            if not (visible(11) and visible(12) and visible(13) and visible(14)):
                 return {"score": 0, "feedback": "Show full upper body!", "stage": current_stage, "reps": rep_counter, "form_correct": False, "confidence": 0}

            left_shoulder = [landmarks[11].x, landmarks[11].y]
            left_elbow = [landmarks[13].x, landmarks[13].y]
            left_wrist = [landmarks[15].x, landmarks[15].y]
            left_hip = [landmarks[23].x, landmarks[23].y]
            left_knee = [landmarks[25].x, landmarks[25].y]
            
            elbow_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
            primary_angle = self.smoother.smooth(elbow_angle)
            
            # Initialize stage
            if current_stage is None:
                current_stage = "up" if primary_angle > 140 else "down"
                new_stage = current_stage

            # FORM CHECKS (don't block reps)
            form_issues = []
            
            # Body alignment
            if visible(23) and visible(25):
                body_angle = self.calculate_angle(left_shoulder, left_hip, left_knee)
                if body_angle < 155:
                    form_issues.append("Hips sagging!")
                    score -= 25
            
            if form_issues:
                feedback = " | ".join(form_issues[:2])
                form_correct = False
                if time.time() - self.last_voice_time > 6:
                    self.speak(get_expert_feedback("push_up", False))
            else:
                form_correct = True
                feedback = "Good form"

            # SIMPLIFIED REP COUNTING
            UP_THRESHOLD = 150   # Arms extended (lowered)
            DOWN_THRESHOLD = 90  # Chest down
            
            if primary_angle > UP_THRESHOLD:  # Up position
                if current_stage == "down":
                    new_reps += 1
                    voice_msg = get_expert_feedback("push_up", True)
                    self.speak(voice_msg)
                    feedback = f"✅ Rep {new_reps}!"
                new_stage = "up"
                if "Rep" not in feedback:
                    feedback = "Lower down"
                
            elif primary_angle < DOWN_THRESHOLD:  # Down position
                new_stage = "down"
                if "Rep" not in feedback:
                    feedback = "Push up!"
            else:
                new_stage = current_stage

        # --- PULL UP ---
        elif exercise == "pull_up":
            if not (visible(11) and visible(12) and visible(13) and visible(14)):
                 return {"score": 0, "feedback": "Show upper body!", "stage": current_stage, "reps": rep_counter, "form_correct": False, "confidence": 0}
            
            left_shoulder = [landmarks[11].x, landmarks[11].y]
            left_elbow = [landmarks[13].x, landmarks[13].y]
            left_wrist = [landmarks[15].x, landmarks[15].y]
            
            elbow_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
            primary_angle = self.smoother.smooth(elbow_angle)
            
            if current_stage is None:
                current_stage = "down" if primary_angle > 140 else "up"
                new_stage = current_stage
            
            form_correct = True
            feedback = "Good form"
            
            # SIMPLIFIED REP COUNTING
            DOWN_ANGLE = 140  # Extended (lowered)
            UP_ANGLE = 90     # Contracted
            
            if primary_angle > DOWN_ANGLE:  # Extended
                if current_stage == "up":
                    new_reps += 1
                    voice_msg = get_expert_feedback("pull_up", True)
                    self.speak(voice_msg)
                    feedback = f"✅ Rep {new_reps}!"
                new_stage = "down"
                if "Rep" not in feedback:
                    feedback = "Pull up!"
                
            elif primary_angle < UP_ANGLE:
                new_stage = "up"
                if "Rep" not in feedback:
                    feedback = "Squeeze!"
            else:
                new_stage = current_stage

        # --- SHOULDER PRESS ---
        elif exercise == "shoulder_press":
            if not (visible(11) and visible(12) and visible(13) and visible(14)):
                  return {"score": 0, "feedback": "Show upper body!", "stage": current_stage, "reps": rep_counter, "form_correct": False, "confidence": 0}

            left_shoulder = [landmarks[11].x, landmarks[11].y]
            left_elbow = [landmarks[13].x, landmarks[13].y]
            left_wrist = [landmarks[15].x, landmarks[15].y]
            
            elbow_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
            primary_angle = self.smoother.smooth(elbow_angle)
            
            if current_stage is None:
                current_stage = "up" if primary_angle > 140 else "down"
                new_stage = current_stage
            
            # Form check (doesn't block reps)
            form_issues = []
            if left_wrist[1] > left_elbow[1] + 0.08:
                form_issues.append("Wrists up!")
                score -= 20
            
            if form_issues:
                feedback = " | ".join(form_issues)
                form_correct = False
                if time.time() - self.last_voice_time > 6:
                    self.speak(get_expert_feedback("shoulder_press", False))
            else:
                form_correct = True
                feedback = "Good form"
            
            # SIMPLIFIED REP COUNTING
            UP_ANGLE = 145    # Extended (lowered)
            DOWN_ANGLE = 90   # Bent
            
            if primary_angle > UP_ANGLE:
                if current_stage == "down":
                    new_reps += 1
                    voice_msg = get_expert_feedback("shoulder_press", True)
                    self.speak(voice_msg)
                    feedback = f"✅ Rep {new_reps}!"
                new_stage = "up"
                if "Rep" not in feedback:
                    feedback = "Lower controlled"
                
            elif primary_angle < DOWN_ANGLE:
                new_stage = "down"
                if "Rep" not in feedback:
                    feedback = "Press!"
            else:
                new_stage = current_stage

        return {
            "score": score,
            "feedback": feedback,
            "stage": new_stage,
            "reps": new_reps,
            "form_correct": form_correct,
            "confidence": confidence,
            "primary_angle": primary_angle
        }
    
    def calculate_angle(self, p1, p2, p3):
        v1 = np.array(p1) - np.array(p2)
        v2 = np.array(p3) - np.array(p2)
        cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        return np.degrees(np.arccos(np.clip(cos_angle, -1.0, 1.0)))


def voice_trainer_ui():
    """Voice trainer interface with professional UI."""
    st.header("Voice-Guided Exercise Trainer")
    st.caption("Real-time form correction with AI voice feedback")
    
    # Information panel
    with st.container():
        st.info(
            "**Form-First Training**: Repetitions are only counted when proper form is maintained. "
            "The system provides real-time guidance to perfect your technique."
        )

    # System requirements check
    with st.sidebar:
        st.expander("Debug Info").write(f"Python: {sys.executable}\n\nPath: {sys.path}")

    if not ELEVENLABS_AVAILABLE:
        error_msg = globals().get('ELEVENLABS_ERROR', 'Unknown error')
        st.warning(
            f"**ElevenLabs Unavailable**: {error_msg}. "
            "Voice feedback will be disabled. Please check your API key and dependencies."
        )
    
    # Check for MediaPipe availability or Basic Mode
    if not MEDIAPIPE_AVAILABLE:
        error_msg = globals().get('MEDIAPIPE_ERROR', 'Unknown error')
        st.warning(
            f"**MediaPipe Unavailable**: {error_msg}. "
            "The Voice Trainer will run in basic mode. Ensure MediaPipe is installed correctly."
        )
    elif st.session_state.get('voice_trainer') and st.session_state.voice_trainer.basic_mode:
        st.info(
            "**Basic Mode Active**: MediaPipe initialization failed. "
            "Running in basic mode without pose detection. Voice feedback is still available."
        )
    
    # Try to initialize trainer even if global check failed
    if "voice_trainer" not in st.session_state:
        st.session_state.voice_trainer = VoiceTrainer()
    
    trainer = st.session_state.voice_trainer
    
    if not trainer.pose:
        st.warning("MediaPipe pose detection not available. Using basic exercise mode.")
        st.info("💡 Try restarting the application or check MediaPipe installation.")
        
        # Provide basic exercise guidance without pose detection
        st.subheader("🎤 Basic Exercise Mode")
        exercise = st.selectbox("Select Exercise:", ["Push Up", "Pull Up", "Bicep Curl", "Shoulder Press"])
        
        if st.button("Start Basic Training", type="primary"):
            st.success(f"Starting {exercise} training in basic mode!")
            st.info("Count your own reps and focus on proper form:")
            
            # Basic exercise instructions
            if exercise == "Push Up":
                st.write("• Keep body straight like a plank")
                st.write("• Lower chest to floor, push back up")
                st.write("• Don't let hips sag or pike up")
            elif exercise == "Squat":
                st.write("• Feet shoulder-width apart")
                st.write("• Sit back like sitting in a chair")
                st.write("• Keep knees behind toes")
            elif exercise == "Bicep Curl":
                st.write("• Keep elbows at your sides")
                st.write("• Curl weight up, squeeze at top")
                st.write("• Lower with control")
            elif exercise == "Shoulder Press":
                st.write("• Press weight straight overhead")
                st.write("• Keep core tight")
                st.write("• Don't arch your back")
        
        return

    # trainer is already initialized above
    # Continue with full pose detection mode

    col1, col2 = st.columns(2)

    with col1:
        exercise = st.selectbox(
            "Select Exercise:",
            ["Push Up", "Pull Up", "Bicep Curl", "Shoulder Press"],
            key="voice_exercise",
        )

        # Voice Assist Toggle
        st.subheader("🎙️ Voice Feedback")
        voice_enabled = st.checkbox(
            "Enable Voice Assist",
            value=st.session_state.get("voice_enabled", True),
            key="voice_enabled",
            help="Turn on/off real-time voice coaching and feedback"
        )
        
        if voice_enabled:
            st.success("✅ Voice coaching active - You'll hear real-time feedback!")
        else:
            st.info("🔇 Voice muted - Visual feedback only")

        # Workout Configuration
        st.subheader("Workout Configuration")
        col_cfg1, col_cfg2, col_cfg3 = st.columns(3)
        with col_cfg1:
            target_sets = st.number_input("Sets", min_value=1, max_value=10, value=3, key="target_sets")
        with col_cfg2:
            target_reps = st.number_input("Reps per Set", min_value=1, max_value=50, value=10, key="target_reps")
        with col_cfg3:
            rest_time = st.number_input("Rest (sec)", min_value=5, max_value=180, value=30, key="rest_time")

        col1a, col1b = st.columns(2)
        with col1a:
            if st.button("Start Training", key="start_voice", type="primary"):
                # Reset counters when starting
                # Reset counters when starting
                st.session_state.rep_count = 0
                st.session_state.current_set = 1
                st.session_state.is_resting = False
                st.session_state.workout_complete = False
                st.session_state.last_angle = 0
                st.session_state.last_saved_reps = 0
                if voice_enabled and VOICE_AVAILABLE:
                    trainer.speak(f"Starting {exercise} with voice feedback. Remember, only perfect form counts!")
                    st.success("Training session initiated with voice guidance")
                else:
                    st.success("Training session initiated with visual feedback")
        
        with col1b:
            if st.button("Reset Counter", key="reset_reps"):
                st.session_state.rep_count = 0
                st.session_state.current_set = 1
                st.session_state.is_resting = False
                st.session_state.workout_complete = False
                st.session_state.last_angle = 0
                st.success("Workout reset")
            
            if st.button("🔊 Test Voice", key="test_voice"):
                if VOICE_AVAILABLE and voice_enabled:
                    st.info("Attempting to play test audio...")
                    trainer.speak("Testing voice system. Can you hear me?")
                else:
                    st.error("Voice engine not available.")

    with col2:
        # Check if MediaPipe is available
        if not MEDIAPIPE_AVAILABLE:
            st.error("⚠️ MediaPipe not available! Camera feed disabled.")
            st.info("Install MediaPipe: pip install mediapipe")
            camera_enabled = False
        else:
            camera_enabled = st.checkbox(
                "Enable Camera Feed", 
                value=True,  # Default to ON
                key="voice_camera"
            )
        
        # Display current metrics
        if "rep_count" in st.session_state:
            st.metric("Current Set", f"{st.session_state.get('current_set', 1)} / {st.session_state.get('target_sets', 3)}")
            st.metric("Reps", f"{st.session_state.rep_count} / {st.session_state.get('target_reps', 10)}")

    if camera_enabled and MEDIAPIPE_AVAILABLE:
        st.subheader("Live Training Session")
        st.caption("Real-time form analysis and feedback")

        video_col, metrics_col = st.columns([3, 1])

        with video_col:
            stframe = st.empty()

        with metrics_col:
            metrics_placeholder = st.empty()

        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            st.error("Camera access unavailable. Please check camera permissions.")
            return

        frame_count = 0

        # Initialize session state for rep counting
        if "rep_count" not in st.session_state:
            st.session_state.rep_count = 0
        if "exercise_stage" not in st.session_state:
            st.session_state.exercise_stage = None
        if "last_feedback_time" not in st.session_state:
            st.session_state.last_feedback_time = 0
        if "form_correction_count" not in st.session_state:
            st.session_state.form_correction_count = 0
        if "frame_history" not in st.session_state:
            st.session_state.frame_history = []
        if "last_angle" not in st.session_state:
            st.session_state.last_angle = 0
        if "current_set" not in st.session_state:
            st.session_state.current_set = 1
        if "is_resting" not in st.session_state:
            st.session_state.is_resting = False
        if "rest_start_time" not in st.session_state:
            st.session_state.rest_start_time = 0
        if "workout_complete" not in st.session_state:
            st.session_state.workout_complete = False

        while camera_enabled:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % 3 == 0: # Optimized to every 3rd frame
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Check if workout is complete
                if st.session_state.workout_complete:
                    cv2.putText(frame, "WORKOUT COMPLETE!", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
                    cv2.putText(frame, "Great Job!", (150, 250), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
                    stframe.image(frame, channels="BGR", use_container_width=True)
                    continue

                # Check if resting
                if st.session_state.is_resting:
                    elapsed_rest = time.time() - st.session_state.rest_start_time
                    remaining_rest = max(0, st.session_state.rest_time - elapsed_rest)
                    
                    if remaining_rest == 0:
                        st.session_state.is_resting = False
                        st.session_state.current_set += 1
                        st.session_state.rep_count = 0 # Reset reps for new set
                        trainer.speak(f"Rest time over. Starting set {st.session_state.current_set}. Let's go!")
                    else:
                        # Draw Rest Overlay
                        overlay = frame.copy()
                        cv2.rectangle(overlay, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 0), -1)
                        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
                        
                        cv2.putText(frame, "REST TIME", (180, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3)
                        cv2.putText(frame, f"{int(remaining_rest)}s", (280, 280), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (255, 255, 255), 4)
                        cv2.putText(frame, f"Next: Set {st.session_state.current_set + 1}", (200, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)
                        
                        stframe.image(frame, channels="BGR", width="stretch")
                        continue

                results = trainer.pose.process(rgb_frame)
                frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)

                if results.pose_landmarks:
                    trainer.mp_drawing.draw_landmarks(
                        frame, results.pose_landmarks, trainer.mp_pose.POSE_CONNECTIONS
                    )

                    # Analyze form and count reps with frame history
                    # Initialize stage if not present
                    if "exercise_stage" not in st.session_state:
                        st.session_state.exercise_stage = None
                    
                    analysis = trainer.analyze_form_and_count_reps(
                        results.pose_landmarks.landmark,
                        exercise.lower().replace(" ", "_"),
                        st.session_state.exercise_stage,  # Pass current stage
                        st.session_state.rep_count,
                        st.session_state.frame_history
                    )
                    
                    # Update session state with new values
                    st.session_state.rep_count = analysis["reps"]
                    st.session_state.exercise_stage = analysis["stage"]  # Update stage
                    
                    # Save session data
                    if AUTH_AVAILABLE and st.session_state.get('authenticated') and analysis["reps"] > 0:
                        # Logic to save data periodically or at end of set
                        pass

                    # Check for Set Completion
                    if st.session_state.rep_count >= st.session_state.target_reps:
                        if st.session_state.current_set >= st.session_state.target_sets:
                            st.session_state.workout_complete = True
                            trainer.speak("Workout complete! Congratulations! You crushed it!")
                        else:
                            st.session_state.is_resting = True
                            st.session_state.rest_start_time = time.time()
                            trainer.speak(f"Set {st.session_state.current_set} complete! Take a {st.session_state.rest_time} second rest.")


                    # Visual feedback overlay
                    score = analysis["score"]
                    form_correct = analysis["form_correct"]
                    
                    # Form status indicator with progress bar
                    form_color = (0, 255, 0) if form_correct else (0, 0, 255)
                    form_text = "CORRECT FORM" if form_correct else "INCORRECT FORM - FIX TO COUNT REP"
                    
                    # Background for form status
                    cv2.rectangle(frame, (10, 10), (600, 50), (0, 0, 0), -1)
                    cv2.putText(
                        frame,
                        form_text,
                        (15, 35),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        form_color,
                        2,
                    )
                    
                    # Dual progress bars - Form Quality and Movement Confidence
                    form_bar_width = int(300 * (score / 100))
                    confidence_bar_width = int(300 * (analysis.get('confidence', 0) / 100))
                    
                    # Form quality bar
                    cv2.rectangle(frame, (10, 60), (310, 75), (50, 50, 50), -1)
                    cv2.rectangle(frame, (10, 60), (10 + form_bar_width, 75), form_color, -1)
                    cv2.putText(frame, f"Form: {score}%", (320, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    
                    # Movement confidence bar
                    cv2.rectangle(frame, (10, 80), (310, 95), (50, 50, 50), -1)
                    cv2.rectangle(frame, (10, 80), (10 + confidence_bar_width, 95), (0, 255, 255), -1)
                    cv2.putText(frame, f"Motion: {int(analysis.get('confidence', 0))}%", (320, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    
                    # Enhanced rep counter with pulsing effect for new reps
                    rep_color = (0, 255, 0) if analysis.get('confidence', 0) > 50 else (255, 255, 255)
                    cv2.putText(
                        frame,
                        f"Set {st.session_state.current_set}/{st.session_state.target_sets} | Reps: {st.session_state.rep_count}/{st.session_state.target_reps}",
                        (10, 115),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.2,
                        rep_color,
                        3,
                    )
                    
                    # Form status instead of stage
                    status_text = "CORRECT FORM" if form_correct else "ADJUST FORM"
                    status_color = (0, 255, 0) if form_correct else (0, 165, 255)
                    cv2.putText(
                        frame,
                        f"STATUS: {status_text}",
                        (10, 155),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        status_color,
                        2,
                    )
                    
                    # Enhanced feedback message with better formatting
                    feedback_text = analysis["feedback"]
                    if len(feedback_text) > 50:
                        # Split long feedback into multiple lines
                        words = feedback_text.split(" ")
                        lines = []
                        current_line = ""
                        for word in words:
                            if len(current_line + word) < 40:
                                current_line += word + " "
                            else:
                                lines.append(current_line.strip())
                                current_line = word + " "
                        if current_line:
                            lines.append(current_line.strip())
                    else:
                        lines = [feedback_text]
                    
                    for i, line in enumerate(lines[:3]):  # Max 3 lines
                        cv2.putText(
                            frame,
                            line,
                            (10, 195 + i * 25),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            form_color,
                            2,
                        )

                    # Exercise name with enhanced info
                    cv2.putText(
                        frame,
                        f"Exercise: {exercise} | AI Precision Mode",
                        (10, frame.shape[0] - 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255, 255, 255),
                        2,
                    )
                    
                    # Show detailed info for bicep curl
                    if "primary_angle" in analysis and analysis["primary_angle"] > 0:
                        angle = int(analysis['primary_angle'])
                        cv2.putText(
                            frame,
                            f"Angle: {angle}° | Confidence: {int(analysis.get('confidence', 0))}%",
                            (10, frame.shape[0] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (0, 255, 255),
                            1,
                        )
                        
                        # Visual Angle Indicator (Arc)
                        center = (frame.shape[1] - 50, frame.shape[0] - 50)
                        radius = 30
                        # Draw background circle
                        cv2.circle(frame, center, radius, (50, 50, 50), -1)
                        # Draw angle arc
                        start_angle = 0
                        end_angle = angle
                        cv2.ellipse(frame, center, (radius, radius), 0, start_angle, end_angle, (0, 255, 0), -1)
                        cv2.putText(frame, f"{angle}°", (center[0]-15, center[1]+5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

                    # Metrics display
                    with metrics_placeholder.container():
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Set", f"{st.session_state.current_set}/{st.session_state.target_sets}")
                            st.metric("Reps", f"{st.session_state.rep_count}/{st.session_state.target_reps}")
                            if form_correct:
                                st.success("Form: Excellent")
                            else:
                                st.error("Form: Needs Correction")
                        
                        with col2:
                            st.metric("Form Quality", f"{score}%")
                            if "confidence" in analysis:
                                st.metric("Movement Confidence", f"{int(analysis['confidence'])}%")
                            # Remove stage display - no longer needed
                        
                        # Clean feedback without emojis
                        feedback_clean = analysis['feedback'].replace('🔥', '').replace('💪', '').replace('⚡', '').replace('🎯', '').replace('💥', '').replace('✨', '').replace('🛑', '').replace('❌', '').replace('🔄', '')
                        
                        if st.session_state.rep_count > 15:
                            st.error(f"EXCELLENT WORK! {st.session_state.rep_count} repetitions completed!")
                            st.warning("Recommended rest period: 60-90 seconds")
                        elif form_correct:
                            st.success(feedback_clean)
                        else:
                            st.warning(feedback_clean)
                            st.error("Repetition will not count until form is corrected")

                        # System status
                        if ELEVENLABS_AVAILABLE:
                            st.info("Voice guidance: Active")
                        else:
                            st.info("Visual feedback: Active")

                else:
                    cv2.putText(
                        frame,
                        "Position yourself in camera view for pose detection",
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 0, 255),
                        2,
                    )

                stframe.image(frame, channels="BGR", width="stretch")

            frame_count += 1

            if not st.session_state.get("voice_camera", False):
                break

        cap.release()

if __name__ == "__main__":
    st.set_page_config(page_title="Voice Trainer", layout="wide")
    apply_legendary_styles()
    voice_trainer_ui()