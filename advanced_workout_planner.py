#!/usr/bin/env python3

import streamlit as st
import json
from datetime import datetime
from typing import Dict, List, Any
from io import BytesIO
import time

# Try to import PDF generation libraries
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

class WorkoutRecommendationEngine:
    def __init__(self):
        self.user_responses = {}
        self.workout_plan = {}
        
    def get_foundational_questions(self) -> List[Dict]:
        """The 10 foundational questions for personalized workout planning"""
        return [
            {
                "id": "primary_goal",
                "question": "Beyond just 'getting fit,' what is the single most important, specific outcome you want to achieve in the next 3 to 6 months?",
                "type": "selectbox",
                "options": [
                    "Lose 5-15 kg of body fat",
                    "Build noticeable muscle mass",
                    "Run 5K without stopping",
                    "Increase overall strength significantly", 
                    "Improve energy and daily function",
                    "Prepare for a specific event (wedding, vacation, etc.)",
                    "Reduce back/joint pain through fitness",
                    "Build confidence and feel better about my body"
                ],
                "why": "This cuts through vague goals and creates a specific target that guides every decision."
            },
            {
                "id": "time_commitment", 
                "question": "Looking at your typical week, how many days can you realistically commit to exercise?",
                "type": "selectbox",
                "options": ["2 days per week", "3 days per week", "4 days per week", "5 days per week", "6+ days per week"],
                "why": "Realism is the key to consistency. The plan must fit your actual life."
            },
            {
                "id": "session_length",
                "question": "How long can each workout session realistically be?",
                "type": "selectbox", 
                "options": ["20-30 minutes", "30-45 minutes", "45-60 minutes", "60+ minutes"],
                "why": "Time constraints determine exercise selection and workout structure."
            },
            {
                "id": "workout_location",
                "question": "Where will you be doing most of your workouts?",
                "type": "selectbox",
                "options": ["Home with no equipment", "Home with basic equipment (dumbbells, bands)", "Home gym setup", "Commercial gym", "Outdoor/park", "Mix of locations"],
                "why": "Equipment availability dictates the entire exercise library we can use."
            },
            {
                "id": "injuries_conditions",
                "question": "Do you have any current injuries, past injuries, or medical conditions I should know about?",
                "type": "multiselect",
                "options": ["None", "Lower back issues", "Knee problems", "Shoulder/neck pain", "High blood pressure", "Diabetes", "Heart condition", "Other chronic condition"],
                "why": "Safety is priority #1. This determines exercise modifications and restrictions."
            },
            {
                "id": "fitness_history",
                "question": "How would you describe your exercise history over the last 2 years?",
                "type": "selectbox",
                "options": [
                    "Complete beginner - little to no exercise",
                    "Occasional exerciser - on and off for months", 
                    "Consistent beginner - regular light exercise",
                    "Intermediate - consistent moderate exercise",
                    "Advanced - consistent intense training"
                ],
                "why": "This determines starting intensity and exercise complexity."
            },
            {
                "id": "daily_activity",
                "question": "Rate your daily physical activity level outside of planned workouts (1-10 scale)",
                "type": "slider",
                "range": [1, 10],
                "labels": {"1": "Desk job, mostly sedentary", "10": "Very active job, always moving"},
                "why": "Total daily activity affects recovery needs and workout intensity."
            },
            {
                "id": "sleep_stress",
                "question": "How many hours of quality sleep do you typically get per night?",
                "type": "selectbox",
                "options": ["Less than 6 hours", "6-7 hours", "7-8 hours", "8+ hours"],
                "why": "Recovery determines how hard you can train and how fast you'll see results."
            },
            {
                "id": "stress_level",
                "question": "How would you describe your current stress levels?",
                "type": "selectbox", 
                "options": ["Low stress", "Manageable stress", "High stress", "Very high stress"],
                "why": "High stress affects recovery and may require modified training intensity."
            },
            {
                "id": "past_obstacles",
                "question": "What has caused you to fall off track with fitness plans in the past?",
                "type": "multiselect",
                "options": [
                    "Too time consuming",
                    "Too complicated/confusing", 
                    "Got bored with routine",
                    "Too intense/difficult",
                    "Lack of visible results",
                    "Injuries or pain",
                    "Life got busy",
                    "Lost motivation",
                    "No accountability"
                ],
                "why": "Learning from past failures helps build a resilient plan."
            }
        ]
    
    def get_architectural_questions(self) -> List[Dict]:
        """The 5 architectural questions for plan structure"""
        return [
            {
                "id": "biometrics",
                "question": "Please provide your basic information for personalized calculations",
                "type": "form",
                "fields": {
                    "age": {"type": "number", "min": 16, "max": 80},
                    "height_cm": {"type": "number", "min": 140, "max": 220},
                    "weight_kg": {"type": "number", "min": 40, "max": 200},
                    "gender": {"type": "selectbox", "options": ["Male", "Female", "Prefer not to say"]}
                },
                "why": "Essential for calculating caloric needs and setting realistic goals."
            },
            {
                "id": "training_split",
                "question": "Do you have a preference for workout structure?",
                "type": "selectbox",
                "options": [
                    "Full Body (all muscles each session) - RECOMMENDED for beginners",
                    "Upper/Lower Split (alternating days)",
                    "Push/Pull/Legs Split", 
                    "Let you decide based on my schedule"
                ],
                "why": "Training split affects weekly schedule and exercise selection."
            },
            {
                "id": "cardio_preference", 
                "question": "How much time per week can you dedicate to cardio?",
                "type": "selectbox",
                "options": ["0-30 minutes", "30-60 minutes", "60-90 minutes", "90+ minutes"],
                "why": "Cardio programming must fit within total time commitment."
            },
            {
                "id": "cardio_type",
                "question": "What type of cardio do you prefer?",
                "type": "selectbox",
                "options": [
                    "LISS - Steady pace (walking, light jogging)",
                    "HIIT - High intensity intervals", 
                    "Mixed - Variety of both",
                    "Whatever is most effective"
                ],
                "why": "Preference affects adherence and enjoyment."
            },
            {
                "id": "movement_confidence",
                "question": "Rate your confidence with these basic movements (1-5 scale)",
                "type": "form",
                "fields": {
                    "squat": {"type": "slider", "min": 1, "max": 5, "label": "Bodyweight Squat"},
                    "pushup": {"type": "slider", "min": 1, "max": 5, "label": "Push-up"},
                    "row": {"type": "slider", "min": 1, "max": 5, "label": "Pulling/Rowing motion"},
                    "overhead": {"type": "slider", "min": 1, "max": 5, "label": "Overhead Press"}
                },
                "why": "Determines starting exercise variations and progressions."
            },
            {
                "id": "plan_duration",
                "question": "How many weeks would you like this plan to cover?",
                "type": "selectbox",
                "options": ["1 Week", "2 Weeks", "3 Weeks", "4 Weeks"],
                "why": "We will build a progressive plan that evolves over this duration."
            }
        ]

