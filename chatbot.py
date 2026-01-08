import os
import streamlit as st
from typing import Literal
from dataclasses import dataclass

# Try to import optional dependencies
DEEPSEEK_AVAILABLE = False
SPEECH_RECOGNITION_AVAILABLE = False

try:
    from dotenv import load_dotenv
    load_dotenv()
    DOTENV_AVAILABLE = True
except (ImportError, UnicodeDecodeError, Exception):
    DOTENV_AVAILABLE = False

try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    pass

try:
    from enhanced_deepseek_integration import get_fitness_response, enhanced_client
    DEEPSEEK_AVAILABLE = True
except ImportError:
    DEEPSEEK_AVAILABLE = False

# Check if DeepSeek is properly configured
if DEEPSEEK_AVAILABLE and DOTENV_AVAILABLE:
    deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
    if not deepseek_api_key:
        DEEPSEEK_AVAILABLE = False


@dataclass
class Message:
    origin: Literal["human", "ai"]
    content: str


def initialize_session_state():
    if "token_count" not in st.session_state:
        st.session_state.token_count = 0
    if "history" not in st.session_state:
        st.session_state.history = []
    if "user_id" not in st.session_state:
        st.session_state.user_id = "streamlit_user_" + str(hash(st.session_state.get("session_id", "default")))


# Voice Input using speech recognition
def voice_input():
    if not SPEECH_RECOGNITION_AVAILABLE:
        st.error(
            "Speech recognition is not available. Please run 'pip install SpeechRecognition pyaudio' to enable voice input."
        )
        return ""

    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.write("Listening... Please speak now.")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio_data = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            st.write("Recognizing...")
            text = recognizer.recognize_google(audio_data)
            st.success(f"You said: {text}")
            return text
    except sr.WaitTimeoutError:
        st.error("No speech detected within the time limit. Please try again.")
        return ""
    except sr.UnknownValueError:
        st.error("Sorry, I couldn't understand your voice. Please try again.")
        return ""
    except Exception as e:
        st.error(f"Error: {e}")
        return ""


