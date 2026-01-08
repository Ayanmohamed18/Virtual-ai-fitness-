import streamlit as st
from datetime import datetime, timedelta
import json
from fpdf import FPDF

def feed_ui():
    st.header("📅 Your Daily Feed")

    # 1. Initialize State
    if "plan_start_date" not in st.session_state:
        st.session_state.plan_start_date = datetime.now().date()
    
    if "workout_swaps" not in st.session_state:
        st.session_state.workout_swaps = {}
    
    if "meal_swaps" not in st.session_state:
        st.session_state.meal_swaps = {}
    
    if "custom_meals" not in st.session_state:
        st.session_state.custom_meals = {}
    
    if "custom_workouts" not in st.session_state:
        st.session_state.custom_workouts = {}

    # Download UI at top
    col_download, col_spacer = st.columns([1, 3])
    with col_download:
        render_download_ui()

    st.divider()

    # 2. Calendar Input
    col_cal, col_info = st.columns([1, 2])
    with col_cal:
        selected_date = st.date_input("Select Date", datetime.now())
    
    # 3. Calculate Plan Day
    start_date = st.session_state.plan_start_date
    delta = (selected_date - start_date).days
    
    week_num = (delta // 7) + 1
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_name = day_names[selected_date.weekday()]
    
    with col_info:
        st.subheader(f"{day_name}, {selected_date.strftime('%B %d')}")
        if delta >= 0:
            st.caption(f"Week {week_num} | Day {delta + 1} of your journey")
        else:
            st.caption("Pre-start date")

    # 4. Fetch Data
    diet_plan = st.session_state.get("diet_plan")
    workout_plan = st.session_state.get("workout_plan")
    
    if delta < 0:
        st.info("Please select a date on or after your plan start date.")
        return

    col1, col2 = st.columns(2)
    
    # --- DIET SECTION ---
    with col1:
        st.markdown("### 🥗 Nutrition")
        if diet_plan:
            render_diet_section(diet_plan, selected_date, week_num, day_name, start_date, day_names)
        else:
            st.warning("No diet plan generated yet. Go to Diet Planner to create one!")

    # --- WORKOUT SECTION ---
    with col2:
        st.markdown("### 🏋️ Workout")
        if workout_plan:
            render_workout_section(workout_plan, selected_date, week_num, day_name, start_date, day_names)
        else:
            st.warning("No workout plan generated yet. Go to Workout Planner to create one!")


def render_diet_section(diet_plan, selected_date, week_num, day_name, start_date, day_names):
    """Render diet section with swap and edit functionality"""
    
    # Check for meal swaps
    date_str = str(selected_date)
    
    # Get meal data
    week_key = f"Week {week_num}"
    day_data = None
    
    # Robust retrieval for Diet
    if "weekly_plans" in diet_plan:
        if week_key in diet_plan["weekly_plans"]:
            week_data = diet_plan["weekly_plans"][week_key]
            if "ml_powered_recommendations" in week_data:
                day_data = week_data["ml_powered_recommendations"].get(day_name)
    elif "ml_powered_recommendations" in diet_plan:
        day_data = diet_plan["ml_powered_recommendations"].get(day_name)
    
    if day_data:
        for meal_type, meal_info in day_data.items():
            meal_key = f"{date_str}_{meal_type}"
            
            # Check for swap
            display_meal_info = meal_info
            is_swapped = False
            swap_source = None
            
            if meal_key in st.session_state.meal_swaps:
                swapped_key = st.session_state.meal_swaps[meal_key]
                swap_source = swapped_key
                is_swapped = True
                
                # Get swapped meal data
                swap_parts = swapped_key.split("_")
                swap_date = datetime.strptime(swap_parts[0], "%Y-%m-%d").date()
                swap_meal_type = "_".join(swap_parts[1:])
                
                swap_delta = (swap_date - start_date).days
                swap_week_num = (swap_delta // 7) + 1
                swap_day_name = day_names[swap_date.weekday()]
                
                # Fetch swapped meal
                display_meal_info = get_meal_data(diet_plan, swap_week_num, swap_day_name, swap_meal_type)
            
            # Check for custom meal
            if meal_key in st.session_state.custom_meals:
                display_meal_info = {"selected_recipe": st.session_state.custom_meals[meal_key]}
            
            # Render meal
            with st.expander(f"{meal_type.title()}", expanded=True):
                if is_swapped:
                    st.info(f"🔄 Swapped with {swap_source}")
                
                if display_meal_info and display_meal_info.get('selected_recipe'):
                    recipe = display_meal_info['selected_recipe']
                    st.markdown(f"**{recipe.get('name', 'Custom Meal')}**")
                    st.caption(f"🔥 {recipe.get('calories', 0)} kcal | 🥩 {recipe.get('protein', 0)}g protein")
                    if 'ingredients' in recipe:
                        ingredients = recipe['ingredients']
                        if isinstance(ingredients, list):
                            st.markdown(f"*Ingredients: {', '.join(ingredients[:3])}...*")
                        else:
                            st.markdown(f"*Ingredients: {ingredients}*")
                else:
                    st.write("No specific recipe selected.")
                
                # Action buttons
                col_edit, col_swap = st.columns(2)
                with col_edit:
                    if st.button("✏️ Edit", key=f"edit_meal_{meal_key}"):
                        st.session_state[f"editing_meal_{meal_key}"] = True
                        st.rerun()
                
                with col_swap:
                    if st.button("🔄 Swap", key=f"swap_meal_{meal_key}"):
                        st.session_state[f"swapping_meal_{meal_key}"] = True
                        st.rerun()
                
                # Edit UI
                if st.session_state.get(f"editing_meal_{meal_key}"):
                    render_meal_edit_ui(meal_key, display_meal_info)
                
                # Swap UI
                if st.session_state.get(f"swapping_meal_{meal_key}"):
                    render_meal_swap_ui(meal_key, selected_date, meal_type, start_date)
    else:
        st.info(f"No diet plan data found for {day_name} (Week {week_num}).")


def render_workout_section(workout_plan, selected_date, week_num, day_name, start_date, day_names):
    """Render workout section with swap and edit functionality"""
    
    # Check for swaps
    display_date = selected_date
    display_date_str = str(selected_date)
    is_swapped = False
    
    if display_date_str in st.session_state.workout_swaps:
        swapped_date_str = st.session_state.workout_swaps[display_date_str]
        st.info(f"🔄 Swapped with {swapped_date_str}")
        is_swapped = True
        
        # Recalculate target based on swap
        swapped_date = datetime.strptime(swapped_date_str, "%Y-%m-%d").date()
        swap_delta = (swapped_date - start_date).days
        swap_week_num = (swap_delta // 7) + 1
        swap_day_name = day_names[swapped_date.weekday()]
        
        target_week = swap_week_num
        target_day = swap_day_name
    else:
        target_week = week_num
        target_day = day_name

    # Check for custom workout
    workout_data = None
    if display_date_str in st.session_state.custom_workouts:
        workout_data = st.session_state.custom_workouts[display_date_str]
    else:
        # Retrieve workout from plan
        week_key = f"Week {target_week}"
        
        if "weekly_plans" in workout_plan:
            if week_key in workout_plan["weekly_plans"]:
                week_data = workout_plan["weekly_plans"][week_key]
                workout_data = week_data["schedule"].get(target_day)
        elif "weekly_schedule" in workout_plan:
            workout_data = workout_plan["weekly_schedule"]["weekly_structure"].get(target_day)

    if workout_data:
        if isinstance(workout_data, dict):  # Detailed plan
            st.markdown(f"**Focus:** {workout_data.get('focus', 'N/A')}")
            for ex in workout_data.get('exercises', []):
                st.markdown(f"- **{ex.get('name', 'Exercise')}**: {ex.get('sets', 0)} sets x {ex.get('reps', 0)}")
                if 'notes' in ex:
                    st.caption(f"  _{ex['notes']}_")
        else:  # Simple string plan
            st.write(workout_data)
        
        # Action buttons
        col_edit, col_swap = st.columns(2)
        with col_edit:
            if st.button("✏️ Edit Workout", key=f"edit_workout_{display_date_str}"):
                st.session_state[f"editing_workout_{display_date_str}"] = True
                st.rerun()
        
        with col_swap:
            if st.button("🔄 Swap Workout", key=f"swap_workout_{display_date_str}"):
                st.session_state[f"swapping_workout_{display_date_str}"] = True
                st.rerun()
        
        # Edit UI
        if st.session_state.get(f"editing_workout_{display_date_str}"):
            render_workout_edit_ui(display_date_str, workout_data)
        
        # Swap UI
        if st.session_state.get(f"swapping_workout_{display_date_str}"):
            render_workout_swap_ui(display_date_str, selected_date, start_date)
    else:
        st.write("💤 Rest Day or No Workout Scheduled.")


def render_meal_edit_ui(meal_key, meal_info):
    """Render meal edit form"""
    st.divider()
    st.subheader("✏️ Edit Meal")
    
    # Get current values
    current_recipe = meal_info.get('selected_recipe', {}) if meal_info else {}
    
    with st.form(key=f"meal_edit_form_{meal_key}"):
        name = st.text_input("Meal Name", value=current_recipe.get('name', ''))
        calories = st.number_input("Calories", min_value=0, value=int(current_recipe.get('calories', 0)))
        protein = st.number_input("Protein (g)", min_value=0, value=int(current_recipe.get('protein', 0)))
        carbs = st.number_input("Carbs (g)", min_value=0, value=int(current_recipe.get('carbs', 0)))
        fats = st.number_input("Fats (g)", min_value=0, value=int(current_recipe.get('fats', 0)))
        
        ingredients_list = current_recipe.get('ingredients', [])
        if isinstance(ingredients_list, list):
            ingredients_str = ", ".join(ingredients_list)
        else:
            ingredients_str = str(ingredients_list)
        
        ingredients = st.text_area("Ingredients (comma-separated)", value=ingredients_str)
        
        col_save, col_cancel = st.columns(2)
        with col_save:
            save = st.form_submit_button("💾 Save", type="primary")
        with col_cancel:
            cancel = st.form_submit_button("❌ Cancel")
        
        if save:
            # Save custom meal
            st.session_state.custom_meals[meal_key] = {
                "name": name,
                "calories": calories,
                "protein": protein,
                "carbs": carbs,
                "fats": fats,
                "ingredients": [i.strip() for i in ingredients.split(",")]
            }
            st.session_state[f"editing_meal_{meal_key}"] = False
            st.success("Meal updated!")
            st.rerun()
        
        if cancel:
            st.session_state[f"editing_meal_{meal_key}"] = False
            st.rerun()


def render_meal_swap_ui(meal_key, selected_date, meal_type, start_date):
    """Render meal swap interface"""
    st.divider()
    st.subheader("🔄 Swap Meal")
    
    with st.form(key=f"meal_swap_form_{meal_key}"):
        st.write(f"Swap **{meal_type.title()}** on {selected_date} with:")
        
        swap_date = st.date_input("Target Date", min_value=start_date, key=f"swap_date_{meal_key}")
        swap_meal_type = st.selectbox(
            "Target Meal",
            ["breakfast", "lunch", "dinner", "snacks"],
            key=f"swap_meal_type_{meal_key}"
        )
        
        col_confirm, col_cancel = st.columns(2)
        with col_confirm:
            confirm = st.form_submit_button("✅ Confirm Swap", type="primary")
        with col_cancel:
            cancel = st.form_submit_button("❌ Cancel")
        
        if confirm:
            if swap_date == selected_date and swap_meal_type == meal_type:
                st.error("Cannot swap with the same meal!")
            else:
                target_key = f"{swap_date}_{swap_meal_type}"
                
                # Bi-directional swap
                st.session_state.meal_swaps[meal_key] = target_key
                st.session_state.meal_swaps[target_key] = meal_key
                
                st.session_state[f"swapping_meal_{meal_key}"] = False
                st.success(f"Swapped {meal_type} with {swap_meal_type} on {swap_date}!")
                st.rerun()
        
        if cancel:
            st.session_state[f"swapping_meal_{meal_key}"] = False
            st.rerun()


def render_workout_edit_ui(date_str, workout_data):
    """Render workout edit form"""
    st.divider()
    st.subheader("✏️ Edit Workout")
    
    # Get current values
    current_focus = workout_data.get('focus', '') if isinstance(workout_data, dict) else ''
    current_exercises = workout_data.get('exercises', []) if isinstance(workout_data, dict) else []
    
    with st.form(key=f"workout_edit_form_{date_str}"):
        focus = st.text_input("Workout Focus", value=current_focus)
        
        st.write("**Exercises:**")
        num_exercises = st.number_input("Number of Exercises", min_value=1, max_value=10, value=max(1, len(current_exercises)))
        
        exercises = []
        for i in range(int(num_exercises)):
            st.markdown(f"**Exercise {i+1}**")
            col1, col2, col3 = st.columns(3)
            
            ex_data = current_exercises[i] if i < len(current_exercises) else {}
            
            with col1:
                ex_name = st.text_input("Name", value=ex_data.get('name', ''), key=f"ex_name_{date_str}_{i}")
            with col2:
                # Ensure sets is a valid integer >= 1
                sets_value = ex_data.get('sets', 3)
                try:
                    sets_value = max(1, int(sets_value))
                except (ValueError, TypeError):
                    sets_value = 3
                ex_sets = st.number_input("Sets", min_value=1, value=sets_value, key=f"ex_sets_{date_str}_{i}")
            with col3:
                # Ensure reps is a valid integer >= 1
                reps_value = ex_data.get('reps', 10)
                try:
                    reps_value = max(1, int(reps_value))
                except (ValueError, TypeError):
                    reps_value = 10
                ex_reps = st.number_input("Reps", min_value=1, value=reps_value, key=f"ex_reps_{date_str}_{i}")
            
            ex_notes = st.text_input("Notes (optional)", value=ex_data.get('notes', ''), key=f"ex_notes_{date_str}_{i}")
            
            exercises.append({
                "name": ex_name,
                "sets": int(ex_sets),
                "reps": int(ex_reps),
                "notes": ex_notes
            })
        
        col_save, col_cancel = st.columns(2)
        with col_save:
            save = st.form_submit_button("💾 Save", type="primary")
        with col_cancel:
            cancel = st.form_submit_button("❌ Cancel")
        
        if save:
            # Save custom workout
            st.session_state.custom_workouts[date_str] = {
                "focus": focus,
                "exercises": exercises
            }
            st.session_state[f"editing_workout_{date_str}"] = False
            st.success("Workout updated!")
            st.rerun()
        
        if cancel:
            st.session_state[f"editing_workout_{date_str}"] = False
            st.rerun()


def render_workout_swap_ui(date_str, selected_date, start_date):
    """Render workout swap interface"""
    st.divider()
    st.subheader("🔄 Swap Workout")
    
    with st.form(key=f"workout_swap_form_{date_str}"):
        st.write(f"Swap workout on {selected_date} with:")
        swap_target = st.date_input("Target Date", min_value=start_date, key=f"workout_swap_date_{date_str}")
        
        col_confirm, col_cancel = st.columns(2)
        with col_confirm:
            confirm = st.form_submit_button("✅ Confirm Swap", type="primary")
        with col_cancel:
            cancel = st.form_submit_button("❌ Cancel")
        
        if confirm:
            if swap_target == selected_date:
                st.error("Cannot swap with the same day!")
            else:
                d1 = str(selected_date)
                d2 = str(swap_target)
                
                # Bi-directional swap
                st.session_state.workout_swaps[d1] = d2
                st.session_state.workout_swaps[d2] = d1
                
                st.session_state[f"swapping_workout_{date_str}"] = False
                st.success(f"Swapped {d1} with {d2}!")
                st.rerun()
        
        if cancel:
            st.session_state[f"swapping_workout_{date_str}"] = False
            st.rerun()


def render_download_ui():
    """Render download plan UI"""
    with st.popover("📥 Download Plan"):
        st.write("Export your customized plan")
        
        format_choice = st.radio("Format:", ["JSON", "PDF"], horizontal=True)
        
        if st.button("Download", type="primary"):
            if format_choice == "JSON":
                json_data = export_plan_as_json()
                st.download_button(
                    label="💾 Download JSON",
                    data=json_data,
                    file_name=f"fitness_plan_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
            else:
                pdf_data = export_plan_as_pdf()
                st.download_button(
                    label="💾 Download PDF",
                    data=pdf_data,
                    file_name=f"fitness_plan_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )


def export_plan_as_json():
    """Export plan as JSON"""
    plan_data = {
        "export_date": datetime.now().isoformat(),
        "plan_start_date": str(st.session_state.get("plan_start_date")),
        "diet_plan": st.session_state.get("diet_plan"),
        "workout_plan": st.session_state.get("workout_plan"),
        "customizations": {
            "meal_swaps": st.session_state.get("meal_swaps", {}),
            "workout_swaps": st.session_state.get("workout_swaps", {}),
            "custom_meals": st.session_state.get("custom_meals", {}),
            "custom_workouts": st.session_state.get("custom_workouts", {})
        }
    }
    return json.dumps(plan_data, indent=2, default=str)


def export_plan_as_pdf():
    """Export plan as PDF"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Your Customized Fitness Plan", ln=True, align="C")
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align="C")
    pdf.ln(10)
    
    # Diet Plan Summary
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Diet Plan", ln=True)
    pdf.set_font("Arial", "", 10)
    
    diet_plan = st.session_state.get("diet_plan")
    if diet_plan:
        pdf.multi_cell(0, 5, "Your personalized diet plan with custom modifications.")
        pdf.ln(5)
    
    # Workout Plan Summary
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Workout Plan", ln=True)
    pdf.set_font("Arial", "", 10)
    
    workout_plan = st.session_state.get("workout_plan")
    if workout_plan:
        pdf.multi_cell(0, 5, "Your personalized workout plan with custom modifications.")
        pdf.ln(5)
    
    # Customizations
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Customizations", ln=True)
    pdf.set_font("Arial", "", 10)
    
    meal_swaps = st.session_state.get("meal_swaps", {})
    workout_swaps = st.session_state.get("workout_swaps", {})
    custom_meals = st.session_state.get("custom_meals", {})
    custom_workouts = st.session_state.get("custom_workouts", {})
    
    pdf.multi_cell(0, 5, f"Meal Swaps: {len(meal_swaps) // 2}")
    pdf.multi_cell(0, 5, f"Workout Swaps: {len(workout_swaps) // 2}")
    pdf.multi_cell(0, 5, f"Custom Meals: {len(custom_meals)}")
    pdf.multi_cell(0, 5, f"Custom Workouts: {len(custom_workouts)}")
    
    return pdf.output(dest='S').encode('latin-1')


def get_meal_data(diet_plan, week_num, day_name, meal_type):
    """Helper to get meal data from diet plan"""
    week_key = f"Week {week_num}"
    
    if "weekly_plans" in diet_plan:
        if week_key in diet_plan["weekly_plans"]:
            week_data = diet_plan["weekly_plans"][week_key]
            if "ml_powered_recommendations" in week_data:
                day_data = week_data["ml_powered_recommendations"].get(day_name, {})
                return day_data.get(meal_type)
    elif "ml_powered_recommendations" in diet_plan:
        day_data = diet_plan["ml_powered_recommendations"].get(day_name, {})
        return day_data.get(meal_type)
    
    return None
