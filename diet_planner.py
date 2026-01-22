#!/usr/bin/env python3

import streamlit as st
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
import time
import random
import math

class DietRecommendationEngine:
    """Advanced diet recommendation system based on 15 essential questions"""
    
    def __init__(self):
        self.questions = self._get_essential_questions()
        
    def _get_essential_questions(self) -> List[Dict]:
        """The 15 essential questions for legendary nutrition planning"""
        return [
            # Section 1: Foundation & Core Objectives
            {
                "id": "primary_outcome",
                "section": "Foundation & Core Objectives",
                "question": "Beyond a number on the scale, what is the single most important health or performance goal you want to achieve with your nutrition in the next 3 months?",
                "type": "selectbox",
                "options": [
                    "I want to have stable energy all day",
                    "I want to reduce bloating and digestive issues", 
                    "I need to fuel my workouts to build muscle",
                    "I need to manage my blood sugar",
                    "I want to improve my athletic performance",
                    "I want to lose body fat while maintaining muscle",
                    "I want to improve my overall health markers",
                    "I want to have better mental clarity and focus"
                ],
                "why": "This defines our target. Fueling for athletic performance is vastly different from eating to improve digestive health."
            },
            {
                "id": "quantitative_baseline",
                "section": "Foundation & Core Objectives", 
                "question": "Please provide your current physical measurements",
                "type": "form",
                "fields": {
                    "height_cm": {"type": "number", "min": 140, "max": 220, "label": "Height (cm)"},
                    "weight_kg": {"type": "number", "min": 40, "max": 200, "label": "Weight (kg)"},
                    "age": {"type": "number", "min": 16, "max": 80, "label": "Age"},
                    "biological_sex": {"type": "selectbox", "options": ["Male", "Female"], "label": "Biological Sex"},
                    "body_fat_percentage": {"type": "number", "min": 5, "max": 50, "label": "Body Fat % (if known, optional)"}
                },
                "why": "These are non-negotiable data points for calculating your baseline metabolic rate."
            },
            {
                "id": "medical_conditions",
                "section": "Foundation & Core Objectives",
                "question": "Do you have any diagnosed medical conditions, food allergies, intolerances, or are you taking medications?",
                "type": "multiselect",
                "options": [
                    "None",
                    "Diabetes (Type 1 or 2)",
                    "PCOS",
                    "IBS or digestive issues", 
                    "Thyroid issues",
                    "High cholesterol",
                    "Lactose intolerance",
                    "Gluten sensitivity/Celiac",
                    "Food allergies (nuts, shellfish, etc.)",
                    "Currently pregnant",
                    "Currently breastfeeding",
                    "Taking medications regularly",
                    "Taking supplements regularly"
                ],
                "why": "Most critical question for safety. Medical conditions require specific nutritional protocols."
            },
            
            # Section 2: Current Nutritional Landscape
            {
                "id": "typical_day_eating",
                "section": "Current Nutritional Landscape",
                "question": "Describe a completely typical day of eating and drinking from wake up to bedtime",
                "type": "text_area",
                "placeholder": "Example: 7am - Coffee with milk, 9am - Oatmeal with banana, 12pm - Sandwich and chips, 3pm - Snack, 7pm - Dinner, etc.",
                "why": "Provides honest snapshot of current habits, portion sizes, and meal timing."
            },
            {
                "id": "hunger_energy_patterns",
                "section": "Current Nutritional Landscape",
                "question": "When do you feel most hungry, when are your energy levels highest/lowest, and what do you crave?",
                "type": "form",
                "fields": {
                    "most_hungry_time": {"type": "selectbox", "options": ["Morning", "Mid-morning", "Lunch time", "Afternoon", "Evening", "Late night"], "label": "Most hungry time"},
                    "highest_energy": {"type": "selectbox", "options": ["Early morning", "Mid-morning", "Afternoon", "Evening", "Varies"], "label": "Highest energy time"},
                    "energy_crash_time": {"type": "selectbox", "options": ["No crashes", "Mid-morning", "After lunch", "Afternoon", "Evening"], "label": "Energy crash time"},
                    "common_cravings": {"type": "multiselect", "options": ["Sweet foods", "Salty snacks", "Carbs/bread", "Chocolate", "Caffeine", "None specific"], "label": "Common cravings"}
                },
                "why": "Helps architect meal timing and macronutrient balance to prevent crashes and manage cravings."
            },
            {
                "id": "hydration_status",
                "section": "Current Nutritional Landscape",
                "question": "How much water do you drink daily and what other beverages do you consume?",
                "type": "form",
                "fields": {
                    "water_glasses": {"type": "slider", "min": 0, "max": 15, "label": "Glasses of water per day"},
                    "coffee_cups": {"type": "slider", "min": 0, "max": 10, "label": "Cups of coffee per day"},
                    "tea_cups": {"type": "slider", "min": 0, "max": 10, "label": "Cups of tea per day"},
                    "alcohol_weekly": {"type": "slider", "min": 0, "max": 20, "label": "Alcoholic drinks per week"},
                    "soda_daily": {"type": "slider", "min": 0, "max": 5, "label": "Sodas/juices per day"}
                },
                "why": "Dehydration is often mistaken for hunger and impacts energy dramatically."
            },
            
            # Section 3: Lifestyle & Practical Realities
            {
                "id": "cooking_reality",
                "section": "Lifestyle & Practical Realities",
                "question": "What is your cooking skill level and how much time can you dedicate to food preparation?",
                "type": "form",
                "fields": {
                    "cooking_skill": {"type": "slider", "min": 1, "max": 10, "label": "Cooking skill (1=beginner, 10=expert)"},
                    "cooking_enjoyment": {"type": "slider", "min": 1, "max": 10, "label": "Cooking enjoyment (1=hate it, 10=love it)"},
                    "prep_time_daily": {"type": "selectbox", "options": ["Less than 15 minutes", "15-30 minutes", "30-60 minutes", "1-2 hours", "2+ hours"], "label": "Daily food prep time available"}
                },
                "why": "Plan must be practical. Complex recipes are useless for someone who hates cooking."
            },
            {
                "id": "social_cultural_context",
                "section": "Lifestyle & Practical Realities",
                "question": "Describe your social eating patterns and cultural considerations",
                "type": "form",
                "fields": {
                    "eating_situation": {"type": "selectbox", "options": ["Mostly alone", "With family/partner", "Mix of both"], "label": "Typical eating situation"},
                    "restaurant_frequency": {"type": "selectbox", "options": ["Rarely", "1-2 times per week", "3-4 times per week", "5+ times per week"], "label": "Restaurant/takeout frequency"},
                    "social_events": {"type": "selectbox", "options": ["Rarely", "Weekly", "Multiple times per week"], "label": "Social events with food"},
                    "cultural_dietary": {"type": "multiselect", "options": ["None", "Vegetarian", "Vegan", "Halal", "Kosher", "Mediterranean", "Asian cuisine preference", "Other"], "label": "Cultural/religious dietary practices"}
                },
                "why": "Food is deeply social and cultural. Plan must navigate family dinners and personal traditions."
            },
            {
                "id": "financial_framework",
                "section": "Lifestyle & Practical Realities",
                "question": "What is your grocery budget and shopping preferences?",
                "type": "form",
                "fields": {
                    "weekly_budget": {"type": "selectbox", "options": ["Under $50", "$50-100", "$100-150", "$150-200", "$200+"], "label": "Weekly grocery budget"},
                    "shopping_preference": {"type": "multiselect", "options": ["Standard supermarket", "Local farmers market", "Organic/specialty stores", "Online grocery delivery", "Bulk stores"], "label": "Shopping preferences"}
                },
                "why": "Plan must be financially sustainable using available resources."
            },
            {
                "id": "activity_performance",
                "section": "Lifestyle & Practical Realities",
                "question": "Describe your physical activity and lifestyle",
                "type": "form",
                "fields": {
                    "workout_frequency": {"type": "selectbox", "options": ["No regular exercise", "1-2 times per week", "3-4 times per week", "5-6 times per week", "Daily"], "label": "Workout frequency"},
                    "workout_type": {"type": "multiselect", "options": ["Cardio", "Weight training", "Yoga/Pilates", "Sports", "Walking/hiking", "High intensity training"], "label": "Types of exercise"},
                    "workout_duration": {"type": "selectbox", "options": ["Less than 30 min", "30-60 min", "60-90 min", "90+ min"], "label": "Typical workout duration"},
                    "daily_activity": {"type": "selectbox", "options": ["Desk job, mostly sedentary", "Some walking/standing", "Moderately active job", "Very active job"], "label": "Daily activity level"}
                },
                "why": "Links nutrition to fitness plan. Need to calculate energy expenditure for proper fueling."
            },
            
            # Section 4: Psychology of Eating
            {
                "id": "food_relationship",
                "section": "Psychology of Eating",
                "question": "How would you describe your personal relationship with food?",
                "type": "selectbox",
                "options": [
                    "Food is primarily fuel for my body",
                    "Food is a source of comfort and pleasure",
                    "Food is a reward system for me",
                    "Food causes me anxiety and stress",
                    "Food is social connection and culture",
                    "Food is both fuel and enjoyment in balance",
                    "I have a complicated relationship with food"
                ],
                "why": "Uncovers emotional drivers. Plan must foster positive, nourishing relationship with food."
            },
            {
                "id": "diet_history",
                "section": "Psychology of Eating",
                "question": "What previous diets or nutritional approaches have you tried and what happened?",
                "type": "text_area",
                "placeholder": "Describe what you tried, what you liked/disliked, and why you stopped following them",
                "why": "Learn from the past to avoid repeating mistakes and find sustainable approaches."
            },
            
            # Section 5: Preferences & Fine-Tuning
            {
                "id": "food_preferences",
                "section": "Preferences & Fine-Tuning",
                "question": "What healthy foods do you love and what do you absolutely dislike?",
                "type": "form",
                "fields": {
                    "favorite_proteins": {"type": "multiselect", "options": ["Chicken", "Fish", "Eggs", "Greek yogurt", "Beans/legumes", "Tofu", "Lean beef", "Turkey"], "label": "Favorite protein sources"},
                    "favorite_carbs": {"type": "multiselect", "options": ["Rice", "Oats", "Quinoa", "Sweet potatoes", "Fruits", "Whole grain bread", "Pasta"], "label": "Favorite carb sources"},
                    "favorite_vegetables": {"type": "multiselect", "options": ["Leafy greens", "Broccoli", "Bell peppers", "Carrots", "Tomatoes", "Cucumber", "Zucchini"], "label": "Favorite vegetables"},
                    "disliked_foods": {"type": "multiselect", "options": ["Fish", "Eggs", "Dairy", "Spicy foods", "Leafy greens", "Beans", "Nuts", "None"], "label": "Foods you dislike"}
                },
                "why": "Sustainability is built on enjoyment. Build plan around foods you love."
            },
            {
                "id": "meal_structure",
                "section": "Preferences & Fine-Tuning",
                "question": "What meal structure and timing works best for you?",
                "type": "form",
                "fields": {
                    "meal_preference": {"type": "selectbox", "options": ["3 larger meals", "5-6 smaller meals", "2 larger meals + snacks", "Flexible timing"], "label": "Preferred meal structure"},
                    "breakfast_timing": {"type": "selectbox", "options": ["Early (6-7am)", "Mid-morning (8-9am)", "Late morning (10-11am)", "I skip breakfast"], "label": "Breakfast preference"},
                    "largest_meal": {"type": "selectbox", "options": ["Breakfast", "Lunch", "Dinner", "No preference"], "label": "Preferred largest meal"}
                },
                "why": "Tailors schedule to your body's natural hunger cues and preferences."
            },
            {
                "id": "success_definition",
                "section": "Preferences & Fine-Tuning",
                "question": "How will we know this nutrition plan is working for you? What will success look and feel like?",
                "type": "multiselect",
                "options": [
                    "I won't feel bloated after meals",
                    "I'll have stable energy throughout the day",
                    "I'll sleep better at night",
                    "My gym performance will improve",
                    "I'll feel more confident about my body",
                    "My mood will be more stable",
                    "I'll have better mental clarity",
                    "My digestion will improve",
                    "I'll feel stronger and more energetic"
                ],
                "why": "Sets personalized metrics for success beyond just weight loss."
            },
            # Section 6: Advanced Lifestyle Factors (New)
            {
                "id": "sleep_stress",
                "section": "Advanced Lifestyle Factors",
                "question": "How are your sleep and stress levels?",
                "type": "form",
                "fields": {
                    "sleep_hours": {"type": "slider", "min": 4, "max": 12, "label": "Average sleep (hours)"},
                    "sleep_quality": {"type": "selectbox", "options": ["Poor", "Fair", "Good", "Excellent"], "label": "Sleep quality"},
                    "stress_level": {"type": "slider", "min": 1, "max": 10, "label": "Daily stress level (1-10)"},
                    "stress_eating": {"type": "selectbox", "options": ["Never", "Rarely", "Sometimes", "Often"], "label": "Do you stress eat?"}
                },
                "why": "Sleep and stress profoundly impact metabolism and cravings."
            },
            {
                "id": "kitchen_equipment",
                "section": "Advanced Lifestyle Factors",
                "question": "What kitchen equipment do you have access to?",
                "type": "multiselect",
                "options": ["Stove/Oven", "Microwave", "Blender", "Air Fryer", "Slow Cooker", "Instant Pot", "Food Processor", "Grill"],
                "why": "Ensures recipes are actually makeable in your kitchen."
            },
            {
                "id": "cuisine_preference",
                "section": "Preferences & Fine-Tuning",
                "question": "What types of cuisine do you prefer?",
                "type": "multiselect",
                "options": ["Indian", "Western", "Mediterranean", "Asian", "Mexican", "No Preference"],
                "why": "Ensures the meal plan matches your cultural and taste preferences."
            },
            {
                "id": "flavor_profile",
                "section": "Preferences & Fine-Tuning",
                "question": "What are your preferred flavor profiles?",
                "type": "multiselect",
                "options": ["Savory", "Sweet", "Spicy", "Sour/Tangy", "Fresh/Herbal", "Rich/Creamy"],
                "why": "Aligns recipes with your palate for higher adherence."
            },
            {
                "id": "caffeine_habits",
                "section": "Advanced Lifestyle Factors",
                "question": "Describe your caffeine consumption",
                "type": "form",
                "fields": {
                    "caffeine_source": {"type": "multiselect", "options": ["Coffee", "Tea", "Energy Drinks", "Pre-workout", "None"], "label": "Sources"},
                    "cutoff_time": {"type": "selectbox", "options": ["Noon", "2pm", "4pm", "No cutoff"], "label": "Caffeine cutoff time"},
                    "sensitivity": {"type": "selectbox", "options": ["Low", "Normal", "High"], "label": "Sensitivity"}
                },
                "why": "Optimizes energy without disrupting sleep."
            },
            {
                "id": "grocery_habits",
                "section": "Lifestyle & Practical Realities",
                "question": "How do you typically shop for groceries?",
                "type": "form",
                "fields": {
                    "frequency": {"type": "selectbox", "options": ["Daily", "Weekly", "Bi-weekly", "Monthly"], "label": "Shopping frequency"},
                    "bulk_buying": {"type": "checkbox", "label": "I buy in bulk (Costco/Sam's)"},
                    "meal_prep_containers": {"type": "checkbox", "label": "I have meal prep containers"}
                },
                "why": "Tailors the shopping list and prep instructions."
            },
            {
                "id": "motivation_type",
                "section": "Psychology of Eating",
                "question": "What motivates you most?",
                "type": "selectbox",
                "options": ["Visual progress (mirror/photos)", "Data/Numbers (scale/measurements)", "Feeling better/Energy", "Social support/Accountability", "Health markers (bloodwork)"],
                "why": "Customizes the 'Success Tracking' section."
            },
            {
                "id": "cheat_meals",
                "section": "Preferences & Fine-Tuning",
                "question": "How do you want to handle 'treat' meals?",
                "type": "selectbox",
                "options": ["Strict adherence (no treats)", "80/20 rule (flexible)", "Scheduled cheat meal (once a week)", "If it fits my macros"],
                "why": "Sets realistic expectations for flexibility."
            },
            {
                "id": "supplements_willingness",
                "section": "Preferences & Fine-Tuning",
                "question": "Are you open to taking supplements?",
                "type": "selectbox",
                "options": ["Yes, whatever helps", "Only basics (protein/vitamins)", "Prefer whole foods only"],
                "why": "Determines the depth of the supplement protocol."
            },
            {
                "id": "previous_pitfalls",
                "section": "Psychology of Eating",
                "question": "What has caused you to fall off track in the past?",
                "type": "multiselect",
                "options": ["Hunger/Cravings", "Social events", "Lack of time", "Boredom with food", "Too restrictive", "Too expensive", "Lack of results"],
                "why": "Proactively addresses potential failure points."
            },
            {
                "id": "plan_duration",
                "section": "Foundation & Core Objectives",
                "question": "How many weeks of detailed planning do you need?",
                "type": "selectbox",
                "options": ["1 Week", "2 Weeks", "3 Weeks", "4 Weeks"],
                "why": "Determines the scope of the generated roadmap."
            }
        ]

