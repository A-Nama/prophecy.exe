import streamlit as st
import cv2
import numpy as np
from deepface import DeepFace
from PIL import Image
import random
import time

# 🎨 Streamlit page config
st.set_page_config(page_title="AI Fortune Teller 🔮", layout="centered")

# 🖼️ Title & Intro
st.title("🔮 AI-Powered Digital Fortune Teller")
st.write("Capture your image, and let me reveal your fate... if you dare!")

# 📸 Capture image
image_file = st.camera_input("Take a photo if you're ready to face your future!")

# ✨ Fortune Messages Based on Emotion (with sass!)
fortunes = {
    "happy": [
        "Ooh honey, looks like someone's about to hit the jackpot. Stay fabulous!",
        "Lucky day? Oh, it’s more than that—it’s your time to shine!",
        "Things are about to get so good, you won’t know what hit you. Enjoy it, darling!",
        "You’ve got that glow, and fortune is here for it. Go get 'em, superstar!",
        "Success is knocking, and it’s wearing a crown—don’t leave it hanging!"
    ],
    "sad": [
        "Well, don’t cry. The universe is just setting you up for a glow-up, trust me.",
        "Tough times? Yeah, but guess what? You’re tougher. Keep going, superstar.",
        "Okay, things are a bit cloudy, but guess who’s about to bring the sunshine? You.",
        "Sad? Nah, you’re just in training for greatness. The big stuff is coming!",
        "Don’t sweat it, darling—this too shall pass. And then you'll shine like a star."
    ],
    "angry": [
        "Whoa there, hot stuff! Chill out, the universe is cooking up something amazing for you.",
        "I see that fire in your eyes. But listen, calm down—good things are coming, promise.",
        "You're a force of nature right now—just try to harness that power for good, okay?",
        "Angry? Hah, cute. But guess what? You're about to have a major breakthrough.",
        "Listen, I know you're mad, but guess who’s about to get some serious rewards? Yep, you."
    ],
    "neutral": [
        "Oh, look at you, sitting in the middle like you don't care. Well, guess what? The future has something wild in store!",
        "The universe is keeping it mysterious. It’s waiting for you to make the first move.",
        "You’re in for a surprise, babe. Life’s not gonna be boring, that's for sure!",
        "You’re just chillin’, huh? Enjoy it, the universe has plans, and they’re gonna be big.",
        "I see that poker face, but trust me, the future's got some serious drama coming your way."
    ]
}

# Mystical animation settings
def mystical_animation():
    for _ in range(5):
        st.markdown('<div style="animation: pulse 1s infinite;">✨</div>', unsafe_allow_html=True)
        time.sleep(0.5)

if image_file is not None:
    # Convert image to OpenCV format
    image = Image.open(image_file)
    image_np = np.array(image)

    # Save image temporarily
    temp_path = "temp.jpg"
    cv2.imwrite(temp_path, cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR))

    # 🎭 Emotion Detection
    try:
        analysis = DeepFace.analyze(img_path=temp_path, actions=['emotion'])
        emotion = analysis[0]['dominant_emotion']

        st.image(image, caption=f"Detected Emotion: {emotion.capitalize()}", use_column_width=True)

        # 🔮 Generate Fortune with Sass
        fortune = random.choice(fortunes.get(emotion, ["Oh, darling, the future is as mysterious as your mood."]))
        mystical_animation()  # Display mystical animation
        st.subheader(f"🔮 Your Fortune: {fortune}")

    except Exception as e:
        st.error("Oops! Couldn't analyze your face. Try again.")
