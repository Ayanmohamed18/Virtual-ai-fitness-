"""
Production-Ready Expert Feedback
Exactly as experienced trainers speak during live sessions
"""

import random

# BICEP CURL FEEDBACK
BICEP_CURL_GOOD = [
    "That's it, control the movement, don't rush it.",
    "Good, keep those elbows pinned — that's clean.",
    "Nice tempo, you're owning that weight.",
    "Strong curl, squeeze at the top.",
    "Perfect range, that's how you build real muscle.",
    "Stay tall, chest up — excellent.",
    "That rep was solid, keep going.",
    "Smooth and controlled, exactly what I want.",
    "Feel that contraction, don't let it swing.",
    "Yes, that's a textbook curl.",
    "Breathe, stay steady — you've got this.",
    "Nice control on the way down.",
    "That's discipline right there.",
    "Good mind-muscle connection, keep it tight.",
    "Let's finish strong, same form."
]

BICEP_CURL_BAD = [
    "Slow it down — don't swing the weight.",
    "Keep your elbows close, don't let them drift.",
    "Control the negative, don't drop it.",
    "Stop leaning back, stand tall.",
    "Reduce the momentum, use the muscle.",
    "Lock that core, you're rocking too much.",
    "Lighter weight if needed — form comes first.",
    "Curl through the elbow, not the shoulder.",
    "Pause at the top, feel the squeeze.",
    "Keep your wrists straight.",
    "Don't rush the reps, stay in control.",
    "That's momentum — reset and go again.",
    "Focus on quality, not speed.",
    "Elbows tight, chest proud.",
    "Fix the form now — then push again."
]

# PUSH-UP FEEDBACK
PUSH_UP_GOOD = [
    "That's clean, body straight — beautiful.",
    "Strong push, keep that line tight.",
    "Chest to the floor, full range.",
    "Core tight, you're moving as one unit.",
    "Nice depth, that's real work.",
    "Good control, don't rush it.",
    "Perfect plank position.",
    "That rep was money.",
    "Drive through the palms.",
    "Strong lockout at the top.",
    "Breathing looks good — stay steady.",
    "That's solid upper-body control.",
    "Nice pace, keep it consistent.",
    "You're owning these reps.",
    "Finish strong, same form."
]

PUSH_UP_BAD = [
    "Hips are sagging — tighten your core.",
    "Don't flare the elbows out.",
    "Chest lower — commit to the rep.",
    "Keep your body straight, no bending.",
    "Slow down, control the descent.",
    "Neck neutral — don't look forward.",
    "Elbows closer to your sides.",
    "Stop bouncing at the bottom.",
    "Reset your plank before the next rep.",
    "Full range, don't cheat it.",
    "Control first, speed later.",
    "Brace your core — everything tight.",
    "That's half a rep, go deeper.",
    "Fix the line of your body.",
    "Clean it up — quality reps only."
]

# PULL-UP FEEDBACK
PULL_UP_GOOD = [
    "Strong pull — that's clean.",
    "Chest up, great control.",
    "Full extension at the bottom — nice.",
    "Smooth pull, no jerking.",
    "That's strength, keep it steady.",
    "Good tempo, own every inch.",
    "Nice squeeze at the top.",
    "Elbows driving down — perfect.",
    "Controlled negative, love that.",
    "That rep was solid.",
    "Stay tight through the core.",
    "Strong back engagement.",
    "Clean rep — no momentum.",
    "Keep breathing, stay calm.",
    "Finish with the same form."
]

PULL_UP_BAD = [
    "Stop swinging — reset.",
    "Use your back, not momentum.",
    "Full extension at the bottom.",
    "Chest up — don't crane your neck.",
    "Control the drop, don't fall.",
    "Slow the movement down.",
    "That's a kip — strict reps only.",
    "Pull through the elbows.",
    "Tighten your core.",
    "Pause, then pull clean.",
    "Less speed, more control.",
    "Fix the swing before the next rep.",
    "Short reps won't build strength.",
    "Reset your grip and posture.",
    "Clean it up — then go again."
]

# SHOULDER PRESS FEEDBACK
SHOULDER_PRESS_GOOD = [
    "Strong press — straight up.",
    "Core tight, nice stability.",
    "Good lockout at the top.",
    "Smooth path, well controlled.",
    "Elbows stacked — perfect.",
    "Nice breathing rhythm.",
    "That rep was clean.",
    "Control on the way down.",
    "Good shoulder engagement.",
    "Upright posture — excellent.",
    "Pressing with confidence.",
    "Stay tight through the core.",
    "That's how you protect the shoulders.",
    "Solid strength, keep going.",
    "Finish strong, same control."
]

SHOULDER_PRESS_BAD = [
    "Don't arch your lower back.",
    "Keep the core braced.",
    "Press straight up, not forward.",
    "Slow it down — control first.",
    "Elbows under the wrists.",
    "Stop flaring too wide.",
    "Lighter weight if needed.",
    "That's back compensation — reset.",
    "Control the negative.",
    "Neutral spine — no leaning.",
    "Fix posture before the next rep.",
    "Stack joints properly.",
    "Smooth motion, no jerking.",
    "Quality reps over heavy weight.",
    "Clean form — then push again."
]


def get_expert_feedback(exercise, form_correct):
    """
    Get production-ready expert feedback
    
    Args:
        exercise: "bicep_curl", "push_up", "pull_up", "shoulder_press"
        form_correct: True for good form, False for corrections
    
    Returns:
        Random expert feedback string
    """
    
    if exercise == "bicep_curl":
        return random.choice(BICEP_CURL_GOOD if form_correct else BICEP_CURL_BAD)
    
    elif exercise == "push_up":
        return random.choice(PUSH_UP_GOOD if form_correct else PUSH_UP_BAD)
    
    elif exercise == "pull_up":
        return random.choice(PULL_UP_GOOD if form_correct else PULL_UP_BAD)
    
    elif exercise == "shoulder_press":
        return random.choice(SHOULDER_PRESS_GOOD if form_correct else SHOULDER_PRESS_BAD)
    
    else:
        return "Keep going, you've got this!" if form_correct else "Focus on your form."