def simple_fitness_response(query):
    """Expert trainer responses that sound natural and experienced"""
    query_lower = query.lower()
    
    # Workout and Exercise
    if any(word in query_lower for word in ['workout', 'exercise', 'training', 'routine']):
        if 'beginner' in query_lower:
            return "Alright, listen up. I've been training people for over 15 years, and here's what separates those who succeed from those who quit after 3 weeks: Start stupidly simple. Bodyweight squats, push-ups (wall or knee if you need to), and planks. That's it. Three days a week, focus on nailing the form. I don't care if you can only do 3 push-ups - do 3 perfect ones. Your ego will recover, but bad habits stick around forever. Trust me on this one."
        elif 'home' in query_lower:
            return "Home workouts? Brother, I've gotten clients absolutely shredded in their living rooms. Here's the deal - you don't need fancy equipment, you need intensity and consistency. Push-ups, squats, lunges, planks, mountain climbers. 20-30 minutes, 3-4 times a week. I had one client lose 35 pounds doing nothing but this routine. The secret sauce? Make every rep count. No half-assing it because nobody's watching."
        else:
            return "Here's my go-to formula that's never failed me: 5-minute warm-up to get the blood flowing, 20-30 minutes hitting the big compound movements - squats, push-ups, rows - then finish with whatever cardio doesn't make you want to die. Do this 3-4 times a week. Keep it simple, stay consistent, and the results will come. I promise you that."
    
    # Diet and Nutrition
    elif any(word in query_lower for word in ['diet', 'nutrition', 'food', 'eat', 'meal']):
        if 'protein' in query_lower:
            return "Protein is absolutely king, especially if you're serious about this. Aim for 1.6-2.2g per kg of body weight if you're training hard. Chicken breast, fish, eggs, Greek yogurt - stick to the basics that have been working for decades. Don't get caught up in the fancy stuff. I've seen too many people obsess over the perfect protein powder while eating like garbage the rest of the day. Hit your numbers with real food first."
        elif 'weight loss' in query_lower or 'lose weight' in query_lower:
            return "Fat loss comes down to one thing: eating less than you burn. Create a 300-500 calorie deficit, prioritize protein to keep your muscle, and lift weights so you don't end up skinny-fat. The magic isn't in some special diet - it's in being consistent day after day. I've watched people lose 50+ pounds just by tracking their food and staying in that deficit. It works, but you gotta stick with it."
        else:
            return "Nutrition doesn't need to be rocket science. Lean proteins, plenty of vegetables, some fruits, whole grains, and healthy fats. Eat real food that your great-grandmother would recognize. Control your portions, drink water, and stop eating when you're 80% full. That's literally 90% of it right there. The other 10% is just details that don't matter until you've mastered the basics."
    
    # Weight Management
    elif any(word in query_lower for word in ['weight', 'lose', 'gain', 'fat', 'calories']):
        if 'gain' in query_lower:
            return "Want to gain weight the right way? Eat 300-500 calories above maintenance, focus on nutrient-dense foods, and lift heavy things. Don't just stuff your face with pizza and call it bulking - you want to build muscle, not just get fat. I've seen too many guys go from skinny to skinny-fat because they thought eating everything in sight was the answer. Be smarter than that."
        else:
            return "Weight management is simple math: calories in versus calories out. Create the right deficit or surplus for your goals, be patient with the process, and stay consistent. The scale will follow eventually. But here's the thing - don't live and die by that number. I've had clients gain 5 pounds while dropping 2 dress sizes. Focus on how you feel and how your clothes fit."
    
    # Muscle Building
    elif any(word in query_lower for word in ['muscle', 'strength', 'build', 'gain muscle']):
        return "Building muscle? It all comes down to progressive overload. Every week, you need to challenge your muscles more than the week before - more weight, more reps, more sets, whatever. Eat enough protein (1.8-2.2g per kg), sleep 7-9 hours, and be patient. Muscle building is a marathon, not a sprint. I've been at this for decades, and the guys who succeed are the ones who show up consistently for months and years, not weeks."
    
    # Cardio
    elif any(word in query_lower for word in ['cardio', 'running', 'walking', 'cycling']):
        return "Cardio gets a bad rap, but it's fantastic for heart health and fat loss. Start with 150 minutes of moderate activity per week - that's just 20-25 minutes daily. Find something you actually enjoy, because consistency beats intensity every single time. I'd rather have you walk 20 minutes every day than run your ass off once a week and then skip the next two weeks because you're burnt out."
    
    # Recovery and Rest
    elif any(word in query_lower for word in ['rest', 'recovery', 'sleep', 'sore']):
        return "Recovery is where the magic actually happens. Your muscles don't grow during the workout - they grow during recovery. Sleep 7-9 hours, eat protein after your workouts, and take your rest days seriously. I've seen more people sabotage their progress by not recovering properly than by not training hard enough. Your body needs time to adapt and rebuild."
    
    # Motivation and Goals
    elif any(word in query_lower for word in ['motivation', 'goal', 'start', 'begin']):
        return "Here's the truth about motivation - it gets you started, but habits keep you going. Set small, achievable goals that you can actually hit. Track your progress, celebrate the wins, and don't beat yourself up over the setbacks. And remember this: you don't need to feel motivated to take action. Some of my best workouts happened when I didn't want to be there. Just show up."
    
    # General Health
    elif any(word in query_lower for word in ['health', 'healthy', 'wellness']):
        return "Health is actually pretty simple when you strip away all the noise: move your body regularly, eat real food most of the time, sleep well, manage your stress, and stay connected with people you care about. Don't overcomplicate it with the latest trends and fads. Small, consistent actions compound into massive results over time. I've seen it happen thousands of times."
    
    else:
        return "I'm here to help you crush your fitness goals, whatever they are. Whether you want to lose fat, build muscle, get stronger, or just feel better in your own skin - I've got the experience to guide you there. After training everyone from complete beginners to competitive athletes, I can tell you this: success comes down to consistency and patience. What's your biggest challenge right now? Let's tackle it together."

def on_click_callback(use_voice=False):
    try:
        if use_voice:
            human_prompt = voice_input()
        else:
            human_prompt = st.session_state.get("human_prompt", "")

        if human_prompt:
            if DEEPSEEK_AVAILABLE:
                try:
                    llm_response = get_fitness_response(st.session_state.user_id, human_prompt)
                except Exception as e:
                    # Fallback to simple responses if DeepSeek fails
                    llm_response = simple_fitness_response(human_prompt)
            else:
                # Use simple responses if no DeepSeek available
                llm_response = simple_fitness_response(human_prompt)

            st.session_state.history.append(Message("human", human_prompt))
            st.session_state.history.append(Message("ai", llm_response))
            st.session_state.token_count += len(llm_response.split())

            # Clear input
            st.session_state.human_prompt = ""
    except Exception as e:
        st.error(f"Error: {e}")