class MLNutritionEngine:
    """Advanced ML-powered nutrition optimization engine with smart personalization"""
    
    def __init__(self):
        # Expanded Recipe Database with Tags and Cuisines
        self.recipe_database = [
            # --- BREAKFAST ---
            # Western
            {"name": "Greek Yogurt Power Bowl", "type": "breakfast", "calories": 320, "protein": 25, "carbs": 35, "fat": 8, "prep_time": 5, "tags": ["vegetarian", "gluten_free", "sweet", "cold", "quick", "western"], "ingredients": ["Greek yogurt", "Mixed Berries", "Granola", "Honey"]},
            {"name": "Spinach & Feta Omelet", "type": "breakfast", "calories": 350, "protein": 22, "carbs": 5, "fat": 25, "prep_time": 10, "tags": ["vegetarian", "keto", "gluten_free", "savory", "hot", "western"], "ingredients": ["Eggs", "Spinach", "Feta Cheese", "Olive Oil"]},
            {"name": "Overnight Oats with Chia", "type": "breakfast", "calories": 380, "protein": 15, "carbs": 55, "fat": 12, "prep_time": 5, "tags": ["vegan", "vegetarian", "gluten_free", "sweet", "cold", "meal_prep", "western"], "ingredients": ["Oats", "Chia Seeds", "Almond Milk", "Maple Syrup"]},
            {"name": "Avocado Toast with Egg", "type": "breakfast", "calories": 400, "protein": 18, "carbs": 35, "fat": 22, "prep_time": 8, "tags": ["vegetarian", "savory", "quick", "western"], "ingredients": ["Whole Grain Bread", "Avocado", "Egg", "Red Pepper Flakes"]},
            {"name": "Protein Pancakes", "type": "breakfast", "calories": 420, "protein": 30, "carbs": 40, "fat": 10, "prep_time": 15, "tags": ["vegetarian", "sweet", "hot", "western"], "ingredients": ["Oat Flour", "Protein Powder", "Egg Whites", "Banana"]},
            {"name": "Smoked Salmon Bagel", "type": "breakfast", "calories": 450, "protein": 25, "carbs": 50, "fat": 15, "prep_time": 5, "tags": ["pescatarian", "savory", "cold", "western"], "ingredients": ["Whole Wheat Bagel", "Smoked Salmon", "Cream Cheese", "Capers"]},
            
            # Indian
            {"name": "Masala Omelet", "type": "breakfast", "calories": 320, "protein": 18, "carbs": 5, "fat": 22, "prep_time": 10, "tags": ["vegetarian", "keto", "gluten_free", "savory", "hot", "spicy", "indian"], "ingredients": ["Eggs", "Onion", "Green Chili", "Coriander", "Turmeric"]},
            {"name": "Paneer Bhurji", "type": "breakfast", "calories": 380, "protein": 22, "carbs": 8, "fat": 28, "prep_time": 15, "tags": ["vegetarian", "keto", "gluten_free", "savory", "hot", "spicy", "indian"], "ingredients": ["Paneer", "Onion", "Tomato", "Spices"]},
            {"name": "Poha with Peanuts", "type": "breakfast", "calories": 350, "protein": 8, "carbs": 55, "fat": 12, "prep_time": 15, "tags": ["vegan", "vegetarian", "gluten_free", "savory", "hot", "indian"], "ingredients": ["Flattened Rice", "Peanuts", "Onion", "Mustard Seeds", "Curry Leaves"]},
            {"name": "Besan Chilla (Gram Flour Pancake)", "type": "breakfast", "calories": 300, "protein": 15, "carbs": 40, "fat": 10, "prep_time": 15, "tags": ["vegan", "vegetarian", "gluten_free", "savory", "hot", "indian"], "ingredients": ["Gram Flour (Besan)", "Onion", "Tomato", "Spices"]},
            {"name": "Upma", "type": "breakfast", "calories": 320, "protein": 8, "carbs": 50, "fat": 10, "prep_time": 15, "tags": ["vegetarian", "savory", "hot", "indian"], "ingredients": ["Semolina", "Vegetables", "Mustard Seeds", "Curry Leaves"]},
            {"name": "Moong Dal Cheela", "type": "breakfast", "calories": 310, "protein": 18, "carbs": 45, "fat": 8, "prep_time": 15, "tags": ["vegan", "vegetarian", "gluten_free", "savory", "hot", "indian"], "ingredients": ["Moong Dal", "Ginger", "Green Chili", "Spices"]},

            # --- LUNCH ---
            # Western
            {"name": "Grilled Chicken Salad", "type": "lunch", "calories": 450, "protein": 40, "carbs": 15, "fat": 25, "prep_time": 15, "tags": ["gluten_free", "keto", "paleo", "savory", "cold", "western"], "ingredients": ["Chicken Breast", "Mixed Greens", "Avocado", "Vinaigrette"]},
            {"name": "Quinoa Power Bowl", "type": "lunch", "calories": 500, "protein": 18, "carbs": 65, "fat": 18, "prep_time": 20, "tags": ["vegan", "vegetarian", "gluten_free", "savory", "meal_prep", "western"], "ingredients": ["Quinoa", "Black Beans", "Corn", "Avocado", "Lime"]},
            {"name": "Turkey & Hummus Wrap", "type": "lunch", "calories": 420, "protein": 30, "carbs": 40, "fat": 15, "prep_time": 5, "tags": ["savory", "cold", "quick", "western"], "ingredients": ["Turkey Slices", "Whole Wheat Wrap", "Hummus", "Cucumber"]},
            {"name": "Tuna Salad Lettuce Wraps", "type": "lunch", "calories": 350, "protein": 30, "carbs": 5, "fat": 22, "prep_time": 10, "tags": ["pescatarian", "keto", "gluten_free", "savory", "cold", "quick", "western"], "ingredients": ["Canned Tuna", "Mayo/Yogurt", "Celery", "Romaine Lettuce"]},
            {"name": "Chicken Burrito Bowl", "type": "lunch", "calories": 550, "protein": 40, "carbs": 60, "fat": 18, "prep_time": 20, "tags": ["gluten_free", "savory", "hot", "spicy", "western", "mexican"], "ingredients": ["Grilled Chicken", "Brown Rice", "Black Beans", "Salsa"]},
            
            # Indian
            {"name": "Rajma Masala with Rice", "type": "lunch", "calories": 500, "protein": 18, "carbs": 70, "fat": 15, "prep_time": 30, "tags": ["vegetarian", "gluten_free", "savory", "hot", "spicy", "indian", "meal_prep"], "ingredients": ["Kidney Beans", "Onion", "Tomato", "Spices", "Basmati Rice"]},
            {"name": "Chicken Curry with Roti", "type": "lunch", "calories": 550, "protein": 35, "carbs": 45, "fat": 25, "prep_time": 40, "tags": ["savory", "hot", "spicy", "indian"], "ingredients": ["Chicken", "Onion", "Tomato", "Spices", "Whole Wheat Roti"]},
            {"name": "Palak Paneer with Rice", "type": "lunch", "calories": 520, "protein": 22, "carbs": 40, "fat": 30, "prep_time": 30, "tags": ["vegetarian", "keto", "gluten_free", "savory", "hot", "indian"], "ingredients": ["Spinach", "Paneer", "Cream", "Spices", "Rice"]},
            {"name": "Chana Masala", "type": "lunch", "calories": 450, "protein": 15, "carbs": 60, "fat": 12, "prep_time": 30, "tags": ["vegan", "vegetarian", "gluten_free", "savory", "hot", "spicy", "indian"], "ingredients": ["Chickpeas", "Onion", "Tomato", "Ginger", "Garlic", "Spices"]},
            {"name": "Dal Tadka with Rice", "type": "lunch", "calories": 420, "protein": 18, "carbs": 65, "fat": 10, "prep_time": 25, "tags": ["vegan", "vegetarian", "gluten_free", "savory", "hot", "indian"], "ingredients": ["Yellow Lentils", "Cumin", "Garlic", "Chili", "Rice"]},
            {"name": "Egg Curry with Roti", "type": "lunch", "calories": 480, "protein": 20, "carbs": 40, "fat": 22, "prep_time": 30, "tags": ["vegetarian", "savory", "hot", "spicy", "indian"], "ingredients": ["Eggs", "Onion", "Tomato", "Spices", "Roti"]},
            {"name": "Bhindi Masala (Okra) with Roti", "type": "lunch", "calories": 380, "protein": 10, "carbs": 45, "fat": 15, "prep_time": 20, "tags": ["vegan", "vegetarian", "gluten_free", "savory", "hot", "spicy", "indian"], "ingredients": ["Okra", "Onion", "Spices", "Roti"]},

            # --- DINNER ---
            # Western
            {"name": "Baked Salmon with Asparagus", "type": "dinner", "calories": 500, "protein": 35, "carbs": 10, "fat": 32, "prep_time": 25, "tags": ["pescatarian", "keto", "gluten_free", "paleo", "savory", "hot", "oven", "western"], "ingredients": ["Salmon Fillet", "Asparagus", "Lemon", "Butter/Oil"]},
            {"name": "Lean Beef Chili", "type": "dinner", "calories": 450, "protein": 35, "carbs": 30, "fat": 18, "prep_time": 40, "tags": ["gluten_free", "savory", "hot", "spicy", "meal_prep", "western"], "ingredients": ["Ground Beef", "Kidney Beans", "Tomatoes", "Chili Powder"]},
            {"name": "Zucchini Noodles with Pesto", "type": "dinner", "calories": 350, "protein": 12, "carbs": 15, "fat": 28, "prep_time": 15, "tags": ["vegetarian", "keto", "gluten_free", "savory", "hot", "western"], "ingredients": ["Zucchini", "Basil Pesto", "Pine Nuts", "Parmesan"]},
            {"name": "Shrimp Stir-Fry", "type": "dinner", "calories": 400, "protein": 30, "carbs": 40, "fat": 12, "prep_time": 15, "tags": ["pescatarian", "gluten_free", "savory", "hot", "quick", "western", "asian"], "ingredients": ["Shrimp", "Bell Peppers", "Snap Peas", "Soy Sauce"]},
            {"name": "Steak with Roasted Veggies", "type": "dinner", "calories": 600, "protein": 45, "carbs": 20, "fat": 35, "prep_time": 30, "tags": ["gluten_free", "paleo", "keto", "savory", "hot", "western"], "ingredients": ["Sirloin Steak", "Brussels Sprouts", "Carrots", "Olive Oil"]},
            
            # Indian
            {"name": "Butter Chicken (Light)", "type": "dinner", "calories": 550, "protein": 35, "carbs": 20, "fat": 30, "prep_time": 40, "tags": ["gluten_free", "savory", "hot", "indian"], "ingredients": ["Chicken", "Tomato Puree", "Cashew Paste", "Spices", "Greek Yogurt"]},
            {"name": "Matar Paneer", "type": "dinner", "calories": 480, "protein": 20, "carbs": 25, "fat": 28, "prep_time": 30, "tags": ["vegetarian", "gluten_free", "savory", "hot", "spicy", "indian"], "ingredients": ["Peas", "Paneer", "Tomato", "Spices"]},
            {"name": "Fish Curry", "type": "dinner", "calories": 450, "protein": 30, "carbs": 15, "fat": 25, "prep_time": 30, "tags": ["pescatarian", "gluten_free", "savory", "hot", "spicy", "indian"], "ingredients": ["Fish Fillet", "Coconut Milk", "Tamarind", "Spices"]},
            {"name": "Baingan Bharta (Roasted Eggplant)", "type": "dinner", "calories": 350, "protein": 8, "carbs": 30, "fat": 15, "prep_time": 40, "tags": ["vegan", "vegetarian", "gluten_free", "savory", "hot", "spicy", "indian"], "ingredients": ["Eggplant", "Onion", "Tomato", "Garlic", "Spices"]},
            {"name": "Chicken Tikka Masala", "type": "dinner", "calories": 520, "protein": 35, "carbs": 25, "fat": 25, "prep_time": 45, "tags": ["gluten_free", "savory", "hot", "spicy", "indian"], "ingredients": ["Chicken", "Yogurt", "Spices", "Tomato Sauce"]},
            {"name": "Dal Makhani (Light)", "type": "dinner", "calories": 450, "protein": 18, "carbs": 45, "fat": 18, "prep_time": 60, "tags": ["vegetarian", "gluten_free", "savory", "hot", "indian"], "ingredients": ["Black Lentils", "Kidney Beans", "Milk/Cream", "Spices"]},
            {"name": "Soya Chunks Curry", "type": "dinner", "calories": 400, "protein": 25, "carbs": 30, "fat": 15, "prep_time": 30, "tags": ["vegan", "vegetarian", "gluten_free", "savory", "hot", "spicy", "indian"], "ingredients": ["Soya Chunks", "Onion", "Tomato", "Potato", "Spices"]},

            # --- SNACKS ---
            # Western
            {"name": "Apple & Almond Butter", "type": "snack", "calories": 200, "protein": 5, "carbs": 25, "fat": 10, "prep_time": 2, "tags": ["vegan", "vegetarian", "gluten_free", "paleo", "sweet", "quick", "western"], "ingredients": ["Apple", "Almond Butter"]},
            {"name": "Greek Yogurt with Honey", "type": "snack", "calories": 180, "protein": 15, "carbs": 20, "fat": 0, "prep_time": 1, "tags": ["vegetarian", "gluten_free", "sweet", "quick", "western"], "ingredients": ["Greek Yogurt", "Honey"]},
            {"name": "Hard Boiled Eggs", "type": "snack", "calories": 140, "protein": 12, "carbs": 1, "fat": 10, "prep_time": 10, "tags": ["vegetarian", "keto", "gluten_free", "paleo", "savory", "meal_prep", "western"], "ingredients": ["Eggs"]},
            {"name": "Hummus & Carrots", "type": "snack", "calories": 180, "protein": 6, "carbs": 20, "fat": 10, "prep_time": 2, "tags": ["vegan", "vegetarian", "gluten_free", "savory", "quick", "western"], "ingredients": ["Hummus", "Carrots"]},
            
            # Indian
            {"name": "Roasted Chana (Chickpeas)", "type": "snack", "calories": 160, "protein": 8, "carbs": 25, "fat": 3, "prep_time": 0, "tags": ["vegan", "vegetarian", "gluten_free", "savory", "quick", "indian"], "ingredients": ["Roasted Chickpeas", "Spices"]},
            {"name": "Sprouts Salad", "type": "snack", "calories": 150, "protein": 10, "carbs": 25, "fat": 1, "prep_time": 5, "tags": ["vegan", "vegetarian", "gluten_free", "savory", "cold", "indian"], "ingredients": ["Moong Sprouts", "Onion", "Tomato", "Lemon"]},
            {"name": "Masala Corn", "type": "snack", "calories": 180, "protein": 5, "carbs": 35, "fat": 2, "prep_time": 5, "tags": ["vegan", "vegetarian", "gluten_free", "savory", "hot", "spicy", "indian"], "ingredients": ["Sweet Corn", "Butter/Oil", "Chaat Masala", "Lemon"]},
            {"name": "Makhana (Fox Nuts)", "type": "snack", "calories": 120, "protein": 3, "carbs": 20, "fat": 5, "prep_time": 5, "tags": ["vegan", "vegetarian", "gluten_free", "savory", "quick", "indian"], "ingredients": ["Makhana", "Ghee/Oil", "Spices"]},
            {"name": "Fruit Chaat", "type": "snack", "calories": 150, "protein": 2, "carbs": 35, "fat": 0, "prep_time": 10, "tags": ["vegan", "vegetarian", "gluten_free", "sweet", "savory", "cold", "indian"], "ingredients": ["Seasonal Fruits", "Chaat Masala", "Lemon"]}
        ]
    
    def generate_meal_recommendations(self, target_calories: int, meal_type: str, user_prefs: Dict = None) -> List[Dict]:
        """
        Smart recommendation engine that filters and scores recipes based on user preferences.
        """
        if user_prefs is None:
            user_prefs = {}
            
        diet_type = user_prefs.get('diet_type', '').lower()
        allergies = [a.lower() for a in user_prefs.get('allergies', [])]
        flavors = [f.lower() for f in user_prefs.get('flavor_profile', [])]
        cuisine_prefs = [c.lower() for c in user_prefs.get('cuisine_preference', [])]
        
        candidates = [r for r in self.recipe_database if r['type'] == meal_type]
        scored_recipes = []
        
        for recipe in candidates:
            score = 1.0
            tags = recipe.get('tags', [])
            
            # 1. HARD FILTERS (Diet Type & Allergies)
            # Diet Type Exclusions
            if diet_type == 'vegan' and 'vegan' not in tags:
                continue
            if diet_type == 'vegetarian' and 'vegetarian' not in tags and 'vegan' not in tags:
                continue
            if diet_type == 'keto' and 'keto' not in tags:
                continue
            if diet_type == 'paleo' and 'paleo' not in tags:
                continue
            if diet_type == 'pescatarian' and 'pescatarian' not in tags and 'vegetarian' not in tags and 'vegan' not in tags:
                continue
                
            # Allergy Exclusions (Simple keyword check)
            if any(allergy in recipe['name'].lower() or any(allergy in ing.lower() for ing in recipe['ingredients']) for allergy in allergies):
                continue

            # 2. SCORING (Preferences)
            # Calorie Match (Bell curve around target)
            cal_diff = abs(recipe['calories'] - target_calories)
            score -= (cal_diff / target_calories) * 0.5  # Up to 50% penalty for calorie mismatch
            
            # Flavor Match
            if any(f in tags for f in flavors):
                score += 0.2
            
            # Cuisine Match
            # If user selected cuisines, boost matching ones. If "No Preference" or empty, no boost/penalty.
            if cuisine_prefs and "no preference" not in cuisine_prefs:
                if any(c in tags for c in cuisine_prefs):
                    score += 0.5 # Strong boost for cuisine match
                else:
                    score -= 0.2 # Slight penalty for non-matching cuisine
            
            # Variety/Randomness (Small jitter to prevent same meals every day)
            score += random.uniform(-0.05, 0.05)
            
            scored_recipes.append({**recipe, "fit_score": max(0.1, score)})
            
        # Sort by score
        scored_recipes.sort(key=lambda x: x['fit_score'], reverse=True)
        
        # Return top matches (or fallback if empty)
        if not scored_recipes:
            # Fallback: Return any recipe of that type if strict filters removed everything
            # This prevents empty plans, but ideally shouldn't happen with a large DB
            return [r for r in candidates][:3]
            
        return scored_recipes[:3]

