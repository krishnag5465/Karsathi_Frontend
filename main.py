# app.py

import streamlit as st
import cv2
from streamlit_option_menu import option_menu

# Page config
st.set_page_config(
    page_title="Welcome to Karsaathi!",
    page_icon="🤟",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Sidebar menu using option_menu
def sidebar_menu():
    with st.sidebar:
        selected = option_menu(
            "Main Menu",
            ["Home", "Learn Signs", "Translate", "Community", "About"],
            icons=['house', 'book', 'camera', 'people', 'info-circle'],
            menu_icon="cast",
            default_index=0,
        )
    return selected

# Home Page
def show_home():
    st.title("🤟 Welcome to Karsaathi!")
    st.markdown("""
    *Karsaathi* helps bridge communication between the Deaf/Mute community and others using Indian Sign Language (ISL).

    ### 🌟 Features:
    - 🧠 Learn ISL alphabets and words
    - 📷 Real-time Gesture Recognition (via webcam)
    - 💬 Translate signs into English / Gujarati
    - 👥 Join and share in our Community
    """)
    st.image("https://cdn-icons-png.flaticon.com/512/3050/3050525.png", width=200)

# Placeholder - Learn Signs Page
def show_learn():
    st.subheader("📚 Learn Indian Sign Language")
    st.markdown("Coming soon: Alphabet, Numbers, and Basic Words with visuals.")

# Translate Page with Webcam Feed
import time  # Make sure this is at the top of your file

def show_translate():
    st.subheader("📷 Real-Time Gesture Recognition")

    if "camera_active" not in st.session_state:
        st.session_state["camera_active"] = False

    toggle = st.button("Start Camera" if not st.session_state["camera_active"] else "Stop Camera")

    if toggle:
        st.session_state["camera_active"] = not st.session_state["camera_active"]

    FRAME_WINDOW = st.empty()

    if st.session_state["camera_active"]:
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            st.error("Unable to access the camera.")
            return

        # Stream camera for a few seconds (simulate real-time)
        for i in range(200):
            ret, frame = cap.read()
            if not ret:
                st.warning("Failed to grab frame.")
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            FRAME_WINDOW.image(frame)
            time.sleep(0.03)

            # Stop early if user turns off camera
            if not st.session_state["camera_active"]:
                break

        cap.release()
    else:
        FRAME_WINDOW.info("Click 'Start Camera' to begin gesture recognition.")

def show_community():
    st.subheader("👥 Community")
    st.markdown("This will be a space to share, ask, and support each other. Coming soon!")

# About Page
def show_about():
    st.subheader("ℹ About Karsaathi")
    st.markdown("""
    - Developed for Hackathons & Accessibility Projects  
    - Built with ❤ using Streamlit  
    - Aims to empower communication with ISL
    """)

# Main function
def main():
    selected = sidebar_menu()

    if selected == "Home":
        show_home()
    elif selected == "Learn Signs":
        show_learn()
    elif selected == "Translate":
        show_translate()
    elif selected == "Community":
        show_community()
    elif selected == "About":
        show_about()

if __name__ == "__main__":
    main()