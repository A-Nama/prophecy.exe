import os
import streamlit as st
import numpy as np
import mediapipe as mp
import cv2
import random
from PIL import Image

# Suppress TensorFlow oneDNN logs
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# Initialize MediaPipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True)

# Load OpenCV face classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Define session states
if "stage" not in st.session_state:
    st.session_state["stage"] = "welcome"
if "captured_frame" not in st.session_state:
    st.session_state["captured_frame"] = None
if "prophecy" not in st.session_state:
    st.session_state["prophecy"] = ""

# Random prophecy generator based on facial features
def get_random_prophecy(feature, category):
    prophecies = {
        "face_shape": {
            "round": [
                "Your warmth draws people in like a beacon—someone is about to confess something big!",
                "The universe sees your kindness, and fate is preparing a surprise just for you.",
                "A familiar place will soon bring an unfamiliar opportunity. Pay attention!",
                "A heart-to-heart conversation is on the horizon—one that will change everything.",
                "Your intuition is stronger than ever. Trust it, especially this week."
            ],
            "oval": [
                "You’re adaptable, but soon you’ll be the one setting the pace. Ready?",
                "A chance encounter will open doors—walk through without hesitation.",
                "People are drawn to your energy, but someone in particular is watching closely.",
                "A challenge is coming, but you’re built for this. Watch how effortlessly you handle it.",
                "Your past and future are about to collide in the most unexpected way."
            ]
        },
        "eyes": {
            "large": [
                "Your eyes see more than most—someone’s true intentions will soon be revealed.",
                "A mystery has been unfolding in the background of your life. It’s about to take center stage.",
                "You notice the little things, but this time, it’s something big that needs your attention.",
                "Your next big move? It starts with a single glance in the right direction.",
                "Someone is keeping a secret from you—but their eyes will give them away."
            ],
            "almond": [
                "You have an old soul, and destiny respects that. Expect a moment of deep clarity soon.",
                "Something about the way you see the world is about to change—forever.",
                "Your focus is razor-sharp, and it’s guiding you toward something extraordinary.",
                "A hidden truth is waiting for you to uncover it. Will you be ready when the time comes?",
                "You’re about to see something—or someone—in a new light."
            ]
        },
        "nose": {
            "small": [
                "Your subtle approach to life is your secret weapon—watch how it pays off soon!",
                "Someone close to you admires your ability to stay calm under pressure.",
                "A quiet revelation is coming your way—listen carefully.",
                "Your patience is about to be rewarded in an unexpected way.",
                "A small gesture from you will have a massive impact on someone’s life."
            ],
            "prominent": [
                "Your presence is undeniable, and the universe is about to make that clear.",
                "A bold decision will soon be in your hands—trust your instincts.",
                "You’re about to command attention in a way you never expected.",
                "The spotlight is shifting towards you. Are you ready to shine?",
                "Your next opportunity is closer than you think—trust the signs."
            ]
        },
        "lips": {
            "full": [
                "Your words carry power—choose them wisely in an upcoming conversation.",
                "A deep conversation will bring you closer to someone unexpected.",
                "The way you express yourself is captivating—someone is hanging onto every word.",
                "Your charm is magnetic—get ready to attract exciting opportunities.",
                "A confession is coming your way—listen carefully."
            ],
            "thin": [
                "You have a sharp wit, and it’s about to come in handy.",
                "A carefully chosen word will shift everything in your favor.",
                "Someone underestimates you, but they’re about to be proven wrong.",
                "A long-held secret will soon come to light—are you prepared?",
                "Your ability to observe quietly gives you a powerful advantage."
            ]
        },
        "symmetry": {
            "high": [
                "You exude balance and harmony—people feel at ease around you.",
                "Your natural equilibrium makes you a magnet for success.",
                "Everything is aligning perfectly—trust the process.",
                "A moment of perfect clarity is coming your way.",
                "Your steady energy is about to attract someone important."
            ],
            "low": [
                "Your unique energy makes you unforgettable—embrace it!",
                "Someone is drawn to you because of your one-of-a-kind nature.",
                "Your differences are your strengths—watch how they pay off.",
                "A new perspective is about to change your path dramatically.",
                "Your unpredictable nature is your superpower—use it wisely."
            ]
        }
    }
    return random.choice(prophecies[feature][category])

# --------- Stage 1: Welcome Screen ---------
if st.session_state["stage"] == "welcome":
    st.title("🔮 Welcome to Prophecy.exe 🔮")
    st.markdown("**Let's unlock your destiny... Are you ready?**")
    if st.button("✨ What's My Prophecy?"):
        st.session_state["stage"] = "capture"
        st.rerun()

# --------- Stage 2: Capture Image ---------
elif st.session_state["stage"] == "capture":
    st.title("📸 Capture Your Face")
    st.markdown("**Look straight into the camera and take a snapshot!**")
    image_file = st.camera_input("Take a photo to reveal your fortune!")
    if image_file:
        img = Image.open(image_file)
        frame = np.array(img)
        st.session_state["captured_frame"] = frame
        st.session_state["stage"] = "analyze"
        st.rerun()

# --------- Stage 3: Face Analysis ---------
elif st.session_state["stage"] == "analyze":
    st.title("🔍 Analyzing Your Fate...")
    frame = st.session_state["captured_frame"]
    st.image(frame, caption="Your Captured Image", use_column_width=True)
    selected_features = {"face_shape": "oval", "eyes": "almond", "nose": "small", "lips": "full", "symmetry": "high"}
    st.session_state["prophecy"] = "\n".join([get_random_prophecy(k, v) for k, v in selected_features.items()])
    if st.button("🔮 Get My Prophecy"):
        st.session_state["stage"] = "prophecy"
        st.rerun()



# --------- Stage 4: Final Prophecy ---------
elif st.session_state["stage"] == "prophecy":
    st.title("🌟 Your Prophecy 🌟")
    st.image(st.session_state["captured_frame"], caption="Your Fortune Snapshot", use_column_width=True)
    prophecy_lines = st.session_state.get("prophecy", "").split("\n")
    for line in prophecy_lines:
        st.write(line)
    if st.button("🏠 Go Home"):
        st.session_state["stage"] = "welcome"
        st.rerun()


