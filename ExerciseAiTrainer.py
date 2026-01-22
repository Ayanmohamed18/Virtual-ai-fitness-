import cv2
import numpy as np
import streamlit as st
import joblib
from AiTrainer_utils import *
import time

try:
    import PoseModule2 as pm
    import tensorflow as tf
    from tensorflow.keras.models import load_model
    import mediapipe as mp
    # Initialize MediaPipe pose
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False

# Define relevant landmarks indices if MediaPipe is available
if MEDIAPIPE_AVAILABLE:
    # These are already initialized in the try block above
    # Define relevant landmarks indices
    relevant_landmarks_indices = [
        mp_pose.PoseLandmark.LEFT_SHOULDER.value,
        mp_pose.PoseLandmark.RIGHT_SHOULDER.value,
    mp_pose.PoseLandmark.LEFT_ELBOW.value,
    mp_pose.PoseLandmark.RIGHT_ELBOW.value,
    mp_pose.PoseLandmark.LEFT_WRIST.value,
    mp_pose.PoseLandmark.RIGHT_WRIST.value,
    mp_pose.PoseLandmark.LEFT_HIP.value,
    mp_pose.PoseLandmark.RIGHT_HIP.value,
    mp_pose.PoseLandmark.LEFT_KNEE.value,
    mp_pose.PoseLandmark.RIGHT_KNEE.value,
    mp_pose.PoseLandmark.LEFT_ANKLE.value,
    mp_pose.PoseLandmark.RIGHT_ANKLE.value,
]

# Function to calculate angle between three points
def calculate_angle(a, b, c):
    if np.any(np.array([a, b, c]) == 0):
        return -1.0  # Placeholder for missing landmarks
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(
        a[1] - b[1], a[0] - b[0]
    )
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

# Function to calculate Euclidean distance between two points
def calculate_distance(a, b):
    if np.any(np.array([a, b]) == 0):
        return -1.0  # Placeholder for missing landmarks
    a = np.array(a)
    b = np.array(b)
    return np.linalg.norm(a - b)

def calculate_y_distance(a, b):
    if np.any(np.array([a, b]) == 0):
        return -1.0  # Placeholder for missing landmarks
    return np.abs(a[1] - b[1])


def draw_styled_text(
    frame,
    text,
    position,
    font=cv2.FONT_HERSHEY_SIMPLEX,
    font_scale=0.55,
    font_color=(255, 255, 255),
    font_thickness=2,
    bg_color=(0, 0, 0),
    padding=5,
):
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_x, text_y = position
    box_coords = (
        (text_x - padding, text_y + padding),
        (text_x + text_size[0] + padding, text_y - text_size[1] - padding),
    )
    cv2.rectangle(frame, box_coords[0], box_coords[1], bg_color, cv2.FILLED)
    cv2.putText(
        frame,
        text,
        (text_x, text_y),
        font,
        font_scale,
        font_color,
        font_thickness,
        lineType=cv2.LINE_AA,
    )


def count_repetition_push_up(
    detector, img, landmark_list, stage, counter, exercise_instance
):
    right_arm_angle = detector.find_angle(img, 12, 14, 16)
    right_shoulder = landmark_list[12][1:]
    right_wrist = landmark_list[16][1:]
    left_arm_angle = detector.find_angle(img, 11, 13, 15)
    left_shoulder = landmark_list[11][1:]
    exercise_instance.visualize_angle(img, right_arm_angle, right_shoulder)
    exercise_instance.visualize_angle(img, left_arm_angle, left_shoulder)

    if left_arm_angle < 220:
        stage = "down"
    if left_arm_angle > 240 and stage == "down":
        stage = "up"
        counter += 1

    return stage, counter


def count_repetition_squat(
    detector, img, landmark_list, stage, counter, exercise_instance
):
    right_leg_angle = detector.find_angle(img, 24, 26, 28)
    left_leg_angle = detector.find_angle(img, 23, 25, 27)
    right_leg = landmark_list[26][1:]
    exercise_instance.visualize_angle(img, right_leg_angle, right_leg)

    if right_leg_angle > 160 and left_leg_angle < 220:
        stage = "down"
    if right_leg_angle < 140 and left_leg_angle > 210 and stage == "down":
        stage = "up"
        counter += 1

    return stage, counter