class PersonalizedDietGenerator:
    """Generate highly personalized diet plans based on 15-question assessment"""
    
    def __init__(self, responses: Dict):
        self.responses = responses
        self.ml_engine = MLNutritionEngine()
        
    def generate_diet_plan(self) -> Dict:
        """Generate comprehensive personalized diet plan"""
        
        # Analyze responses
        analysis = self._analyze_responses()
        
        # Generate plan components
        # Determine duration
        duration_str = analysis.get("plan_duration", "4 Weeks")
        duration_weeks = int(duration_str.split()[0])
        
        weekly_plans = {}
        for week in range(1, duration_weeks + 1):
            weekly_plans[f"Week {week}"] = self._create_weekly_meals(analysis, week)

        diet_plan = {
            "plan_overview": self._create_plan_overview(analysis, duration_str),
            "daily_nutrition_targets": self._calculate_nutrition_targets(analysis),
            "meal_structure": self._design_meal_structure(analysis),
            "weekly_plans": weekly_plans,
            "food_guidelines": self._create_food_guidelines(analysis),
            "hydration_plan": self._create_hydration_plan(analysis),
            "supplement_recommendations": self._recommend_supplements(analysis),
            "success_tracking": self._create_success_metrics(analysis),
            "lifestyle_integration": self._create_lifestyle_tips(analysis)
        }
        
        return diet_plan
    
    def _analyze_responses(self) -> Dict:
        """Analyze user responses to determine plan parameters"""
        
        # Extract key information
        baseline = self.responses.get("quantitative_baseline", {})
        primary_goal = self.responses.get("primary_outcome", "")
        medical = self.responses.get("medical_conditions", [])
        activity = self.responses.get("activity_performance", {})
        
        # Calculate BMR using Mifflin-St Jeor equation
        weight = baseline.get("weight_kg", 70)
        height = baseline.get("height_cm", 170) 
        age = baseline.get("age", 30)
        sex = baseline.get("biological_sex", "Male")
        
        if sex == "Male":
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        
        # Activity multiplier
        workout_freq = activity.get("workout_frequency", "No regular exercise")
        daily_activity = activity.get("daily_activity", "Desk job, mostly sedentary")
        
        if "No regular exercise" in workout_freq and "sedentary" in daily_activity:
            activity_multiplier = 1.2
        elif "1-2 times" in workout_freq:
            activity_multiplier = 1.375
        elif "3-4 times" in workout_freq:
            activity_multiplier = 1.55
        elif "5-6 times" in workout_freq:
            activity_multiplier = 1.725
        else:
            activity_multiplier = 1.9
        
        tdee = bmr * activity_multiplier
        
        # Adjust for goals
        if "stable energy" in primary_goal.lower():
            calorie_target = int(tdee)
            focus = "energy_stability"
        elif "muscle" in primary_goal.lower():
            calorie_target = int(tdee + 300)
            focus = "muscle_building"
        elif "performance" in primary_goal.lower():
            calorie_target = int(tdee + 200)
            focus = "performance"
        elif "blood sugar" in primary_goal.lower():
            calorie_target = int(tdee)
            focus = "blood_sugar"
        else:
            calorie_target = int(tdee)
            focus = "general_health"
        
        return {
            "bmr": bmr,
            "tdee": tdee,
            "calorie_target": calorie_target,
            "focus": focus,
            "medical_conditions": medical,
            "primary_goal": primary_goal,
            "baseline_data": baseline,
            "activity_level": activity,
            "cooking_skills": self.responses.get("cooking_reality", {}),
            "food_preferences": self.responses.get("food_preferences", {}),
            "meal_structure_pref": self.responses.get("meal_structure", {}),
            "social_context": self.responses.get("social_cultural_context", {}),
            "budget": self.responses.get("financial_framework", {}),
            "relationship_with_food": self.responses.get("food_relationship", ""),
            "relationship_with_food": self.responses.get("food_relationship", ""),
            "success_metrics": self.responses.get("success_definition", []),
            "plan_duration": self.responses.get("plan_duration", "4 Weeks"),
            "sleep_stress": self.responses.get("sleep_stress", {}),
            "kitchen_equipment": self.responses.get("kitchen_equipment", []),
            "flavor_profile": self.responses.get("flavor_profile", [])
        }
    
    def _create_plan_overview(self, analysis: Dict, duration: str) -> Dict:
        """Create personalized plan overview"""
        
        focus_descriptions = {
            "energy_stability": "Energy Optimization & Metabolic Balance",
            "muscle_building": "Muscle Building & Performance Nutrition", 
            "performance": "Athletic Performance & Recovery",
            "blood_sugar": "Blood Sugar Management & Metabolic Health",
            "general_health": "Comprehensive Health & Wellness"
        }
        
        plan_name = f"Personalized {focus_descriptions[analysis['focus']]} Plan"
        
        description = f"""
        Your custom nutrition plan designed specifically for your goal: "{analysis['primary_goal']}"
        
        This plan is built around your lifestyle, preferences, and metabolic needs with {analysis['calorie_target']} daily calories.
        Every recommendation is tailored to your cooking skills, time availability, and food preferences.
        """
        
        return {
            "plan_name": plan_name,
            "description": description.strip(),
            "primary_focus": analysis["focus"],
            "primary_focus": analysis["focus"],
            "duration": duration,
            "created_date": datetime.now().isoformat()
        }
    
    def _calculate_nutrition_targets(self, analysis: Dict) -> Dict:
        """Calculate personalized macro and micronutrient targets"""
        
        calories = analysis["calorie_target"]
        focus = analysis["focus"]
        
        # Protein targets based on goals and activity
        if focus == "muscle_building":
            protein_per_kg = 2.2
        elif focus == "performance":
            protein_per_kg = 2.0
        else:
            protein_per_kg = 1.6
        
        protein_g = analysis["baseline_data"].get("weight_kg", 70) * protein_per_kg
        protein_calories = protein_g * 4
        
        # Fat targets
        if focus == "blood_sugar":
            fat_percentage = 0.35  # Higher fat for blood sugar control
        else:
            fat_percentage = 0.25
        
        fat_calories = calories * fat_percentage
        fat_g = fat_calories / 9
        
        # Carbs fill the rest
        carb_calories = calories - protein_calories - fat_calories
        carb_g = carb_calories / 4
        
        return {
            "daily_calories": calories,
            "protein_g": round(protein_g, 1),
            "carbs_g": round(carb_g, 1),
            "fat_g": round(fat_g, 1),
            "fiber_g": round(calories / 100, 1),  # 1g per 100 calories
            "water_liters": round(analysis["baseline_data"].get("weight_kg", 70) * 0.035, 1)
        }
    
    def _design_meal_structure(self, analysis: Dict) -> Dict:
        """Design optimal meal timing and structure"""
        
        meal_pref = analysis["meal_structure_pref"].get("meal_preference", "3 larger meals")
        breakfast_timing = analysis["meal_structure_pref"].get("breakfast_timing", "Mid-morning (8-9am)")
        
        if "3 larger meals" in meal_pref:
            structure = {
                "meal_count": 3,
                "breakfast": {"time": breakfast_timing, "calories_percent": 25},
                "lunch": {"time": "12-1pm", "calories_percent": 35},
                "dinner": {"time": "6-7pm", "calories_percent": 40}
            }
        elif "5-6 smaller meals" in meal_pref:
            structure = {
                "meal_count": 5,
                "breakfast": {"time": breakfast_timing, "calories_percent": 20},
                "snack1": {"time": "10-11am", "calories_percent": 10},
                "lunch": {"time": "12-1pm", "calories_percent": 25},
                "snack2": {"time": "3-4pm", "calories_percent": 15},
                "dinner": {"time": "6-7pm", "calories_percent": 30}
            }
        else:
            structure = {
                "meal_count": 4,
                "breakfast": {"time": breakfast_timing, "calories_percent": 20},
                "lunch": {"time": "12-1pm", "calories_percent": 30},
                "snack": {"time": "3-4pm", "calories_percent": 15},
                "dinner": {"time": "6-7pm", "calories_percent": 35}
            }
        
        return structure
    
    def _create_weekly_meals(self, analysis: Dict, week_num: int) -> Dict:
        """Create ML-powered weekly meal recommendations for a specific week with strict personalization"""
        
        daily_calories = analysis["calorie_target"]
        
        # Generate ML-powered recommendations
        weekly_recommendations = {}
        
        # Define calorie distribution (approximate)
        # Breakfast: 25%, Lunch: 35%, Dinner: 30%, Snack: 10%
        cal_dist = {
            "breakfast": int(daily_calories * 0.25),
            "lunch": int(daily_calories * 0.35),
            "dinner": int(daily_calories * 0.30),
            "snack": int(daily_calories * 0.10)
        }
        
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        for day_idx, day in enumerate(days):
            daily_meals = {}
            
            # Seed random generator for consistent but varied results across weeks/days
            # Use week_num, day index, and a salt to ensure unique selections
            random.seed(week_num * 100 + day_idx)
            
            for meal_type in ["breakfast", "lunch", "dinner", "snack"]:
                target_cals = cal_dist[meal_type]
                
                # Pass full analysis (user prefs) to the engine
                recs = self.ml_engine.generate_meal_recommendations(
                    target_calories=target_cals,
                    meal_type=meal_type,
                    user_prefs=self.responses # Pass raw responses for diet_type, allergies, etc.
                )
                
                # Select the top match, or rotate based on day to avoid repetition if possible
                # Simple rotation: use day_idx % len(recs)
                if recs:
                    selected_idx = day_idx % len(recs)
                    selected_recipe = recs[selected_idx]
                else:
                    selected_recipe = None
                
                daily_meals[meal_type] = {
                    "nutritional_target": {"calories": target_cals, "protein": int(target_cals * 0.25 / 4)}, # Approx protein target
                    "recommendations": recs,
                    "selected_recipe": selected_recipe
                }
            
            weekly_recommendations[day] = daily_meals
        
        # Generate smart shopping list
        ingredients = set()
        for day_meals in weekly_recommendations.values():
            for meal_data in day_meals.values():
                selected = meal_data.get("selected_recipe")
                if selected:
                    ingredients.update(selected.get("ingredients", []))
        
        return {
            "ml_powered_recommendations": weekly_recommendations,
            "smart_shopping_list": sorted(list(ingredients)),
            "meal_prep_tips": ["Batch cook proteins on weekends", "Prep vegetables in advance", "Use meal containers for portion control"]
        }
    
    def _create_food_guidelines(self, analysis: Dict) -> Dict:
        """Create personalized food guidelines"""
        
        medical = analysis["medical_conditions"]
        focus = analysis["focus"]
        
        guidelines = {
            "prioritize": [],
            "limit": [],
            "timing": [],
            "special_considerations": []
        }
        
        # Focus-specific guidelines
        if focus == "energy_stability":
            guidelines["prioritize"].extend([
                "Complex carbohydrates for sustained energy",
                "Protein at every meal to stabilize blood sugar",
                "Healthy fats for satiety"
            ])
            guidelines["timing"].append("Eat every 3-4 hours to maintain stable energy")
        
        elif focus == "muscle_building":
            guidelines["prioritize"].extend([
                "High-quality protein sources",
                "Post-workout protein within 2 hours",
                "Adequate carbohydrates for training fuel"
            ])
        
        # Medical condition modifications
        if "Diabetes" in medical:
            guidelines["special_considerations"].append("Focus on low glycemic index foods")
            guidelines["limit"].append("Simple sugars and refined carbohydrates")
        
        if "IBS" in medical:
            guidelines["special_considerations"].append("Consider low-FODMAP approach")
            guidelines["limit"].append("High-fiber foods initially")
        
        return guidelines
    
    def _create_hydration_plan(self, analysis: Dict) -> Dict:
        """Create personalized hydration strategy"""
        
        current_water = self.responses.get("hydration_status", {}).get("water_glasses", 4)
        target_water = analysis["baseline_data"].get("weight_kg", 70) * 0.035
        
        return {
            "daily_water_target": f"{target_water:.1f} liters",
            "current_intake": f"{current_water} glasses",
            "improvement_needed": target_water > (current_water * 0.25),
            "hydration_tips": [
                "Start each day with a glass of water",
                "Drink water before, during, and after workouts",
                "Set hourly reminders if needed"
            ]
        }
    
    def _recommend_supplements(self, analysis: Dict) -> Dict:
        """Recommend supplements based on individual needs"""
        
        recommendations = {
            "essential": [],
            "beneficial": [],
            "considerations": []
        }
        
        # Basic recommendations
        recommendations["essential"].append("High-quality multivitamin")
        
        if analysis["focus"] == "muscle_building":
            recommendations["beneficial"].extend([
                "Whey protein powder (if needed to meet protein targets)",
                "Creatine monohydrate (3-5g daily)"
            ])
        
        if "Vitamin D deficiency" in analysis["medical_conditions"]:
            recommendations["essential"].append("Vitamin D3 supplement")
        
        recommendations["considerations"].append("Consult healthcare provider before starting any supplements")
        
        return recommendations
    
    def _create_success_metrics(self, analysis: Dict) -> Dict:
        """Define personalized success metrics"""
        
        user_metrics = analysis["success_metrics"]
        
        return {
            "primary_metrics": user_metrics[:3] if len(user_metrics) >= 3 else user_metrics,
            "tracking_methods": [
                "Daily energy level rating (1-10)",
                "Weekly progress photos",
                "Monthly body measurements",
                "Sleep quality tracking"
            ],
            "check_in_frequency": "Weekly self-assessment, monthly plan review"
        }
    
    def _create_lifestyle_tips(self, analysis: Dict) -> Dict:
        """Create lifestyle integration strategies"""
        
        social_context = analysis["social_context"]
        budget = analysis["budget"]
        
        tips = {
            "meal_prep": [],
            "social_eating": [],
            "budget_friendly": [],
            "time_saving": []
        }
        
        # Cooking skill-based tips
        cooking_skill = analysis["cooking_skills"].get("cooking_skill", 5)
        if cooking_skill <= 3:
            tips["time_saving"].extend([
                "Use pre-cut vegetables to save time",
                "Batch cook proteins on weekends",
                "Keep healthy frozen meals as backup"
            ])
        
        # Budget considerations
        weekly_budget = budget.get("weekly_budget", "$100-150")
        if "Under $50" in weekly_budget:
            tips["budget_friendly"].extend([
                "Buy proteins in bulk and freeze portions",
                "Use dried beans and lentils as protein sources",
                "Shop seasonal produce for best prices"
            ])
        
        return tips
    
    def _get_meal_prep_tips(self, skill_level: int, prep_time: str) -> List[str]:
        """Get meal prep tips based on skill and time"""
        
        tips = []
        
        if skill_level <= 3:
            tips.extend([
                "Start with simple assembly meals",
                "Use pre-cooked proteins like rotisserie chicken",
                "Invest in good food storage containers"
            ])
        
        if "Less than 15 minutes" in prep_time:
            tips.extend([
                "Prepare overnight oats for quick breakfasts",
                "Use slow cooker or instant pot for hands-off cooking",
                "Keep healthy snacks pre-portioned"
            ])
        
        return tips

