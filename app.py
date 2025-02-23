import os
import streamlit as st
import numpy as np
import mediapipe as mp
import cv2
from PIL import Image

# Suppress TensorFlow oneDNN logs (No longer needed since we removed DeepFace)
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# Initialize MediaPipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True)

# Load OpenCV face classifier for emotion detection (FOSS-friendly replacement for DeepFace)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Define session states
if "stage" not in st.session_state:
    st.session_state["stage"] = "welcome"
if "captured_frame" not in st.session_state:
    st.session_state["captured_frame"] = None

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

    # 📸 Streamlit Camera Input (fixes glitch)
    image_file = st.camera_input("Take a photo to reveal your fortune!")

    if image_file:
        img = Image.open(image_file)
        frame = np.array(img)

        # Save image to session state
        st.session_state["captured_frame"] = frame
        st.session_state["stage"] = "reading"
        st.rerun()

# --------- Stage 3: Face Analysis & Reading ---------
elif st.session_state["stage"] == "reading":
    st.title("🔍 Analyzing Your Fate...")

    frame = st.session_state["captured_frame"]
    if frame is None:
        st.error("No image found! Go back and try again.")
        if st.button("🏠 Home"):
            st.session_state["stage"] = "welcome"
            st.rerun()

    st.image(frame, caption="Your Captured Image", use_column_width=True)

    # Convert image to grayscale for OpenCV processing
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # Detect faces using OpenCV
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) == 0:
        st.error("No face detected! Try capturing another photo.")
        if st.button("🔁 Retake Photo"):
            st.session_state["stage"] = "capture"
            st.rerun()

    # Process face mesh analysis
    results = face_mesh.process(frame)
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            h, w, _ = frame.shape
            face_pts = np.array([(int(p.x * w), int(p.y * h)) for p in face_landmarks.landmark])

            # Symmetry Check
            left_side = face_pts[:len(face_pts)//2]
            right_side = face_pts[len(face_pts)//2:]
            asymmetry_score = np.sum(np.abs(left_side[:, 0] - np.flip(right_side[:, 0])))

            symmetry_result = (
                "✨ An exciting adventure is on the horizon! New people and experiences are coming your way—embrace them!" 
                if asymmetry_score < 15 else 
                "🔮 A moment of clarity awaits you! Soon, you'll uncover hidden insights that change your perspective."
                if asymmetry_score <30 else
                "💖 A deep connection will soon surprise you! Someone in your life appreciates you more than you realize."
            )

            # Face Shape Analysis
            forehead_width = np.linalg.norm(face_pts[10] - face_pts[338])
            jaw_width = np.linalg.norm(face_pts[152] - face_pts[172])
            face_height = np.linalg.norm(face_pts[10] - face_pts[152])

            if face_height / forehead_width > 1.5:
                face_shape = "🧠 Hard work pays off soon—your dedication is about to lead to big rewards!"
            elif jaw_width > forehead_width:
                face_shape = "🔥 A bold decision will shape your future—trust yourself to make the right call!"
            elif forehead_width > jaw_width:
                face_shape = "🌿 Your kindness will bring unexpected opportunities—stay open to new connections!"
            else:
                face_shape = "💖 Balance is key! A moment of harmony is coming your way—trust the process."

            # Eyes, Nose, Lips Analysis
            eye_distance = np.linalg.norm(face_pts[33] - face_pts[263])
            eye_result = (
                "🔥 Something—or someone—is about to ignite your excitement! Whether it's a new idea, an unexpected adventure, or a deep conversation, your open heart will draw in something truly special. Follow your instincts, embrace the moment, and let your passion lead the way!" 
                if eye_distance > forehead_width * 0.4 else 
                "🔎 You’re about to notice something others overlook—trust your sharp instincts! A small but important detail will reveal itself, helping you solve a problem or gain an advantage. Stay focused, because this insight could put you one step ahead in ways you never expected!"
            )

            nose_width = np.linalg.norm(face_pts[2] - face_pts[331])
            nose_result = (
                "🚀 Your ambition is about to open doors! In the coming days, you may find yourself in a situation where your leadership skills are put to the test—trust yourself, because this moment could shape your path to success. Stay bold, stay confident—the universe is setting the stage for your next big move!"
                if nose_width > forehead_width * 0.3 else
                "🌸 Your kindness never goes unnoticed, and soon, someone will truly appreciate your warmth and generosity. Whether it’s a heartfelt conversation or a quiet moment of support, your gentle nature will leave a lasting impact. The universe is reminding you: your compassion is a gift—share it freely!"
            )

            mouth_width = np.linalg.norm(face_pts[61] - face_pts[291])
            lip_thickness = np.linalg.norm(face_pts[13] - face_pts[14])
            lips_result = (
                "💋 Get ready for laughter, love, and heartfelt connections! In the coming days, a meaningful conversation or a shared experience will bring warmth to your heart. Your openness draws people in—embrace the moments of joy, because the universe is sending you beautiful energy!"
                if lip_thickness > 5 else 
                "🌙 Your independence is about to pay off in a big way. Soon, you’ll accomplish something on your own terms—whether it’s solving a problem, reaching a goal, or gaining clarity on a situation. Trust yourself, because your inner strength is leading you exactly where you need to be!"
            )

            # Save the fortune reading
            st.session_state["fortune"] = {
                "symmetry": symmetry_result,
                "face_shape": face_shape,
                "eyes": eye_result,
                "nose": nose_result,
                "lips": lips_result
            }

    # Proceed to Prophecy
    if st.button("🔮 Get My Prophecy"):
        st.session_state["stage"] = "prophecy"
        st.rerun()

# --------- Stage 4: Final Prophecy ---------
elif st.session_state["stage"] == "prophecy":
    st.title("🌟 Your Prophecy 🌟")

    st.image(st.session_state["captured_frame"], caption="Your Fortune Snapshot", use_column_width=True)

    fortune = st.session_state.get("fortune", {})

    st.write(fortune.get("symmetry", ""))
    st.write(fortune.get("face_shape", ""))
    st.write(fortune.get("eyes", ""))
    st.write(fortune.get("nose", ""))
    st.write(fortune.get("lips", ""))

    if st.button("🏠 Go Home"):
        st.session_state["stage"] = "welcome"
        st.rerun()