def count_repetition_bicep_curl(
    detector, img, landmark_list, stage_right, stage_left, counter, exercise_instance
):
    right_arm_angle = detector.find_angle(img, 12, 14, 16)
    left_arm_angle = detector.find_angle(img, 11, 13, 15)
    exercise_instance.visualize_angle(img, right_arm_angle, landmark_list[14][1:])
    exercise_instance.visualize_angle(img, left_arm_angle, landmark_list[13][1:])

    if right_arm_angle > 160 and right_arm_angle < 200:
        stage_right = "down"
    if left_arm_angle < 200 and left_arm_angle > 140:
        stage_left = "down"

    if (
        stage_right == "down"
        and (right_arm_angle > 310 or right_arm_angle < 60)
        and (left_arm_angle > 310 or left_arm_angle < 60)
        and stage_left == "down"
    ):
        stage_right = "up"
        stage_left = "up"
        counter += 1

    return stage_right, stage_left, counter


def count_repetition_shoulder_press(
    detector, img, landmark_list, stage, counter, exercise_instance
):
    right_arm_angle = detector.find_angle(img, 12, 14, 16)
    left_arm_angle = detector.find_angle(img, 11, 13, 15)
    right_elbow = landmark_list[14][1:]
    exercise_instance.visualize_angle(img, right_arm_angle, right_elbow)

    if right_arm_angle > 280 and left_arm_angle < 80:
        stage = "down"
    if right_arm_angle < 240 and left_arm_angle > 120 and stage == "down":
        stage = "up"
        counter += 1

    return stage, counter

