import streamlit as st
import requests
import os
from ui_utils import card_container

def get_exercises_by_target(target, api_key):
    """Fetch exercises by target muscle from ExerciseDB"""
    url = f"https://exercisedb.p.rapidapi.com/exercises/bodyPart/{target}"
    
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "exercisedb.p.rapidapi.com"
    }
    
    try:
        response = requests.get(url, headers=headers, params={"limit": "50"}) # Limit to avoid huge payloads
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return []

def exercise_library_ui():
    st.header("📚 Exercise Video Library")
    st.markdown("Explore detailed video demonstrations for every muscle group.")

    # 1. API Key Handling
    api_key = os.getenv("RAPIDAPI_KEY")
    
    if not api_key:
        with st.expander("🔑 Setup API Key", expanded=True):
            st.warning("RapidAPI Key for ExerciseDB not found in environment variables.")
            api_key = st.text_input("Enter your RapidAPI Key (ExerciseDB):", type="password")
            st.caption("Get your key here: [ExerciseDB on RapidAPI](https://rapidapi.com/justin-t/api/exercisedb)")
            if not api_key:
                st.info("Please enter a key to proceed.")
                return

    # 2. Muscle Selector
    muscle_targets = [
        "chest", "back", "cardio", "lower arms", "lower legs", 
        "neck", "shoulders", "upper arms", "upper legs", "waist"
    ]
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("1. Select Muscle")
        selected_target = st.selectbox("Target Muscle Group", muscle_targets, index=0)
        
        # Fetch Data
        if "exercise_cache" not in st.session_state:
            st.session_state.exercise_cache = {}
            
        cache_key = f"ex_{selected_target}"
        
        if cache_key not in st.session_state.exercise_cache:
            with st.spinner(f"Fetching exercises for {selected_target}..."):
                st.session_state.exercise_cache[cache_key] = get_exercises_by_target(selected_target, api_key)
        
        exercises = st.session_state.exercise_cache[cache_key]
        
        if not exercises:
            st.error("Failed to fetch exercises. Please check your API key.")
            return

        # Filter options
        exercise_names = [ex["name"].title() for ex in exercises]
        
        st.subheader("2. Select Exercise")
        selected_exercise_name = st.selectbox("Choose variation", exercise_names)

    # 3. Display Section
    with col2:
        # Find the full object
        selected_ex_data = next((ex for ex in exercises if ex["name"].title() == selected_exercise_name), None)
        
        if selected_ex_data:
            st.subheader(selected_exercise_name)
            
            # --- YouTube Integration ---
            try:
                # Check for API Key first
                youtube_api_key = os.getenv("YOUTUBE_API_KEY")
                results = []
                
                if youtube_api_key and len(youtube_api_key) > 10:
                    # Use Official API
                    from googleapiclient.discovery import build
                    youtube = build('youtube', 'v3', developerKey=youtube_api_key)
                    
                    search_query = f"{selected_exercise_name} exercise form demonstration"
                    
                    request = youtube.search().list(
                        part="snippet",
                        maxResults=1,
                        q=search_query,
                        type="video"
                    )
                    response = request.execute()
                    
                    if response['items']:
                        video_id = response['items'][0]['id']['videoId']
                        title = response['items'][0]['snippet']['title']
                        results = [{'id': video_id, 'title': title}]
                else:
                    # Use YoutubeSearch Library (Fallback)
                    from youtube_search import YoutubeSearch
                    search_query = f"{selected_exercise_name} exercise form demonstration"
                    results = YoutubeSearch(search_query, max_results=1).to_dict()
                
                if results:
                    video_id = results[0]['id']
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    st.video(video_url)
                    st.caption(f"📺 YouTube Demonstration: {results[0]['title']}")
                else:
                    st.info("No YouTube video found.")
                    
            except Exception as e:
                # Fallback to GIF if YouTube fails
                # Display GIF/Video
                gif_url = selected_ex_data.get("gifUrl")
                
                # Fallback if gifUrl is missing from API (Common issue with some endpoints)
                if not gif_url and "id" in selected_ex_data:
                    gif_url = f"https://d205bpvrqc9yn1.cloudfront.net/{selected_ex_data['id']}.gif"
                
                if gif_url:
                    # Use a container with border for the video
                    st.image(gif_url, caption="Demonstration", use_column_width=True)
                else:
                    st.info("No video demonstration available.")
            # ---------------------------
            with st.expander("📝 Instructions & Details", expanded=False):
                st.markdown(f"**Target:** {selected_ex_data.get('target', '').title()}")
                st.markdown(f"**Equipment:** {selected_ex_data.get('equipment', '').title()}")
                st.markdown(f"**Body Part:** {selected_ex_data.get('bodyPart', '').title()}")
                
                instructions = selected_ex_data.get("instructions", [])
                if instructions:
                    st.markdown("**Instructions:**")
                    for i, step in enumerate(instructions, 1):
                        st.markdown(f"{i}. {step}")
            
    # clear cache button
    if st.sidebar.button("Refresh Exercise Library"):
        st.session_state.exercise_cache = {}
        st.rerun()