class PersonalizedWorkoutGenerator:
    def __init__(self, responses: Dict):
        self.responses = responses
        
    def generate_plan(self) -> Dict:
        """Generate a complete personalized workout plan"""
        
        # Analyze responses to determine plan parameters
        plan_params = self._analyze_responses()
        
        # Determine duration
        duration_str = plan_params.get("plan_duration", "4 Weeks")
        num_weeks = int(duration_str.split()[0])
        
        # Generate weekly plans
        weekly_plans = {}
        for week in range(1, num_weeks + 1):
            weekly_plans[f"Week {week}"] = self._create_weekly_plan(week, plan_params)
            
        # Generate the actual workout plan
        workout_plan = {
            "plan_overview": self._create_plan_overview(plan_params),
            "weekly_plans": weekly_plans, # New structure
            "exercise_library": self._create_exercise_library(plan_params),
            "progression_rules": self._create_progression_rules(plan_params),
            "nutrition_guidelines": self._create_nutrition_guidelines(plan_params),
            "success_metrics": self._create_success_metrics(plan_params)
        }
        
        return workout_plan
    
    def _analyze_responses(self) -> Dict:
        """Analyze user responses to determine plan parameters"""
        
        # Determine experience level
        fitness_history = self.responses.get("fitness_history", "")
        if "Complete beginner" in fitness_history or "Occasional exerciser" in fitness_history:
            experience_level = "beginner"
        elif "Consistent beginner" in fitness_history or "Intermediate" in fitness_history:
            experience_level = "intermediate" 
        else:
            experience_level = "advanced"
            
        # Determine primary focus
        goal = self.responses.get("primary_goal", "")
        if "fat" in goal.lower() or "lose" in goal.lower():
            primary_focus = "fat_loss"
        elif "muscle" in goal.lower() or "strength" in goal.lower():
            primary_focus = "muscle_building"
        elif "run" in goal.lower() or "cardio" in goal.lower():
            primary_focus = "endurance"
        else:
            primary_focus = "general_fitness"
            
        # Determine training frequency
        days_per_week = int(self.responses.get("time_commitment", "3 days")[0])
        
        # Determine session length
        session_length = self.responses.get("session_length", "30-45 minutes")
        if "20-30" in session_length:
            session_minutes = 25
        elif "30-45" in session_length:
            session_minutes = 40
        elif "45-60" in session_length:
            session_minutes = 55
        else:
            session_minutes = 70
            
        # Determine equipment availability
        location = self.responses.get("workout_location", "")
        if "no equipment" in location.lower():
            equipment_level = "bodyweight"
        elif "basic equipment" in location.lower():
            equipment_level = "home_basic"
        elif "home gym" in location.lower():
            equipment_level = "home_advanced"
        elif "commercial gym" in location.lower():
            equipment_level = "full_gym"
        else:
            equipment_level = "minimal"
            
        return {
            "experience_level": experience_level,
            "primary_focus": primary_focus,
            "days_per_week": days_per_week,
            "session_minutes": session_minutes,
            "equipment_level": equipment_level,
            "plan_duration": self.responses.get("plan_duration", "4 Weeks"),
            "injuries": self.responses.get("injuries_conditions", []),
            "sleep_quality": self.responses.get("sleep_stress", ""),
            "stress_level": self.responses.get("stress_level", ""),
            "past_obstacles": self.responses.get("past_obstacles", [])
        }
    
    def _create_plan_overview(self, params: Dict) -> Dict:
        """Create personalized plan overview"""
        
        # Generate personalized plan name
        focus_names = {
            "fat_loss": "Fat Loss & Body Recomposition",
            "muscle_building": "Muscle Building & Strength",
            "endurance": "Cardiovascular Fitness & Endurance", 
            "general_fitness": "Complete Fitness Transformation"
        }
        
        plan_name = f"{params['experience_level'].title()} {focus_names[params['primary_focus']]}"
        
        # Create personalized description
        description = f"""
        Your personalized {params['days_per_week']}-day per week program designed specifically for your goals, 
        schedule, and equipment availability. Each workout is designed to be completed in approximately 
        {params['session_minutes']} minutes.
        
        This plan addresses your primary goal while building a strong foundation of movement patterns,
        strength, and cardiovascular health. The program is designed to evolve with you as you get stronger.
        """
        
        return {
            "plan_name": plan_name,
            "description": description.strip(),
            "duration": params.get("plan_duration", "4 Weeks"),
            "focus": params["primary_focus"],
            "experience_level": params["experience_level"]
        }
    
    def _create_weekly_plan(self, week_num: int, params: Dict) -> Dict:
        """Create a detailed plan for a specific week with progression"""
        
        # Get base structure and exercises
        schedule_data = self._create_weekly_schedule(params)
        structure = schedule_data["weekly_structure"]
        exercises = self._create_exercise_library(params)
        
        # Define progression variables based on week
        # Week 1: Base volume
        # Week 2: +1 Set or +Rep
        # Week 3: +Intensity
        # Week 4: Deload or Peak
        
        if week_num == 1:
            sets = 3
            reps = "10-12"
            intensity = "Moderate (RPE 7)"
        elif week_num == 2:
            sets = 3
            reps = "12-15"
            intensity = "Moderate-High (RPE 8)"
        elif week_num == 3:
            sets = 4
            reps = "10-12"
            intensity = "High (RPE 9)"
        else: # Week 4
            sets = 3
            reps = "8-10"
            intensity = "High (RPE 9.5) or Deload"
            
        daily_workouts = {}
        
        for day, focus in structure.items():
            workout_details = {
                "focus": focus,
                "exercises": []
            }
            
            # Select exercises based on focus
            selected_exercises = []
            if "Full Body" in focus:
                selected_exercises.extend(exercises.get("squat", [])[:1])
                selected_exercises.extend(exercises.get("push", [])[:1])
                selected_exercises.extend(exercises.get("pull", [])[:1])
                selected_exercises.extend(exercises.get("lunge", [])[:1])
                selected_exercises.extend(exercises.get("core", [])[:1])
            elif "Upper" in focus or "Push" in focus:
                selected_exercises.extend(exercises.get("push", [])[:2])
                selected_exercises.extend(exercises.get("pull", [])[:1]) # Balance
            elif "Lower" in focus or "Legs" in focus:
                selected_exercises.extend(exercises.get("squat", [])[:2])
                selected_exercises.extend(exercises.get("lunge", [])[:2])
            elif "Pull" in focus:
                selected_exercises.extend(exercises.get("pull", [])[:3])
            
            # Fallback if empty
            if not selected_exercises:
                 selected_exercises.extend(exercises.get("cardio", [])[:2])

            for ex in selected_exercises:
                workout_details["exercises"].append({
                    "name": ex,
                    "sets": sets,
                    "reps": reps,
                    "rest": "60s",
                    "notes": intensity
                })
                
            daily_workouts[day] = workout_details
            
        return {
            "week_number": week_num,
            "focus": f"Week {week_num} Progression",
            "schedule": daily_workouts,
            "weekly_goal": f"Complete all {len(structure)} workouts with {intensity} intensity"
        }

    def _create_weekly_schedule(self, params: Dict) -> Dict:
        """Create weekly workout schedule"""
        
        days = params["days_per_week"]
        experience = params["experience_level"]
        
        if days <= 3:
            # Full body workouts
            if experience == "beginner":
                schedule = {
                    "Monday": "Full Body Foundation",
                    "Wednesday": "Full Body Strength", 
                    "Friday": "Full Body Power" if days == 3 else None
                }
            else:
                schedule = {
                    "Monday": "Full Body Push Focus",
                    "Wednesday": "Full Body Pull Focus",
                    "Friday": "Full Body Legs Focus" if days == 3 else None
                }
        elif days == 4:
            # Upper/Lower split
            schedule = {
                "Monday": "Upper Body Strength",
                "Tuesday": "Lower Body Power",
                "Thursday": "Upper Body Hypertrophy", 
                "Friday": "Lower Body Strength"
            }
        else:
            # Push/Pull/Legs split
            schedule = {
                "Monday": "Push (Chest, Shoulders, Triceps)",
                "Tuesday": "Pull (Back, Biceps)",
                "Wednesday": "Legs (Quads, Glutes, Hamstrings)",
                "Thursday": "Push (Volume Focus)",
                "Friday": "Pull (Strength Focus)",
                "Saturday": "Legs (Power Focus)" if days == 6 else None
            }
            
        # Remove None values
        schedule = {k: v for k, v in schedule.items() if v is not None}
        
        return {
            "weekly_structure": schedule,
            "rest_days": "Take at least 1-2 complete rest days per week",
            "active_recovery": "Light walking, stretching, or yoga on rest days"
        }
    
    def _create_exercise_library(self, params: Dict) -> Dict:
        """Create equipment-appropriate exercise library"""
        
        equipment = params["equipment_level"]
        experience = params["experience_level"]
        injuries = params["injuries"]
        
        # Base exercise library by equipment level
        if equipment == "bodyweight":
            exercises = {
                "push": ["Push-ups", "Pike Push-ups", "Tricep Dips", "Wall Push-ups"],
                "pull": ["Superman", "Reverse Snow Angels", "Door Frame Rows"],
                "squat": ["Bodyweight Squats", "Jump Squats", "Single Leg Squats"],
                "lunge": ["Forward Lunges", "Reverse Lunges", "Lateral Lunges"],
                "core": ["Planks", "Side Planks", "Mountain Climbers", "Dead Bug"],
                "cardio": ["Jumping Jacks", "High Knees", "Burpees", "Step-ups"]
            }
        elif equipment == "home_basic":
            exercises = {
                "push": ["Dumbbell Press", "Overhead Press", "Push-ups", "Chest Flyes"],
                "pull": ["Dumbbell Rows", "Reverse Flyes", "Band Pull-aparts"],
                "squat": ["Goblet Squats", "Dumbbell Squats", "Jump Squats"],
                "lunge": ["Dumbbell Lunges", "Bulgarian Split Squats", "Step-ups"],
                "core": ["Russian Twists", "Weighted Planks", "Dumbbell Deadbugs"],
                "cardio": ["Dumbbell Thrusters", "Renegade Rows", "Mountain Climbers"]
            }
        else:  # Full gym
            exercises = {
                "push": ["Bench Press", "Overhead Press", "Dips", "Push-ups"],
                "pull": ["Pull-ups", "Rows", "Lat Pulldowns", "Face Pulls"],
                "squat": ["Back Squats", "Front Squats", "Goblet Squats"],
                "lunge": ["Walking Lunges", "Bulgarian Split Squats", "Step-ups"],
                "core": ["Planks", "Hanging Leg Raises", "Cable Crunches"],
                "cardio": ["Treadmill", "Rowing Machine", "Bike", "Elliptical"]
            }
        
        # Modify for injuries
        if "Lower back issues" in injuries:
            # Remove/modify exercises that stress the lower back
            if "Back Squats" in exercises.get("squat", []):
                exercises["squat"] = ["Goblet Squats", "Front Squats", "Wall Sits"]
                
        if "Knee problems" in injuries:
            # Modify high-impact exercises
            exercises["cardio"] = [ex for ex in exercises.get("cardio", []) if "Jump" not in ex]
            
        # Adjust for experience level
        if experience == "beginner":
            # Start with easier variations
            for category in exercises:
                exercises[category] = exercises[category][:2]  # Limit options for simplicity
                
        return exercises
    
    def _create_progression_rules(self, params: Dict) -> Dict:
        """Create clear progression guidelines"""
        
        experience = params["experience_level"]
        
        if experience == "beginner":
            rules = {
                "weeks_1_4": {
                    "focus": "Master perfect form and build consistency",
                    "progression": "Only increase reps when you can complete all sets with perfect form",
                    "rep_ranges": "8-12 reps for strength exercises, 15-30 seconds for planks",
                    "rest_periods": "60-90 seconds between sets"
                },
                "weeks_5_8": {
                    "focus": "Gradual intensity increase",
                    "progression": "Add weight in smallest increments (1-2kg) or increase reps by 1-2",
                    "rep_ranges": "10-15 reps for strength exercises",
                    "rest_periods": "60-90 seconds between sets"
                },
                "weeks_9_12": {
                    "focus": "Consistent challenge and variety",
                    "progression": "Continue adding weight/reps, introduce exercise variations",
                    "rep_ranges": "8-15 reps depending on exercise",
                    "rest_periods": "90-120 seconds for compound movements"
                }
            }
        else:
            rules = {
                "general": {
                    "strength_focus": "3-6 reps with heavier weight",
                    "hypertrophy_focus": "8-12 reps with moderate weight", 
                    "endurance_focus": "15+ reps with lighter weight",
                    "progression": "Increase weight by 2.5-5kg when you can complete all sets at top of rep range"
                }
            }
            
        return rules
    
    def _create_nutrition_guidelines(self, params: Dict) -> Dict:
        """Create basic nutrition guidelines based on goals"""
        
        focus = params["primary_focus"]
        
        if focus == "fat_loss":
            guidelines = {
                "calorie_approach": "Moderate calorie deficit (300-500 calories below maintenance)",
                "protein": "1.8-2.4g per kg body weight to preserve muscle",
                "carbs": "Time around workouts for energy",
                "fats": "0.8-1.2g per kg body weight for hormone production",
                "hydration": "35ml per kg body weight daily",
                "meal_timing": "Eat protein at every meal, don't skip meals"
            }
        elif focus == "muscle_building":
            guidelines = {
                "calorie_approach": "Slight calorie surplus (200-500 calories above maintenance)",
                "protein": "1.6-2.2g per kg body weight for muscle growth",
                "carbs": "4-6g per kg body weight for workout fuel",
                "fats": "1.0-1.5g per kg body weight",
                "hydration": "40ml per kg body weight daily",
                "meal_timing": "Protein within 2 hours post-workout"
            }
        else:
            guidelines = {
                "calorie_approach": "Eat to maintain energy for workouts",
                "protein": "1.4-1.8g per kg body weight",
                "carbs": "Focus on whole grains and fruits",
                "fats": "Include healthy fats daily",
                "hydration": "35ml per kg body weight daily",
                "meal_timing": "Regular meals to maintain energy"
            }
            
        return guidelines
    
    def _create_success_metrics(self, params: Dict) -> Dict:
        """Define how to measure success"""
        
        focus = params["primary_focus"]
        
        metrics = {
            "primary_metrics": [],
            "secondary_metrics": [],
            "tracking_frequency": "Weekly"
        }
        
        if focus == "fat_loss":
            metrics["primary_metrics"] = ["Body measurements (waist, hips)", "Progress photos", "How clothes fit"]
            metrics["secondary_metrics"] = ["Weight (weekly average)", "Energy levels", "Workout performance"]
        elif focus == "muscle_building":
            metrics["primary_metrics"] = ["Strength increases", "Progress photos", "Body measurements"]
            metrics["secondary_metrics"] = ["Weight gain", "Workout volume", "Recovery quality"]
        elif focus == "endurance":
            metrics["primary_metrics"] = ["Cardio performance", "Resting heart rate", "Energy levels"]
            metrics["secondary_metrics"] = ["Workout completion time", "Recovery between sets"]
        else:
            metrics["primary_metrics"] = ["Overall energy", "Strength improvements", "Consistency"]
            metrics["secondary_metrics"] = ["Sleep quality", "Mood", "Daily activity tolerance"]
            
        return metrics