def chat_ui():
    initialize_session_state()
    
    st.title("💪 Your Personal Trainer")
    
    # Initialize Mode
    if "chat_mode" not in st.session_state:
        st.session_state.chat_mode = "General"
    
    # Status Indicators
    if not DEEPSEEK_AVAILABLE:
        st.warning("🤖 using enhanced basic responses. Add DEEPSEEK_API_KEY for AI.")
    else:
        try:
            from local_llm_handler import local_llm
            if local_llm and local_llm.model:
                st.success("🧠 Fine-tuned Local Model Active (DeepSeek-R1-Distill-Qwen-7B + LoRA)")
            else:
                st.success("☁️ Enhanced AI with DeepSeek API Active")
        except ImportError:
            st.success("✅ Enhanced AI Active")

    # Quick Topics (Top Bar)
    with st.expander("🚀 Quick Topics", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        
        if col1.button("🏋️ Workout Plan"):
            st.session_state.chat_mode = "Workout Plan"
            st.session_state.history.append(Message("ai", "I'm set to **Workout Plan** mode. I'll focus on creating the perfect routine for you. What are your goals?"))
            st.rerun()
            
        if col2.button("🥗 Nutrition Guide"):
            st.session_state.chat_mode = "Nutrition"
            st.session_state.history.append(Message("ai", "I'm set to **Nutrition** mode. Let's talk about fueling your body. What do you need help with?"))
            st.rerun()
            
        if col3.button("💪 Muscle Build"):
            st.session_state.chat_mode = "Muscle Building"
            st.session_state.history.append(Message("ai", "I'm set to **Muscle Building** mode. Hypertrophy is the name of the game. What's your current status?"))
            st.rerun()
            
        if col4.button("📝 Plan Modifier"):
            st.session_state.chat_mode = "Plan Modifier"
            st.session_state.history.append(Message("ai", "I'm set to **Plan Modifier** mode. Please look at the options below to upload your plan."))
            st.rerun()

    # Plan Modifier Context UI
    file_content = ""
    if st.session_state.chat_mode == "Plan Modifier":
        with st.container(): 
            st.info("🔧 **Plan Modifier Active**")
            plan_type = st.radio("Select Plan Type:", ["Workout Planner", "Diet Planner"], horizontal=True)
            uploaded_file = st.file_uploader(f"Upload your {plan_type} (TXT/PDF)", type=['txt', 'pdf'])
            
            if uploaded_file:
                try:
                    if uploaded_file.type == "application/pdf":
                        try:
                            import PyPDF2
                            pdf_reader = PyPDF2.PdfReader(uploaded_file)
                            for page in pdf_reader.pages:
                                file_content += page.extract_text()
                        except ImportError:
                            st.warning("PyPDF2 not installed. Treating as text.")
                            file_content = uploaded_file.getvalue().decode("utf-8", errors='ignore')
                    else:
                        file_content = uploaded_file.getvalue().decode("utf-8")
                    
                    st.success("✅ File loaded! Ask me what changes you want to make.")
                    with st.expander("View Uploaded Content"):
                        st.text(file_content[:1000] + "...")
                except Exception as e:
                    st.error(f"Error reading file: {e}")

    # Display Chat History
    for msg in st.session_state.history:
        with st.chat_message(msg.origin):
            st.write(msg.content)

    # Helper to clean response of tokens for display
    def clean_response(text):
        return text.replace("[OPTIONS_PROVIDED]", "").replace("[CONFIRMATION_NEEDED]", "").replace("[FINAL_PLAN_READY]", "")

    # Helper function to process response and return cleaned text + state
    def processing_state(text):
        if "[OPTIONS_PROVIDED]" in text: return "options"
        if "[CONFIRMATION_NEEDED]" in text: return "confirm"
        if "[FINAL_PLAN_READY]" in text: return "final"
        return "normal"

    # Chat Input
    if prompt := st.chat_input(f"Message ({st.session_state.chat_mode} Mode)..."):
        # 1. Display User Message
        st.session_state.history.append(Message("human", prompt))
        with st.chat_message("human"):
            st.write(prompt)

        # 2. Generate AI Response
        with st.chat_message("ai"):
            status = st.status("🧠 Thinking...", expanded=True)
            placeholder = st.empty()
            full_response = ""
            
            # Construct Contextual Prompt and logic
            context_prefix = ""
            system_prompt_override = None
            
            if st.session_state.chat_mode == "Workout Plan":
                context_prefix = "FOCUS: Create or advise on detailed WORKOUT PLANS. Be technical about sets, reps, and exercises.\n\n"
            elif st.session_state.chat_mode == "Nutrition":
                context_prefix = "FOCUS: NUTRITION and DIET. Discuss macros, calories, and meal timing.\n\n"
            elif st.session_state.chat_mode == "Muscle Building":
                context_prefix = "FOCUS: HYPERTROPHY and MUSCLE GROWTH. Focus on volume, intensity, and recovery.\n\n"
            elif st.session_state.chat_mode == "Plan Modifier":
                # Strict System Prompt for Plan Modifier
                system_prompt_override = """You are a Functional Plan Modification Engine.
                
CRITICAL INSTRUCTIONS:
1. You are NOT a chatty assistant. You are a logic engine for modifying fitness/diet plans.
2. You MUST strictly follow the state flow below.
3. You MUST append specific status tokens to the end of your response.

STATE FLOW:
A. IF user requests a change (e.g., "Swap Monday breakfast", "I can't do gym on Tue"):
   - GENERATE 3 distinct, numbered options.
   - APPEND `[OPTIONS_PROVIDED]` to the end.

B. IF user selects an Option (e.g., "Option 1"):
   - GENERATE a preview of the specific day/meal change.
   - ASK the user to confirm.
   - APPEND `[CONFIRMATION_NEEDED]` to the end.

C. IF user confirms (e.g., "Go ahead", "Yes"):
   - GENERATE the FULL, COMPLETE, MODIFIED PLAN document.
   - APPEND `[FINAL_PLAN_READY]` to the end.

DO NOT deviate from this flow. DO NOT be apologetic. BE DIRECT."""

                if file_content:
                    context_prefix = f"TASK: MODIFY the existing plan based on user request.\n\nCONTEXT FILE:\n{file_content}\n\nUSER REQUEST: "
                else:
                    context_prefix = "TASK: The user wants to modify a plan but hasn't uploaded one yet. Ask them to upload it.\n\n"
            
            final_prompt = context_prefix + prompt
            
            try:
                if DEEPSEEK_AVAILABLE:
                    # Pass the system_prompt_override if it exists
                    stream = enhanced_client.generate_fitness_response_stream(final_prompt, system_prompt_override=system_prompt_override)
                    status.update(label="⚡ Generating answer...", state="running")
                    
                    import time
                    last_update = time.time()
                    info_update_interval = 0.1 # Update UI every 100ms
                    
                    for chunk in stream:
                        full_response += chunk
                        
                        # Buffer updates to prevent UI lag
                        current_time = time.time()
                        if current_time - last_update > info_update_interval:
                            # Clean stream for display
                            display_text = clean_response(full_response)
                            placeholder.markdown(display_text + "▌")
                            last_update = current_time
                    
                    # Final clean render
                    final_display = clean_response(full_response)
                    placeholder.markdown(final_display)
                    status.update(label="✅ Answer ready", state="complete", expanded=False)
                    
                    # Handle File Download if Final Plan
                    if "[FINAL_PLAN_READY]" in full_response:
                        st.session_state['last_plan'] = final_display
                        
                else:
                    time.sleep(0.5) # Reduced simulated delay
                    full_response = simple_fitness_response(prompt)
                    placeholder.markdown(full_response)
                    status.update(label="✅ Generated", state="complete", expanded=False)
            except Exception as e:
                status.update(label="❌ Error", state="error")
                st.error(f"Error: {e}")
                full_response = simple_fitness_response(prompt)
                placeholder.markdown(full_response)
            
            st.session_state.history.append(Message("ai", full_response))
            st.session_state.token_count += len(full_response.split())
            
            # Rerun to show buttons below
            st.rerun()

    # Post-Loop Interaction Buttons (Outside prompt block to persist)
    if st.session_state.history:
        last_msg = st.session_state.history[-1]
        if last_msg.origin == "ai":
            state = processing_state(last_msg.content)
            
            if state == "options":
                st.info("👇 **Select an option:**")
                c1, c2, c3, c4 = st.columns(4)
                if c1.button("Option 1"):
                    st.session_state.history.append(Message("human", "I choose Option 1."))
                    st.rerun()
                if c2.button("Option 2"):
                    st.session_state.history.append(Message("human", "I choose Option 2."))
                    st.rerun()
                if c3.button("Option 3"):
                    st.session_state.history.append(Message("human", "I choose Option 3."))
                    st.rerun()
                if c4.button("Option 4"):
                    st.session_state.history.append(Message("human", "I choose Option 4."))
                    st.rerun()
                    
            elif state == "confirm":
                st.warning("⚠️ **Please verify the plan above.**")
                if st.button("✅ Go Ahead - Generate Final Plan", type="primary"):
                    st.session_state.history.append(Message("human", "Go ahead. Generate the final plan."))
                    st.rerun()
                    
            elif state == "final":
                if 'last_plan' in st.session_state:
                    st.success("🎉 Plan Ready!")
                    st.download_button(
                        label="📥 Download Final Plan",
                        data=st.session_state['last_plan'],
                        file_name="modified_plan.txt",
                        mime="text/plain"
                    )

    # Display Stats
    if st.session_state.history:
        st.caption(f"💬 Messages: {len(st.session_state.history)//2} | Tokens: {st.session_state.token_count}")

if __name__ == "__main__":
    chat_ui()