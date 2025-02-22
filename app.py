import streamlit as st
import cv2
import numpy as np
from deepface import DeepFace
from PIL import Image
import random

# 🎨 Streamlit page config
st.set_page_config(page_title="AI Fortune Teller 🔮", layout="centered")

# 🖼️ Title & Intro
st.title("🔮 AI-Powered Digital Fortune Teller")
st.write("Capture your image, and let AI predict your fortune!")

# 📸 Capture image
image_file = st.camera_input("Take a photo to reveal your fortune!")

# ✨ Fortune Messages Based on Emotion
fortunes = {
    "happy": ["A great opportunity is coming!", "Today is your lucky day!", "Happiness attracts success!"],
    "sad": ["Things will get better soon!", "Tough times don’t last, strong people do.", "You are stronger than you think!"],
    "angry": ["Take a deep breath—good things are coming.", "Let go of the negativity, and fortune will follow.", "Stay calm, great changes are ahead!"],
    "neutral": ["Your future is unwritten—embrace the mystery!", "Big surprises await!", "Life’s a journey, enjoy the ride!"]
}

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

        # 🔮 Generate Fortune
        fortune = random.choice(fortunes.get(emotion, ["The future is mysterious!"]))
        st.subheader(f"🔮 Your Fortune: {fortune}")

    except Exception as e:
        st.error("Oops! Couldn't analyze your face. Try again.")

