import streamlit as st
import cv2
import time
from streamlit_option_menu import option_menu

# Page config
st.set_page_config(
    page_title="Welcome to Karsaathi!",
    page_icon="🤟",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Initialize user database in session state (fake DB)
if "user_db" not in st.session_state:
    st.session_state.user_db = {
        "Krishna Gupta": "12345",
        "Test User": "password"
    }

def login_page():
    st.markdown("<h1 style='text-align: center;'>🔐 Login to Karsaathi</h1>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login = st.button("Login")

    if login:
        if username.strip() == "" or password.strip() == "":
            st.warning("Please enter both username and password.")
            return
        if username in st.session_state.user_db and st.session_state.user_db[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome back, {username}!")
            st.experimental_rerun()
        else:
            st.error("Invalid credentials. Please try again.")

    st.markdown(
        """
        <p style='text-align: center; margin-top:20px;'>
        Don't have an account? 👉 <a href="#" onclick="window.location.reload()">Register here</a>
        </p>
        """, 
        unsafe_allow_html=True
    )

def register_page():
    st.markdown("<h1 style='text-align: center;'>📝 Register for Karsaathi</h1>", unsafe_allow_html=True)

    new_user = st.text_input("Choose a username")
    new_pass = st.text_input("Choose a password", type="password")
    register = st.button("Register")

    if register:
        if new_user.strip() == "" or new_pass.strip() == "":
            st.warning("Please enter both username and password.")
            return
        if new_user in st.session_state.user_db:
            st.error("Username already exists. Please choose another.")
        else:
            st.session_state.user_db[new_user] = new_pass
            st.success("Registered successfully! You can now log in.")
            st.experimental_rerun()

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

def show_learn():
    st.subheader("📚 Learn Indian Sign Language")
    st.markdown("Coming soon: Alphabet, Numbers, and Basic Words with visuals.")

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

        for i in range(200):
            ret, frame = cap.read()
            if not ret:
                st.warning("Failed to grab frame.")
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            FRAME_WINDOW.image(frame)
            time.sleep(0.03)

            if not st.session_state["camera_active"]:
                break

        cap.release()
    else:
        FRAME_WINDOW.info("Click 'Start Camera' to begin gesture recognition.")

def show_community():
    st.subheader("👥 Community")
    st.markdown("This will be a space to share, ask, and support each other. Coming soon!")

def show_about():
    st.subheader("ℹ About Karsaathi")
    st.markdown("""
    - Developed for Hackathons & Accessibility Projects  
    - Built with ❤ using Streamlit  
    - Aims to empower communication with ISL
    """)

def main_app():
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

def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login_or_register = st.radio("Choose:", ["Login", "Register"], horizontal=True)
        if login_or_register == "Login":
            login_page()
        else:
            register_page()
    else:
        st.sidebar.title(f"👋 Hello, {st.session_state.username}")
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.experimental_rerun()

        main_app()

if __name__ == "__main__":
    main()
