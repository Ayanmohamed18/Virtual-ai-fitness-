"""
Multi-Engine Voice Feedback System
Primary: ElevenLabs (premium quality)
Fallback: gTTS (free, good quality)
Last Resort: pyttsx3 (offline)
"""

import os
import tempfile
import threading
import time

# Try importing all voice engines
ELEVENLABS_AVAILABLE = False
GTTS_AVAILABLE = False
PYTTSX3_AVAILABLE = False
PYGAME_AVAILABLE = False

# ElevenLabs (Premium - PRIMARY)
try:
    from elevenlabs import generate, set_api_key
    ELEVENLABS_AVAILABLE = True
except:
    try:
        from elevenlabs.client import ElevenLabs
        ELEVENLABS_AVAILABLE = True
    except:
        pass

# gTTS (Free, requires internet)
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except:
    pass

# pyttsx3 (Free, offline)
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except:
    pass

# Pygame for audio playback
try:
    import pygame
    PYGAME_AVAILABLE = True
except:
    pass


class MultiVoiceEngine:
    """Voice feedback with ElevenLabs as primary, automatic fallback to free alternatives"""
    
    def __init__(self):
        self.last_voice_time = 0
        self.voice_buffer = 2  # seconds between voice prompts
        self.elevenlabs_client = None
        
        # Determine which engines are available
        self.engine_priority = []
        
        # DISABLE ElevenLabs (API issues) - Use free alternatives
        # Check ElevenLabs FIRST (PRIMARY)
        # if ELEVENLABS_AVAILABLE:
        #     api_key = os.getenv("ELEVENLABS_API_KEY", "sk_11540ed8f87bd499b4f216ad860629c495cf18b0042b6ad8")
        #     try:
        #         # Try new SDK first
        #         try:
        #             from elevenlabs.client import ElevenLabs
        #             self.elevenlabs_client = ElevenLabs(api_key=api_key)
        #             self.engine_priority.append("elevenlabs_new")
        #             print("✅ ElevenLabs (new SDK) initialized")
        #         except:
        #             # Fall back to old SDK
        #             from elevenlabs import set_api_key
        #             set_api_key(api_key)
        #             self.engine_priority.append("elevenlabs_old")
        #             print("✅ ElevenLabs (old SDK) initialized")
        #     except Exception as e:
        #         print(f"⚠️  ElevenLabs init failed: {e}")
        
        # Check gTTS (free, good quality) - PRIMARY
        if GTTS_AVAILABLE:
            self.engine_priority.append("gtts")
            print("✅ gTTS (Google Text-to-Speech) initialized as PRIMARY")
        
        # Check pyttsx3 (free, offline)
        if PYTTSX3_AVAILABLE:
            self.engine_priority.append("pyttsx3")
        
        if not self.engine_priority:
            print("⚠️  No voice engines available!")
        else:
            print(f"✅ Voice engines available: {', '.join(self.engine_priority)}")
            print(f"   Primary: {self.engine_priority[0]}")
    
    def speak(self, text, force=False):
        """Generate and play voice feedback"""
        
        # Rate limiting
        if not force and time.time() - self.last_voice_time < self.voice_buffer:
            return
        
        if not self.engine_priority:
            print(f"[Voice]: {text}")
            return
        
        # Try engines in priority order
        for engine in self.engine_priority:
            try:
                if engine == "elevenlabs_new":
                    self._speak_elevenlabs_new(text)
                    break
                elif engine == "elevenlabs_old":
                    self._speak_elevenlabs_old(text)
                    break
                elif engine == "gtts":
                    self._speak_gtts(text)
                    break
                elif engine == "pyttsx3":
                    self._speak_pyttsx3(text)
                    break
            except Exception as e:
                print(f"❌ {engine} failed: {e}, trying next...")
                continue
        
        self.last_voice_time = time.time()
    
    def _speak_elevenlabs_new(self, text):
        """ElevenLabs New SDK (Premium, best quality)"""
        def play():
            try:
                print(f"🎙️  Generating with ElevenLabs: {text[:50]}...")
                
                # Generate audio using new SDK v2.x
                audio_generator = self.elevenlabs_client.text_to_speech.convert(
                    voice_id="Finn",  # or use voice ID
                    text=text,
                    model_id="eleven_turbo_v2"
                )
                
                # Collect audio data from generator
                audio_data = b"".join(chunk for chunk in audio_generator)
                
                if not audio_data:
                    raise Exception("No audio data received")
                
                # Save and play
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                    f.write(audio_data)
                    temp_file = f.name
                
                if PYGAME_AVAILABLE:
                    pygame.mixer.quit()
                    pygame.mixer.init()
                    pygame.mixer.music.load(temp_file)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        pygame.time.Clock().tick(10)
                    pygame.mixer.quit()
                
                os.remove(temp_file)
                print("✅ ElevenLabs playback complete")
                
            except Exception as e:
                raise Exception(f"ElevenLabs new SDK error: {e}")
        
        threading.Thread(target=play, daemon=True).start()
    
    def _speak_elevenlabs_old(self, text):
        """ElevenLabs Old SDK"""
        def play():
            try:
                from elevenlabs import generate
                
                print(f"🎙️  Generating with ElevenLabs: {text[:50]}...")
                
                audio_data = generate(
                    text=text,
                    voice="Finn",
                    model="eleven_turbo_v2"
                )
                
                # Save and play
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                    f.write(audio_data)
                    temp_file = f.name
                
                if PYGAME_AVAILABLE:
                    pygame.mixer.quit()
                    pygame.mixer.init()
                    pygame.mixer.music.load(temp_file)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        pygame.time.Clock().tick(10)
                    pygame.mixer.quit()
                
                os.remove(temp_file)
                print("✅ ElevenLabs playback complete")
                
            except Exception as e:
                raise Exception(f"ElevenLabs old SDK error: {e}")
        
        threading.Thread(target=play, daemon=True).start()
    
    def _speak_gtts(self, text):
        """Google Text-to-Speech (Free, requires internet)"""
        def play():
            try:
                print(f"🎙️  Generating with gTTS: {text[:50]}...")
                
                # Generate audio
                tts = gTTS(text=text, lang='en', slow=False)
                
                # Save to temp file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                    temp_file = f.name
                
                tts.save(temp_file)
                
                # Play with pygame
                if PYGAME_AVAILABLE:
                    pygame.mixer.quit()
                    pygame.mixer.init()
                    pygame.mixer.music.load(temp_file)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        pygame.time.Clock().tick(10)
                    pygame.mixer.quit()
                
                os.remove(temp_file)
                print("✅ gTTS playback complete")
                
            except Exception as e:
                raise Exception(f"gTTS error: {e}")
        
        threading.Thread(target=play, daemon=True).start()
    
    def _speak_pyttsx3(self, text):
        """pyttsx3 (Free, offline, lower quality)"""
        def play():
            try:
                print(f"🎙️  Generating with pyttsx3: {text[:50]}...")
                
                engine = pyttsx3.init()
                
                # Configure voice
                voices = engine.getProperty('voices')
                for voice in voices:
                    if 'male' in voice.name.lower() and 'female' not in voice.name.lower():
                        engine.setProperty('voice', voice.id)
                        break
                
                engine.setProperty('rate', 175)
                engine.setProperty('volume', 1.0)
                
                engine.say(text)
                engine.runAndWait()
                engine.stop()
                print("✅ pyttsx3 playback complete")
                
            except Exception as e:
                raise Exception(f"pyttsx3 error: {e}")
        
        threading.Thread(target=play, daemon=True).start()
    
    def test_voice(self):
        """Test the voice system"""
        test_message = "Voice feedback is working! Let's crush this workout!"
        print(f"Testing voice with: {self.engine_priority[0] if self.engine_priority else 'None'}")
        self.speak(test_message, force=True)


# Global instance
voice_engine = MultiVoiceEngine()


if __name__ == "__main__":
    # Test all engines
    print("Testing Multi-Voice Engine")
    print("=" * 50)
    voice_engine.test_voice()