class Exercise:
    def __init__(self):
        try:
            self.lstm_model = load_model(
                "final_forthesis_bidirectionallstm_and_encoders_exercise_classifier_model.h5"
            )
        except Exception as e:
            print(f"Error loading LSTM model: {e}")
            self.lstm_model = None

        try:
            self.scaler = joblib.load("thesis_bidirectionallstm_scaler.pkl")
        except Exception as e:
            print(f"Error loading scaler: {e}")
            self.scaler = None

        try:
            self.label_encoder = joblib.load(
                "thesis_bidirectionallstm_label_encoder.pkl"
            )
            self.exercise_classes = self.label_encoder.classes_
        except Exception as e:
            print(f"Error loading label encoder: {e}")
            self.label_encoder = None
            self.exercise_classes = []
            
        # Initialize state variables
        self.reset_state()

    def reset_state(self):
        self.landmarks_window = []
        self.frame_count = 0
        self.current_prediction = "No prediction yet"
        self.counters = {"push_up": 0, "squat": 0, "bicep_curl": 0, "shoulder_press": 0}
        self.stages = {
            "push_up": None,
            "squat": None,
            "left_bicep_curl": None,
            "right_bicep_curl": None,
            "shoulder_press": None,
        }
        self.window_size = 30
        
        # Initialize helper classes
        self.detector = pm.posture_detector()
        self.pose = mp.solutions.pose.Pose()

    def process_frame(self, frame):
        """
        Process a single frame: predict exercise and count repetitions.
        Returns the processed frame with annotations.
        """
        # Feature extraction and prediction logic
        landmarks = self.preprocess_frame(frame, self.pose)
        if len(landmarks) == len(relevant_landmarks_indices) * 3:
            features = self.extract_features(landmarks)
            if len(features) == 22:
                self.landmarks_window.append(features)

        self.frame_count += 1

        if len(self.landmarks_window) == self.window_size:
            landmarks_window_np = (
                np.array(self.landmarks_window).flatten().reshape(1, -1)
            )
            scaled_landmarks_window = self.scaler.transform(landmarks_window_np)
            scaled_landmarks_window = scaled_landmarks_window.reshape(
                1, self.window_size, 22
            )

            prediction = self.lstm_model.predict(scaled_landmarks_window)
            predicted_class = np.argmax(prediction, axis=1)[0]
            
            if predicted_class < len(self.exercise_classes):
                self.current_prediction = self.exercise_classes[predicted_class]
                # print(f"Current Prediction: {self.current_prediction}")

            self.landmarks_window = [] # Reset window
            self.frame_count = 0

        # Repetition counting logic
        img = self.detector.find_person(frame, draw=True)
        landmark_list = self.detector.find_landmarks(frame, draw=True)
        
        if len(landmark_list) > 0:
            if self.current_prediction == "push-up":
                self.stages["push_up"], self.counters["push_up"] = count_repetition_push_up(
                    self.detector, frame, landmark_list, self.stages["push_up"], self.counters["push_up"], self
                )
            elif self.current_prediction == "squat":
                self.stages["squat"], self.counters["squat"] = count_repetition_squat(
                    self.detector, frame, landmark_list, self.stages["squat"], self.counters["squat"], self
                )
            elif self.current_prediction == "barbell biceps curl":
                (self.stages["right_bicep_curl"], self.stages["left_bicep_curl"], self.counters["bicep_curl"]) = count_repetition_bicep_curl(
                    self.detector, frame, landmark_list, self.stages["right_bicep_curl"], self.stages["left_bicep_curl"], self.counters["bicep_curl"], self
                )
            elif self.current_prediction == "shoulder press":
                self.stages["shoulder_press"], self.counters["shoulder_press"] = count_repetition_shoulder_press(
                    self.detector, frame, landmark_list, self.stages["shoulder_press"], self.counters["shoulder_press"], self
                )

        # Draw UI
        exercise_name_map = {
            "push_up": "Push-up",
            "squat": "Squat",
            "bicep_curl": "Curl",
            "shoulder_press": "Press",
        }

        height, width, _ = frame.shape
        num_exercises = len(self.counters)
        vertical_spacing = height // (num_exercises + 1)

        # Draw overlays
        cv2.rectangle(frame, (0, 0), (120, height), (0, 0, 0), -1)
        cv2.rectangle(frame, (0, 0), (width, 30), (0, 0, 0), -1)

        short_name = exercise_name_map.get(self.current_prediction, self.current_prediction)
        draw_styled_text(frame, f"Exercise: {short_name}", ((width - 290) // 2 + 100, 20))

        for idx, (exercise, count) in enumerate(self.counters.items()):
            short_name = exercise_name_map.get(exercise, exercise)
            draw_styled_text(frame, f"{short_name}: {count}", (10, (idx + 1) * vertical_spacing))

        return frame

    # Auto classify and count method with repetition counting logic - LEGACY WRAPPER
    def auto_classify_and_count(self):
        """
        Legacy method for local cv2.VideoCapture usage.
        """
        stframe = st.empty()
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error opening webcam.")
            return

        print("Starting real-time classification...")
        self.reset_state()
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error reading frame.")
                break
                
            frame = self.process_frame(frame)
            stframe.image(frame, channels="BGR", use_container_width=True)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

    # Check if hands are joined together in a 'prayer' gesture
    def are_hands_joined(self, landmark_list, stop, is_video=False):
        # Extract wrist coordinates
        left_wrist = landmark_list[15][1:]  # (x, y) for left wrist
        right_wrist = landmark_list[16][1:]  # (x, y) for right wrist

        # Calculate the Euclidean distance between the wrists
        distance = np.linalg.norm(np.array(left_wrist) - np.array(right_wrist))
        # Consider hands joined if the distance is below a certain threshold, e.g., 50 pixels
        if distance < 30 and not is_video:
            print("JOINED HANDS")
            stop = True
            return stop

        return False

    # Visualize the angle between 3 point on screen
    def visualize_angle(self, img, angle, landmark):
        cv2.putText(
            img,
            str(angle),
            tuple(np.multiply(landmark, [640, 480]).astype(int)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

    # Visualize repetitions of the exercise on screen
    def repetitions_counter(self, img, counter):
        cv2.rectangle(img, (0, 0), (225, 73), (245, 117, 16), -1)

        # Rep data
        cv2.putText(
            img,
            "REPS",
            (15, 12),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 0),
            1,
            cv2.LINE_AA,
        )
        cv2.putText(
            img,
            str(counter),
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

    # Define push-up method
    def push_up(self, cap, is_video=False, counter=0, stage=None):
        self.exercise_method(
            cap, is_video, count_repetition_push_up, counter=counter, stage=stage
        )

    # Define squat method
    def squat(self, cap, is_video=False, counter=0, stage=None):
        self.exercise_method(
            cap, is_video, count_repetition_squat, counter=counter, stage=stage
        )

    # Define bicep curl method
    def bicept_curl(
        self, cap, is_video=False, counter=0, stage_right=None, stage_left=None
    ):
        self.exercise_method(
            cap,
            is_video,
            count_repetition_bicep_curl,
            multi_stage=True,
            counter=counter,
            stage_right=stage_right,
            stage_left=stage_left,
        )

    # Define shoulder press method
    def shoulder_press(self, cap, is_video=False, counter=0, stage=None):
        self.exercise_method(
            cap, is_video, count_repetition_shoulder_press, counter=counter, stage=stage
        )

    # Generic exercise method
    # Generic exercise method
    # Generic exercise method
    def exercise_method(
        self,
        cap,
        is_video,
        count_repetition_function,
        multi_stage=False,
        counter=0,
        stage=None,
        stage_right=None,
        stage_left=None,
    ):
        if is_video:
            stframe = st.empty()
            detector = pm.posture_detector()

            # Get the original video's FPS
            original_fps = cap.get(cv2.CAP_PROP_FPS)
            frame_time = 1 / original_fps

            frame_count = 0
            start_time = time.time()
            last_update_time = start_time

            update_interval = 0.1  # Update display every 100ms

            while cap.isOpened():
                current_time = time.time()
                elapsed_time = current_time - start_time

                # Determine how many frames should have been processed by now
                target_frame = int(elapsed_time * original_fps)

                # Process frames until we catch up to where we should be
                while frame_count < target_frame:
                    ret, frame = cap.read()
                    if not ret:
                        print("End of video.")
                        return

                    frame_count += 1

                    # Process the last frame we read
                    if frame_count == target_frame:
                        img = detector.find_person(frame)
                        landmark_list = detector.find_landmarks(img, draw=False)

                        if len(landmark_list) != 0:
                            if multi_stage:
                                stage_right, stage_left, counter = (
                                    count_repetition_function(
                                        detector,
                                        img,
                                        landmark_list,
                                        stage_right,
                                        stage_left,
                                        counter,
                                        self,
                                    )
                                )
                            else:
                                stage, counter = count_repetition_function(
                                    detector, img, landmark_list, stage, counter, self
                                )

                            if self.are_hands_joined(
                                landmark_list, stop=False, is_video=is_video
                            ):
                                return

                        self.repetitions_counter(img, counter)

                # Update display at regular intervals
                if current_time - last_update_time >= update_interval:
                    stframe.image(img, channels="BGR", use_container_width=True)
                    last_update_time = current_time

                # Small sleep to prevent busy-waiting
                time.sleep(0.001)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            cap.release()
            cv2.destroyAllWindows()
        else:
            # Original webcam exercise code
            stframe = st.empty()
            cap = cv2.VideoCapture(0)
            detector = pm.posture_detector()

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                img = detector.find_person(frame)
                landmark_list = detector.find_landmarks(img, draw=False)

                if len(landmark_list) != 0:
                    if multi_stage:
                        stage_right, stage_left, counter = count_repetition_function(
                            detector,
                            img,
                            landmark_list,
                            stage_right,
                            stage_left,
                            counter,
                            self,
                        )
                    else:
                        stage, counter = count_repetition_function(
                            detector, img, landmark_list, stage, counter, self
                        )

                    if self.are_hands_joined(landmark_list, stop=False):
                        break

                self.repetitions_counter(img, counter)
                stframe.image(img, channels="BGR", use_container_width=True)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            cap.release()
            cv2.destroyAllWindows()