def advanced_workout_planner_ui():
    """Advanced workout planner with comprehensive questionnaire"""
    
    # Add custom CSS for better readability
    st.markdown("""
    <style>
        /* Improve selectbox and multiselect readability */
        .stSelectbox label, .stMultiSelect label {
            color: #FFFFFF !important;
            font-weight: 500 !important;
            font-size: 1rem !important;
        }
        
        /* Selectbox dropdown options */
        .stSelectbox div[data-baseweb="select"] > div {
            background-color: #1E1E1E !important;
            color: #FFFFFF !important;
        }
        
        /* Dropdown menu items */
        [data-baseweb="menu"] {
            background-color: #2D2D2D !important;
        }
        
        [data-baseweb="menu"] li {
            color: #FFFFFF !important;
            background-color: #2D2D2D !important;
        }
        
        [data-baseweb="menu"] li:hover {
            background-color: #3D3D3D !important;
            color: #00D9FF !important;
        }
        
        /* Selected option in dropdown */
        .stSelectbox div[data-baseweb="select"] span {
            color: #FFFFFF !important;
        }
        
        /* Multiselect options */
        .stMultiSelect div[data-baseweb="select"] > div {
            background-color: #1E1E1E !important;
            color: #FFFFFF !important;
        }
        
        .stMultiSelect span {
            color: #FFFFFF !important;
        }
        
        /* Text input and text area */
        .stTextInput input, .stTextArea textarea {
            color: #FFFFFF !important;
            background-color: #1E1E1E !important;
        }
        
        /* Number input */
        .stNumberInput input {
            color: #FFFFFF !important;
            background-color: #1E1E1E !important;
        }
        
        /* Slider labels and values */
        .stSlider label, .stSlider div {
            color: #FFFFFF !important;
        }
        
        /* Question text */
        h3, h4 {
            color: #FFFFFF !important;
        }
        
        /* Make sure all paragraph text is readable */
        p, span, div {
            color: #E0E0E0 !important;
        }
        
        /* Caption text */
        .caption {
            color: #B0B0B0 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🎯 Smart Workout Planner")
    st.markdown("*World-class personalized training plans based on 15 foundational questions*")
    st.markdown("*Answer 15 expert-designed questions to get a workout plan tailored specifically to your goals, schedule, and fitness level*")
    
    # Show benefits
    with st.expander("🎆 What makes this planner special?"):
        st.markdown("""
        **Based on 15 Years of Personal Training Experience:**
        
        ✅ **Truly Personalized**: Not just your fitness level, but your schedule, equipment, injuries, and past obstacles
        
        ✅ **Goal-Specific**: Whether you want to lose fat, build muscle, or improve endurance - your plan is designed for YOUR outcome
        
        ✅ **Realistic & Sustainable**: Built around your actual life, not some perfect scenario
        
        ✅ **Progressive**: Clear rules on how to advance safely and effectively
        
        ✅ **Complete**: Includes exercise selection, nutrition guidelines, and success tracking
        
        **This isn't a generic template - it's a custom plan designed by analyzing your unique situation.**
        """)
    
    # Initialize session state
    if "questionnaire_step" not in st.session_state:
        st.session_state.questionnaire_step = 0
    if "user_responses" not in st.session_state:
        st.session_state.user_responses = {}
    if "workout_plan" not in st.session_state:
        st.session_state.workout_plan = None
        
    # Initialize recommendation engine
    engine = WorkoutRecommendationEngine()
    foundational_questions = engine.get_foundational_questions()
    architectural_questions = engine.get_architectural_questions()
    all_questions = foundational_questions + architectural_questions
    
    # Progress bar
    progress = st.session_state.questionnaire_step / len(all_questions)
    st.progress(progress)
    
    # Progress info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption(f"Question {st.session_state.questionnaire_step + 1} of {len(all_questions)}")
    with col2:
        st.caption(f"Progress: {int(progress * 100)}%")
    with col3:
        if st.session_state.questionnaire_step <= 10:
            st.caption("📝 Foundational Questions")
        else:
            st.caption("🏧 Plan Architecture")
    
    # Show current question or results
    if st.session_state.questionnaire_step < len(all_questions):
        current_question = all_questions[st.session_state.questionnaire_step]
        
        # Display question
        st.subheader(f"Question {st.session_state.questionnaire_step + 1}")
        st.markdown(f"**{current_question['question']}**")
        
        # Show why this question matters
        with st.expander("💡 Why this question matters"):
            st.info(current_question['why'])
        
        # Handle different question types
        response = None
        
        if current_question['type'] == 'selectbox':
            response = st.selectbox("Select your answer:", current_question['options'])
            
        elif current_question['type'] == 'multiselect':
            response = st.multiselect("Select all that apply:", current_question['options'])
            
        elif current_question['type'] == 'slider':
            min_val, max_val = current_question['range']
            labels = current_question.get('labels', {})
            response = st.slider(
                "Rate from 1-10:", 
                min_val, max_val, 
                help=f"{labels.get(str(min_val), '')} ... {labels.get(str(max_val), '')}"
            )
            
        elif current_question['type'] == 'form':
            st.markdown("**Please provide the following information:**")
            response = {}
            
            for field_name, field_config in current_question['fields'].items():
                if field_config['type'] == 'number':
                    response[field_name] = st.number_input(
                        field_name.replace('_', ' ').title(),
                        min_value=field_config.get('min', 0),
                        max_value=field_config.get('max', 1000)
                    )
                elif field_config['type'] == 'selectbox':
                    response[field_name] = st.selectbox(
                        field_name.replace('_', ' ').title(),
                        field_config['options']
                    )
                elif field_config['type'] == 'slider':
                    response[field_name] = st.slider(
                        field_config.get('label', field_name.replace('_', ' ').title()),
                        field_config['min'], 
                        field_config['max'],
                        help="1 = Never tried, 5 = Very confident"
                    )
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.session_state.questionnaire_step > 0:
                if st.button("← Previous", key="prev_workout"):
                    st.session_state.questionnaire_step -= 1
                    st.rerun()
        
        with col2:
            if st.button("Skip Question", key="skip_workout"):
                st.session_state.questionnaire_step += 1
                st.rerun()
                
        with col3:
            if st.button("Next →", type="primary", key="next_workout"):
                # Save response
                st.session_state.user_responses[current_question['id']] = response
                st.session_state.questionnaire_step += 1
                st.rerun()
                
    else:
        # Generate and display workout plan
        if st.session_state.workout_plan is None:
            with st.spinner("🧠 Analyzing your responses and creating your personalized plan..."):
                # Show what's happening
                status_placeholder = st.empty()
                status_placeholder.info("🔍 Analyzing your goals and constraints...")
                
                generator = PersonalizedWorkoutGenerator(st.session_state.user_responses)
                
                status_placeholder.info("🏧 Designing your weekly structure...")
                st.session_state.workout_plan = generator.generate_plan()
                
                # Save to MongoDB if user is logged in
                if st.session_state.get('authenticated') and st.session_state.get('user'):
                    try:
                        from auth_system import FitnessDatabase
                        db = FitnessDatabase()
                        if db.save_workout_plan(st.session_state.user['user_id'], st.session_state.workout_plan):
                            status_placeholder.success("✅ Your personalized plan is ready and saved!")
                        else:
                            status_placeholder.success("✅ Your personalized plan is ready!")
                    except Exception as e:
                        print(f"Error saving workout plan: {e}")
                        status_placeholder.success("✅ Your personalized plan is ready!")
                else:
                    status_placeholder.success("✅ Your personalized plan is ready!")
                
                time.sleep(1)
                status_placeholder.empty()
        
        # Display the generated plan
        display_workout_plan(st.session_state.workout_plan)
        
        # Save plan
        if st.button("💾 Save Plan", key="save_workout_plan"):
            st.success("Plan saved!")
        
        # Reset button
        if st.button("🔄 Start Over", key="reset_workout"):
            st.session_state.questionnaire_step = 0
            st.session_state.user_responses = {}
            st.session_state.workout_plan = None
            st.rerun()

def generate_pdf_plan(plan: Dict) -> bytes:
    """Generate a PDF version of the workout plan"""
    
    if not PDF_AVAILABLE:
        # Fallback to text-based PDF simulation
        return generate_document_plan(plan).encode('utf-8')
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.darkblue,
        alignment=1  # Center alignment
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        textColor=colors.darkgreen
    )
    
    # Build PDF content
    story = []
    
    # Title
    overview = plan['plan_overview']
    story.append(Paragraph(overview['plan_name'], title_style))
    story.append(Spacer(1, 12))
    
    # Overview
    story.append(Paragraph("Plan Overview", heading_style))
    story.append(Paragraph(overview['description'], styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Plan details table
    plan_data = [
        ['Duration', overview['duration']],
        ['Focus', overview['focus'].replace('_', ' ').title()],
        ['Level', overview['experience_level'].title()]
    ]
    
    plan_table = Table(plan_data, colWidths=[2*inch, 4*inch])
    plan_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(plan_table)
    story.append(Spacer(1, 20))
    
    # Weekly Schedule
    story.append(Paragraph("Weekly Schedule", heading_style))
    schedule = plan['weekly_schedule']
    
    schedule_data = [['Day', 'Workout']]
    for day, workout in schedule['weekly_structure'].items():
        schedule_data.append([day, workout])
    
    schedule_table = Table(schedule_data, colWidths=[1.5*inch, 4.5*inch])
    schedule_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(schedule_table)
    story.append(Spacer(1, 12))
    
    story.append(Paragraph(f"<b>Rest Days:</b> {schedule['rest_days']}", styles['Normal']))
    story.append(Paragraph(f"<b>Active Recovery:</b> {schedule['active_recovery']}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Exercise Library
    story.append(Paragraph("Exercise Library", heading_style))
    exercises = plan['exercise_library']
    
    for category, exercise_list in exercises.items():
        story.append(Paragraph(f"<b>{category.title()} Exercises:</b>", styles['Normal']))
        for exercise in exercise_list:
            story.append(Paragraph(f"• {exercise}", styles['Normal']))
        story.append(Spacer(1, 8))
    
    story.append(Spacer(1, 20))
    
    # Progression Rules
    story.append(Paragraph("Progression Guidelines", heading_style))
    progression = plan['progression_rules']
    
    for phase, rules in progression.items():
        story.append(Paragraph(f"<b>{phase.replace('_', ' ').title()}:</b>", styles['Normal']))
        for rule_type, rule_text in rules.items():
            story.append(Paragraph(f"• <b>{rule_type.replace('_', ' ').title()}:</b> {rule_text}", styles['Normal']))
        story.append(Spacer(1, 8))
    
    story.append(Spacer(1, 20))
    
    # Nutrition Guidelines
    story.append(Paragraph("Nutrition Guidelines", heading_style))
    nutrition = plan['nutrition_guidelines']
    
    for guideline, details in nutrition.items():
        story.append(Paragraph(f"• <b>{guideline.replace('_', ' ').title()}:</b> {details}", styles['Normal']))
    
    story.append(Spacer(1, 20))
    
    # Success Metrics
    story.append(Paragraph("Success Tracking", heading_style))
    metrics = plan['success_metrics']
    
    story.append(Paragraph("<b>Primary Metrics:</b>", styles['Normal']))
    for metric in metrics['primary_metrics']:
        story.append(Paragraph(f"• {metric}", styles['Normal']))
    
    story.append(Paragraph("<b>Secondary Metrics:</b>", styles['Normal']))
    for metric in metrics['secondary_metrics']:
        story.append(Paragraph(f"• {metric}", styles['Normal']))
    
    story.append(Paragraph(f"<b>Tracking Frequency:</b> {metrics['tracking_frequency']}", styles['Normal']))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

def generate_document_plan(plan: Dict) -> str:
    """Generate a text document version of the workout plan"""
    
    overview = plan['plan_overview']
    schedule = plan['weekly_schedule']
    exercises = plan['exercise_library']
    progression = plan['progression_rules']
    nutrition = plan['nutrition_guidelines']
    metrics = plan['success_metrics']
    
    doc_content = f"""
═══════════════════════════════════════════════════════════════
                    {overview['plan_name'].upper()}
═══════════════════════════════════════════════════════════════

Generated on: {datetime.now().strftime('%B %d, %Y')}

📋 PLAN OVERVIEW
{"="*50}
{overview['description']}

• Duration: {overview['duration']}
• Focus: {overview['focus'].replace('_', ' ').title()}
• Experience Level: {overview['experience_level'].title()}

📅 WEEKLY SCHEDULE
{"="*50}
"""
    
    for day, workout in schedule['weekly_structure'].items():
        doc_content += f"• {day}: {workout}\n"
    
    doc_content += f"""

🛌 REST & RECOVERY
• Rest Days: {schedule['rest_days']}
• Active Recovery: {schedule['active_recovery']}

💪 EXERCISE LIBRARY
{"="*50}
"""
    
    for category, exercise_list in exercises.items():
        doc_content += f"\n{category.upper()} EXERCISES:\n"
        for exercise in exercise_list:
            doc_content += f"  • {exercise}\n"
    
    doc_content += f"""

📈 PROGRESSION GUIDELINES
{"="*50}
"""
    
    for phase, rules in progression.items():
        doc_content += f"\n{phase.replace('_', ' ').upper()}:\n"
        for rule_type, rule_text in rules.items():
            doc_content += f"  • {rule_type.replace('_', ' ').title()}: {rule_text}\n"
    
    doc_content += f"""

🥗 NUTRITION GUIDELINES
{"="*50}
"""
    
    for guideline, details in nutrition.items():
        doc_content += f"• {guideline.replace('_', ' ').title()}: {details}\n"
    
    doc_content += f"""

📊 SUCCESS TRACKING
{"="*50}

PRIMARY METRICS:
"""
    
    for metric in metrics['primary_metrics']:
        doc_content += f"  • {metric}\n"
    
    doc_content += "\nSECONDARY METRICS:\n"
    for metric in metrics['secondary_metrics']:
        doc_content += f"  • {metric}\n"
    
    doc_content += f"\nTracking Frequency: {metrics['tracking_frequency']}\n"
    
    doc_content += f"""

═══════════════════════════════════════════════════════════════
                        IMPORTANT NOTES
═══════════════════════════════════════════════════════════════

🔥 CONSISTENCY IS KEY
The most perfect plan is useless without consistency. Show up, 
do the work, and trust the process.

⚠️ SAFETY FIRST
Always prioritize proper form over weight or speed. If something 
hurts (not muscle fatigue), stop and reassess.

📞 WHEN TO SEEK HELP
Consider working with a qualified trainer if you're unsure about 
exercise form or need additional guidance.

🎯 STAY FOCUSED
This plan is designed specifically for your goals and situation. 
Stick to it for at least 4-6 weeks before making major changes.

═══════════════════════════════════════════════════════════════
                    YOUR FITNESS JOURNEY STARTS NOW!
═══════════════════════════════════════════════════════════════
"""
    
    return doc_content

def display_workout_plan(plan: Dict):
    """Display the generated workout plan"""
    
    st.success("🎉 Your personalized workout plan is ready!")
    
    # Plan Overview
    overview = plan['plan_overview']
    st.header(overview['plan_name'])
    st.markdown(overview['description'])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Duration", overview['duration'])
    with col2:
        st.metric("Focus", overview['focus'].replace('_', ' ').title())
    with col3:
        st.metric("Level", overview['experience_level'].title())
    
    # Weekly Schedule
    st.subheader("📅 Your Weekly Schedule")
    
    if "weekly_plans" in plan:
        tabs = st.tabs(list(plan["weekly_plans"].keys()))
        for i, (week_name, week_data) in enumerate(plan["weekly_plans"].items()):
            with tabs[i]:
                st.markdown(f"### {week_data['focus']}")
                st.markdown(f"**Goal:** {week_data['weekly_goal']}")
                
                for day, details in week_data['schedule'].items():
                    with st.expander(f"{day}: {details['focus']}", expanded=True):
                        for ex in details['exercises']:
                            col1, col2, col3, col4 = st.columns([3, 1, 1, 2])
                            col1.markdown(f"**{ex['name']}**")
                            col2.markdown(f"{ex['sets']} sets")
                            col3.markdown(f"{ex['reps']} reps")
                            col4.markdown(f"_{ex['notes']}_")
    else:
        schedule = plan['weekly_schedule']
        
        for day, workout in schedule['weekly_structure'].items():
            st.markdown(f"**{day}**: {workout}")
        
        st.info(f"**Rest Days**: {schedule['rest_days']}")
        st.info(f"**Active Recovery**: {schedule['active_recovery']}")
    
    # Exercise Library
    st.subheader("💪 Your Exercise Library")
    exercises = plan['exercise_library']
    
    for category, exercise_list in exercises.items():
        with st.expander(f"{category.title()} Exercises"):
            for exercise in exercise_list:
                st.markdown(f"• {exercise}")
    
    # Progression Rules
    st.subheader("📈 How to Progress")
    progression = plan['progression_rules']
    
    for phase, rules in progression.items():
        with st.expander(f"{phase.replace('_', ' ').title()}"):
            for rule_type, rule_text in rules.items():
                st.markdown(f"**{rule_type.replace('_', ' ').title()}**: {rule_text}")
    
    # Nutrition Guidelines
    st.subheader("🥗 Nutrition Guidelines")
    nutrition = plan['nutrition_guidelines']
    
    for guideline, details in nutrition.items():
        st.markdown(f"**{guideline.replace('_', ' ').title()}**: {details}")
    
    # Success Metrics
    st.subheader("📊 How to Track Success")
    metrics = plan['success_metrics']
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Primary Metrics:**")
        for metric in metrics['primary_metrics']:
            st.markdown(f"• {metric}")
    
    with col2:
        st.markdown("**Secondary Metrics:**")
        for metric in metrics['secondary_metrics']:
            st.markdown(f"• {metric}")
    
    st.info(f"**Tracking Frequency**: {metrics['tracking_frequency']}")
    
    # Additional tips
    st.markdown("---")
    st.subheader("💡 Success Tips")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Consistency Beats Perfection**
        - Show up even when you don't feel like it
        - 80% effort consistently beats 100% effort sporadically
        - Focus on building the habit first
        """)
    
    with col2:
        st.markdown("""
        **Listen to Your Body**
        - Muscle fatigue is normal, pain is not
        - Take extra rest if you're feeling run down
        - Progress isn't always linear
        """)
    
    st.warning("⚠️ **Important**: This plan is for educational purposes. Consult with a healthcare provider before starting any new exercise program, especially if you have medical conditions.")
    
    # Download options
    st.subheader("📥 Download Your Plan")
    st.caption("Save your personalized workout plan in your preferred format")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Download as PDF", type="primary"):
            if PDF_AVAILABLE:
                pdf_content = generate_pdf_plan(plan)
                st.download_button(
                    label="📄 Get PDF",
                    data=pdf_content,
                    file_name=f"workout_plan_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )
            else:
                st.error("🚨 PDF generation requires reportlab library. Install with: pip install reportlab")
                st.info("💡 Use the Document option as an alternative.")
    
    with col2:
        if st.button("📝 Download as Document"):
            doc_content = generate_document_plan(plan)
            st.download_button(
                label="📝 Get Document",
                data=doc_content,
                file_name=f"workout_plan_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
            st.success("✅ Text document ready for download!")
    
    with col3:
        if st.button("🔧 Download as JSON"):
            plan_json = json.dumps(plan, indent=2)
            st.download_button(
                label="🔧 Get JSON",
                data=plan_json,
                file_name=f"workout_plan_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
            st.success("✅ JSON file ready for download!")
    
    # Installation help
    with st.expander("🛠️ Need help with PDF downloads?"):
        st.markdown("""
        **To enable PDF downloads, install the required library:**
        ```bash
        pip install reportlab
        ```
        
        **Alternative formats:**
        - **Document (.txt)**: Plain text format, works everywhere
        - **JSON (.json)**: Structured data format for developers
        """)

if __name__ == "__main__":
    advanced_workout_planner_ui()