def main():
    """Main diet planner interface with 15-question assessment"""
    
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
    
    st.title("🥗 Advanced Diet Planner")
    st.markdown("*World-class personalized nutrition plans based on 25 essential questions*")
    
    # Initialize recommendation engine
    engine = DietRecommendationEngine()
    
    # Initialize session state
    if "diet_questionnaire_step" not in st.session_state:
        st.session_state.diet_questionnaire_step = 0
    if "diet_responses" not in st.session_state:
        st.session_state.diet_responses = {}
    if "diet_plan" not in st.session_state:
        st.session_state.diet_plan = None
    
    # Show introduction
    if st.session_state.diet_questionnaire_step == 0:
        st.markdown("""
        ### 🎯 The Science of Personalized Nutrition
        
        As a world-renowned dietitian, I believe a nutrition plan is not a set of rules to follow, 
        but a **personalized blueprint** for nourishing your unique body and life.
        
        **Why 25 Questions?**
        - Generic plans are destined to fail
        - Your body, lifestyle, and goals are unique
        - Every recommendation will be tailored specifically to YOU
        
        **What You'll Get:**
        - Scientifically calculated calorie and macro targets
        - Meal plans based on your preferences and cooking skills
        - Strategies that fit your lifestyle and budget
        - Success metrics that matter to YOU
        """)
        
        if st.button("🚀 Start Your Personalized Assessment", type="primary"):
            st.session_state.diet_questionnaire_step = 1
            st.rerun()
        
        return
    
    questions = engine.questions
    total_questions = len(questions)
    
    # Progress tracking
    if st.session_state.diet_questionnaire_step <= total_questions:
        progress = (st.session_state.diet_questionnaire_step - 1) / total_questions
        st.progress(progress)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.caption(f"Question {st.session_state.diet_questionnaire_step} of {total_questions}")
        with col2:
            st.caption(f"Progress: {int(progress * 100)}%")
        with col3:
            current_section = questions[st.session_state.diet_questionnaire_step - 1]["section"]
            st.caption(f"📋 {current_section}")
    
    # Show current question
    if st.session_state.diet_questionnaire_step <= total_questions:
        current_q = questions[st.session_state.diet_questionnaire_step - 1]
        
        st.subheader(f"Question {st.session_state.diet_questionnaire_step}")
        st.markdown(f"**{current_q['question']}**")
        
        # Show why this question matters
        with st.expander("💡 Why this question matters"):
            st.info(current_q['why'])
        
        # Handle different question types
        response = None
        
        if current_q['type'] == 'selectbox':
            response = st.selectbox("Select your answer:", current_q['options'])
        
        elif current_q['type'] == 'multiselect':
            response = st.multiselect("Select all that apply:", current_q['options'])
        
        elif current_q['type'] == 'text_area':
            response = st.text_area(
                "Your answer:", 
                placeholder=current_q.get('placeholder', ''),
                height=100
            )
        
        elif current_q['type'] == 'form':
            st.markdown("**Please provide the following information:**")
            response = {}
            
            for field_name, field_config in current_q['fields'].items():
                if field_config['type'] == 'number':
                    response[field_name] = st.number_input(
                        field_config.get('label', field_name.replace('_', ' ').title()),
                        min_value=field_config.get('min', 0),
                        max_value=field_config.get('max', 1000),
                        value=field_config.get('min', 0)
                    )
                elif field_config['type'] == 'selectbox':
                    response[field_name] = st.selectbox(
                        field_config.get('label', field_name.replace('_', ' ').title()),
                        field_config['options']
                    )
                elif field_config['type'] == 'multiselect':
                    response[field_name] = st.multiselect(
                        field_config.get('label', field_name.replace('_', ' ').title()),
                        field_config['options']
                    )
                elif field_config['type'] == 'slider':
                    response[field_name] = st.slider(
                        field_config.get('label', field_name.replace('_', ' ').title()),
                        field_config['min'],
                        field_config['max'],
                        value=field_config.get('min', 0)
                    )
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.session_state.diet_questionnaire_step > 1:
                if st.button("← Previous", key="prev_diet"):
                    st.session_state.diet_questionnaire_step -= 1
                    st.rerun()
        
        with col2:
            if st.button("Skip Question", key="skip_diet"):
                st.session_state.diet_questionnaire_step += 1
                st.rerun()
        
        with col3:
            if st.button("Next →", type="primary", key="next_diet"):
                # Save response
                st.session_state.diet_responses[current_q['id']] = response
                st.session_state.diet_questionnaire_step += 1
                st.rerun()
    
    else:
        # Generate and display diet plan
        if st.session_state.diet_plan is None:
            with st.spinner("🧠 Creating your personalized nutrition plan..."):
                status_placeholder = st.empty()
                status_placeholder.info("🔬 Analyzing your metabolic profile...")
                time.sleep(1)
                
                status_placeholder.info("🍽️ Designing your meal structure...")
                generator = PersonalizedDietGenerator(st.session_state.diet_responses)
                time.sleep(1)
                
                status_placeholder.info("📊 Calculating your nutrition targets...")
                st.session_state.diet_plan = generator.generate_diet_plan()
                
                # Save to MongoDB if user is logged in
                if st.session_state.get('authenticated') and st.session_state.get('user'):
                    try:
                        from auth_system import FitnessDatabase
                        db = FitnessDatabase()
                        if db.save_diet_plan(st.session_state.user['user_id'], st.session_state.diet_plan):
                            print("Diet plan saved to MongoDB successfully")
                    except Exception as e:
                        print(f"Error saving diet plan: {e}")
                
                # Track plan creation
                try:
                    from mixpanel_analytics import analytics
                    user_id = st.session_state.user['user_id'] if 'user' in st.session_state else "guest"
                    plan = st.session_state.diet_plan
                    targets = plan['daily_nutrition_targets']
                    overview = plan['plan_overview']
                    
                    analytics.track_nutrition_plan_created(
                        user_id,
                        overview['primary_focus'],
                        targets['daily_calories'],
                        overview['plan_name']
                    )
                    
                    # Also set user nutrition preferences
                    analytics.set_nutrition_preferences(
                        user_id,
                        targets['daily_calories'],
                        overview['primary_focus'],
                        0 # Meals logged week placeholder
                    )
                except Exception as e:
                    print(f"Analytics error: {e}")

                time.sleep(1)
                
                status_placeholder.success("✅ Your personalized nutrition plan is ready!")
                time.sleep(1)
                status_placeholder.empty()
        
        # Display the plan
        display_diet_plan(st.session_state.diet_plan)
        
        # Save plan
        if st.button("💾 Save Plan", key="save_diet_plan"):
            st.success("Plan saved!")
        
        # Reset button
        if st.button("🔄 Start Over", key="reset_diet"):
            st.session_state.diet_questionnaire_step = 0
            st.session_state.diet_responses = {}
            st.session_state.diet_plan = None
            st.rerun()

def display_diet_plan(plan: Dict):
    """Display the generated personalized diet plan"""
    
    st.success("🎉 Your Personalized Nutrition Plan is Ready!")
    
    # Plan Overview
    overview = plan['plan_overview']
    st.header(overview['plan_name'])
    st.markdown(overview['description'])
    
    # Daily Nutrition Targets
    st.subheader("🎯 Your Daily Nutrition Targets")
    targets = plan['daily_nutrition_targets']
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Calories", f"{targets['daily_calories']}")
    with col2:
        st.metric("Protein", f"{targets['protein_g']}g")
    with col3:
        st.metric("Carbs", f"{targets['carbs_g']}g")
    with col4:
        st.metric("Fat", f"{targets['fat_g']}g")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Fiber", f"{targets['fiber_g']}g")
    with col2:
        st.metric("Water", f"{targets['water_liters']}L")
    
    # Meal Structure
    st.subheader("⏰ Your Optimal Meal Structure")
    structure = plan['meal_structure']
    st.write(f"**Recommended:** {structure['meal_count']} meals per day")
    
    for meal, details in structure.items():
        if isinstance(details, dict) and 'time' in details:
            st.write(f"• **{meal.title()}**: {details['time']} ({details['calories_percent']}% of daily calories)")
    
    # Food Guidelines
    st.subheader("📋 Your Personalized Food Guidelines")
    guidelines = plan['food_guidelines']
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**✅ Prioritize:**")
        for item in guidelines['prioritize']:
            st.write(f"• {item}")
    
    with col2:
        st.markdown("**⚠️ Limit:**")
        for item in guidelines['limit']:
            st.write(f"• {item}")
    
    if guidelines['special_considerations']:
        st.markdown("**🏥 Special Considerations:**")
        for item in guidelines['special_considerations']:
            st.write(f"• {item}")
    
    # ML-Powered Meal Recommendations
    st.subheader("🤖 AI-Powered Meal Recommendations")
    st.caption("Personalized recipes that match your exact nutritional needs")
    
    if 'weekly_plans' in plan:
        weeks = list(plan['weekly_plans'].keys())
        tabs = st.tabs(weeks)
        
        for i, week_name in enumerate(weeks):
            with tabs[i]:
                week_data = plan['weekly_plans'][week_name]
                
                if 'ml_powered_recommendations' in week_data:
                    ml_recommendations = week_data['ml_powered_recommendations']
                    
                    # Show today's recommendations (or Monday if generic)
                    today = datetime.now().strftime("%A")
                    display_day = today if today in ml_recommendations else "Monday"
                    
                    st.markdown(f"### 📅 Recommendations for {display_day}")
                    
                    day_meals = ml_recommendations.get(display_day, {})
                    
                    for meal_type, meal_data in day_meals.items():
                        if meal_data.get('recommendations'):
                            target = meal_data['nutritional_target']
                            st.markdown(f"**{meal_type.title()}** (Target: {target['calories']} cal, {target['protein']}g protein)")
                            
                            for j, recipe in enumerate(meal_data['recommendations'][:3]):
                                with st.expander(f"Option {j+1}: {recipe['name']} ({recipe['fit_score']:.0%} match)"):
                                    col1, col2 = st.columns([2, 1])
                                    with col1:
                                        st.write(f"🔥 {recipe['calories']} cal | 💪 {recipe['protein']}g protein")
                                        st.write(f"⏱️ {recipe['prep_time']} min prep")
                                        
                                        # Show tags
                                        if 'tags' in recipe:
                                            tags_str = " ".join([f"`{t}`" for t in recipe['tags'][:4]])
                                            st.markdown(f"**Tags:** {tags_str}")
                                            
                                        st.markdown("**Ingredients:**")
                                        for ingredient in recipe['ingredients']:
                                            st.write(f"• {ingredient}")
                            st.divider()
                
                # Show shopping list for this week
                st.subheader(f"🛒 Shopping List for {week_name}")
                shopping_list = week_data.get('smart_shopping_list', [])
                
                col1, col2, col3 = st.columns(3)
                for j, item in enumerate(shopping_list):
                    with [col1, col2, col3][j % 3]:
                        st.write(f"☐ {item}")
    
    # Success Tracking
    st.subheader("📈 How to Track Your Success")
    success = plan['success_tracking']
    
    st.markdown("**Your Personal Success Metrics:**")
    for metric in success['primary_metrics']:
        st.write(f"• {metric}")
    
    st.markdown("**Tracking Methods:**")
    for method in success['tracking_methods']:
        st.write(f"• {method}")
    
    # Lifestyle Tips
    st.subheader("💡 Lifestyle Integration Tips")
    lifestyle = plan['lifestyle_integration']
    
    for category, tips in lifestyle.items():
        if tips:
            st.markdown(f"**{category.replace('_', ' ').title()}:**")
            for tip in tips:
                st.write(f"• {tip}")
    
    # Download options
    st.divider()
    st.subheader("📥 Save Your Plan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Download Complete Plan", type="primary"):
            plan_text = f"""
{overview['plan_name']}
Generated: {datetime.now().strftime('%B %d, %Y')}

DAILY NUTRITION TARGETS:
• Calories: {targets['daily_calories']}
• Protein: {targets['protein_g']}g
• Carbs: {targets['carbs_g']}g
• Fat: {targets['fat_g']}g
• Fiber: {targets['fiber_g']}g
• Water: {targets['water_liters']}L

{overview['description']}

ML-POWERED MEAL RECOMMENDATIONS:
"""
            
            if 'weekly_plans' in plan:
                for week_name, week_data in plan['weekly_plans'].items():
                    plan_text += f"\n\n{'='*30}\n{week_name.upper()}\n{'='*30}\n"
                    
                    if 'ml_powered_recommendations' in week_data:
                        ml_recs = week_data['ml_powered_recommendations']
                        for day, meals in ml_recs.items():
                            plan_text += f"\n{day.upper()}:\n"
                            for meal_type, meal_data in meals.items():
                                selected = meal_data.get('selected_recipe')
                                if selected:
                                    plan_text += f"  {meal_type.title()}: {selected['name']} ({selected['calories']} cal)\n"
            
            st.download_button(
                "📄 Get Your Plan",
                plan_text,
                file_name=f"ml_diet_plan_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
    
    with col2:
        if st.button("🛒 Download Shopping Lists"):
            shopping_text = "SMART SHOPPING LISTS\n" + "="*20 + "\n\n"
            
            if 'weekly_plans' in plan:
                for week_name, week_data in plan['weekly_plans'].items():
                    shopping_text += f"\n{week_name.upper()}\n{'-'*len(week_name)}\n"
                    shopping_list = week_data.get('smart_shopping_list', [])
                    for item in shopping_list:
                        shopping_text += f"☐ {item}\n"
            
            st.download_button(
                "🛒 Get Shopping Lists",
                shopping_text,
                file_name=f"shopping_lists_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )

if __name__ == "__main__":
    main()