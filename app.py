import os
import time
import random
import numpy as np
import streamlit as st
from PIL import Image

# ------------------ SETTINGS ------------------
DEMO_MODE = True  # True = demo rules, False = use anomaly_model.pkl

# Default demo parameters
if "RANDOM_ANOMALY_PROB" not in st.session_state:
    st.session_state.RANDOM_ANOMALY_PROB = 0.20
if "MAX_CLICKS_PER_MIN" not in st.session_state:
    st.session_state.MAX_CLICKS_PER_MIN = 30
if "MIN_SAFE_SECONDS" not in st.session_state:
    st.session_state.MIN_SAFE_SECONDS = 8

ANOMALY_MESSAGE = "You've been detected as bot, you're out of this session."
VALID_USERNAME = "admin"
VALID_PASSWORD = "1234"
IMG_W, IMG_H = 300, 200

# ------------------ MODEL (optional) ------------------
model = None
if not DEMO_MODE:
    try:
        import joblib
        model = joblib.load("anomaly_model.pkl")
    except Exception as e:
        DEMO_MODE = True
        print("Falling back to DEMO_MODE:", e)

# ------------------ SESSION STATE ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "click_count" not in st.session_state:
    st.session_state.click_count = 0
if "scroll_depth" not in st.session_state:
    st.session_state.scroll_depth = 0
if "show_popup" not in st.session_state:
    st.session_state.show_popup = False
if "failed_logins" not in st.session_state:
    st.session_state.failed_logins = 0
if "account_locked_until" not in st.session_state:
    st.session_state.account_locked_until = None
if "session_RANDOM_ANOMALY_PROB" not in st.session_state:
    st.session_state.session_RANDOM_ANOMALY_PROB = None
if "session_MAX_CLICKS_PER_MIN" not in st.session_state:
    st.session_state.session_MAX_CLICKS_PER_MIN = None
if "session_MIN_SAFE_SECONDS" not in st.session_state:
    st.session_state.session_MIN_SAFE_SECONDS = None
if "cart" not in st.session_state:
    st.session_state.cart = []

# ------------------ ANOMALY DETECTION ------------------
def update_scroll_depth():
    if st.session_state.scroll_depth < 100:
        bump = random.randint(2, 8)
        st.session_state.scroll_depth = min(100, st.session_state.scroll_depth + bump)

def detect_anomaly():
    if st.session_state.start_time is None:
        return False
    elapsed = max(1, int(time.time() - st.session_state.start_time))
    clicks = st.session_state.click_count
    update_scroll_depth()
    scroll_norm = st.session_state.scroll_depth / 100.0

    if DEMO_MODE:
        prob = st.session_state.session_RANDOM_ANOMALY_PROB if st.session_state.session_RANDOM_ANOMALY_PROB is not None else st.session_state.RANDOM_ANOMALY_PROB
        max_clicks = st.session_state.session_MAX_CLICKS_PER_MIN if st.session_state.session_MAX_CLICKS_PER_MIN is not None else st.session_state.MAX_CLICKS_PER_MIN
        min_safe = st.session_state.session_MIN_SAFE_SECONDS if st.session_state.session_MIN_SAFE_SECONDS is not None else st.session_state.MIN_SAFE_SECONDS

        # avoid random-triggering immediately after login — require at least `min_safe` seconds
        if elapsed >= min_safe and random.random() < prob:
            return True
        clicks_per_min = (clicks / elapsed) * 60.0
        if clicks_per_min > max_clicks:
            return True
        if elapsed < min_safe and clicks >= 2:
            return True
        return False
    else:
        if model is None:
            return False
        features = np.array([[elapsed, clicks, scroll_norm]])
        try:
            pred = model.predict(features)[0]
            return pred == -1
        except Exception:
            return False

def logout():
    st.session_state.logged_in = False
    st.session_state.start_time = None
    st.session_state.click_count = 0
    st.session_state.scroll_depth = 0
    st.session_state.show_popup = False
    st.session_state.session_RANDOM_ANOMALY_PROB = None
    st.session_state.session_MAX_CLICKS_PER_MIN = None
    st.session_state.session_MIN_SAFE_SECONDS = None

# ------------------ UI THEME ------------------
st.set_page_config(page_title="SmartShop", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

/* App background with gradient */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: #1a202c !important;
    font-family: 'Poppins', 'Segoe UI', sans-serif;
}

/* Main content wrapper */
.main .block-container {
    padding: 2rem 1rem !important;
    max-width: 1400px !important;
    margin: 0 auto !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2d3748 0%, #1a202c 100%) !important;
    color: #f7fafc !important;
    box-shadow: 2px 0 10px rgba(0,0,0,0.1);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 2rem;
}

[data-testid="stSidebar"] .css-1offfwp,
[data-testid="stSidebar"] .css-qrbaxs,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] p {
    color: #f7fafc !important;
    font-weight: 500;
}

/* Widget labels */
.stMarkdown, .stSlider label, .stSlider span, .stSlider div,
.stTextInput label, .stTextInput input,
.stButton button, .stSelectbox label,
.stNumberInput label, .stNumberInput input,
.stCheckbox label, .stRadio label {
    color: #2d3748 !important;
    font-weight: 500 !important;
}

/* Text inputs */
.stTextInput input {
    background-color: #ffffff !important;
    border: 2px solid #e2e8f0 !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
    font-size: 15px !important;
    transition: all 0.3s ease !important;
}

.stTextInput input:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
}

/* Buttons */
.stButton button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 28px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.stButton button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
}

/* Headings */
.header {
    text-align: center;
    font-size: clamp(28px, 5vw, 42px);
    font-weight: 800;
    background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 1rem 0 0.75rem;
    text-shadow: 0 2px 10px rgba(0,0,0,0.1);
    letter-spacing: -0.5px;
}

.subtle {
    text-align: center;
    color: #e2e8f0;
    margin-bottom: 2rem;
    font-size: clamp(13px, 2vw, 15px);
    font-weight: 400;
}

/* Product cards */
.card {
    border: none;
    border-radius: 16px;
    padding: 12px 12px 20px 12px; /* less top padding */
    background: #ffffff;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    text-align: center;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    color: #1a202c;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
}

.card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    transform: scaleX(0);
    transition: transform 0.3s ease;
}

.card:hover::before {
    transform: scaleX(1);
}

.card:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 40px rgba(102, 126, 234, 0.25);
}

.card img {
    border-radius: 12px;
    margin-bottom: 12px;
}

.title {
    font-size: clamp(16px, 2.5vw, 19px);
    font-weight: 700;
    margin-top: 12px;
    color: #2d3748;
    letter-spacing: -0.3px;
}

.price {
    font-size: clamp(18px, 3vw, 22px);
    font-weight: 800;
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 8px 0 16px;
}

/* Footer */
.footer {
    text-align: center;
    margin-top: 3rem;
    padding: 1.5rem;
    font-size: 13px;
    color: #e2e8f0;
    font-weight: 500;
    background: rgba(255,255,255,0.1);
    border-radius: 12px;
    backdrop-filter: blur(10px);
}

/* Success/Error messages */
.stSuccess, .stError, .stWarning, .stInfo {
    border-radius: 12px !important;
    padding: 1rem !important;
    font-weight: 500 !important;
}

/* Responsive layout */
@media (max-width: 1024px) {
    .main .block-container {
        padding: 1.5rem 1rem !important;
    }
}

@media (max-width: 768px) {
    .main .block-container {
        padding: 1rem 0.5rem !important;
    }

    .card {
        padding: 16px;
        margin-bottom: 1rem;
    }

    .header {
        margin: 0.5rem 0;
    }

    .subtle {
        margin-bottom: 1.5rem;
    }
}

@media (max-width: 480px) {
    .stButton button {
        width: 100%;
        padding: 10px 20px !important;
    }

    .card {
        padding: 12px;
    }
}

/* Sliders */
.stSlider {
    padding: 1rem 0;
}

.stSlider > div > div > div {
    background-color: #667eea !important;
}

/* Login container styling */
.login-container {
    max-width: 450px;
    margin: 2rem auto;
    padding: 2.5rem;
    background: rgba(255,255,255,0.95);
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    backdrop-filter: blur(10px);
}
</style>
""", unsafe_allow_html=True)

# ------------------ DATA ------------------
PRODUCTS = [
    ("Laptop", "₹55,000", "images/laptop.jpg"),
    ("Smartphone", "₹25,000", "images/phone.jpg"),
    ("Smart TV", "₹40,000", "images/tv.jpg"),
    ("Headphones", "₹2,000", "images/headphones.jpg"),
    ("Shoes", "₹3,500", "images/shoes.jpg"),
    ("Smart Watch", "₹6,000", "images/watch.jpg"),
    ("Camera", "₹35,000", "images/camera.jpg"),
    ("Tablet", "₹20,000", "images/tablet.jpg"),
    ("Refrigerator", "₹30,000", "images/fridge.jpg"),
    ("Microwave Oven", "₹12,000", "images/microwave.jpg"),
]

# ------------------ PAGES ------------------
def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
        st.markdown("<div class='header'>Welcome to SmartShop</div>", unsafe_allow_html=True)
        st.markdown("<div class='subtle'>Sign in to access exclusive deals</div>", unsafe_allow_html=True)

        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

        if st.session_state.account_locked_until and time.time() < st.session_state.account_locked_until:
            remaining = int(st.session_state.account_locked_until - time.time())
            st.error(f"Account temporarily locked. Try again in {remaining} seconds.")
            return

        with st.container():
            st.markdown("""
            <div style='background: rgba(255,255,255,0.95); padding: 40px; border-radius: 20px; box-shadow: 0 20px 60px rgba(0,0,0,0.3);'>
            </div>
            """, unsafe_allow_html=True)

            username = st.text_input("Username", placeholder="Enter your username", key="login_username")
            password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

            if st.button("Sign In", use_container_width=True):
                if username == VALID_USERNAME and password == VALID_PASSWORD:
                    st.session_state.logged_in = True
                    st.session_state.start_time = time.time()
                    st.session_state.click_count = 0
                    st.session_state.scroll_depth = 0
                    st.session_state.failed_logins = 0
                    st.session_state.account_locked_until = None
                    st.experimental_rerun()
                else:
                    st.session_state.failed_logins += 1
                    remaining_attempts = 3 - st.session_state.failed_logins
                    if remaining_attempts > 0:
                        st.warning(f"Invalid credentials. {remaining_attempts} attempt(s) remaining.")
                    else:
                        st.session_state.account_locked_until = time.time() + 30
                        st.error("Too many failed attempts. Account locked for 30 seconds.")

        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

def shop_page():
    # Main container with proper spacing
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # Header section with gradient background
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; border-radius: 20px; margin-bottom: 30px; text-align: center;'>
        <h1 style='color: white; font-size: 48px; font-weight: 900; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>SmartShop</h1>
        <p style='color: rgba(255,255,255,0.9); font-size: 18px; margin: 10px 0 0 0; font-weight: 500;'>Premium Electronics & Accessories</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation bar
    nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
    with nav_col2:
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            logout()
            st.experimental_rerun()
    
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    
    # Products grid with enhanced styling
    st.markdown("### 🛍 Featured Products")
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    
    # Create responsive grid
    cols = st.columns(3)
    for i, (name, price, img_path) in enumerate(PRODUCTS):
        with cols[i % 3]:
            # Start card container (no extra div above image)
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            
            # Product image (uniform size, no extra space above)
            if os.path.exists(img_path):
                img = Image.open(img_path).resize((IMG_W, IMG_H))
                st.image(img, width=IMG_W)
            else:
                # If image missing, just show product name as fallback (no white bar)
                st.markdown(f"<div class='title'>{name}</div>", unsafe_allow_html=True)

            # Product title and price
            st.markdown(f"<div class='title'>{name}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='price'>{price}</div>", unsafe_allow_html=True)

            # Add to Cart button
            if st.button(f"Add to Cart", key=f"buy_{i}", use_container_width=True):
                st.session_state.click_count += 1
                st.session_state.cart.append((name, price))
                st.success(f"{name} added to cart!")
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Footer section
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='
        text-align: center; 
        margin-top: 50px; 
        font-size: 14px; 
        color: #4a5568;
        background: rgba(255,255,255,0.1);
        padding: 20px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
    '>
        <strong>© 2025 SmartShop</strong> – Advanced Anomaly Detection System
    </div>
    """, unsafe_allow_html=True)

    if detect_anomaly():
        st.session_state.show_popup = True

    if st.session_state.show_popup:
        # Overlay and modal
        st.markdown(f"""
        <style>
        .custom-overlay {{
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(0,0,0,0.65);
            backdrop-filter: blur(8px);
            z-index: 9999;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .custom-modal {{
            background: white;
            padding: 40px 30px 30px 30px;
            border-radius: 20px;
            text-align: center;
            max-width: 420px;
            width: 90vw;
            box-shadow: 0 25px 50px rgba(0,0,0,0.4);
            color: #1a202c;
            font-family: "Poppins", sans-serif;
            border-top: 5px solid #f5576c;
            animation: slideUp 0.4s ease;
        }}
        @keyframes slideUp {{
            from {{
                transform: translateY(50px);
                opacity: 0;
            }}
            to {{
                transform: translateY(0);
                opacity: 1;
            }}
        }}
        .custom-modal p {{
            font-size: 20px;
            font-weight: 700;
            margin-bottom: 24px;
            line-height: 1.6;
        }}
        </style>
        <div class="custom-overlay">
            <div class="custom-modal">
                <p>{ANOMALY_MESSAGE}</p>
                <form>
                    <button type="submit" style="
                        margin-top: 18px;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        border: none;
                        border-radius: 12px;
                        padding: 12px 28px;
                        font-weight: 600;
                        font-size: 16px;
                        cursor: pointer;
                        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                    ">OK</button>
                </form>
            </div>
        </div>
        """, unsafe_allow_html=True)
        # Use Streamlit's form submit workaround
        if st.form_submit_button("OK", key="anomaly_ok"):
            logout()
            st.experimental_rerun()
        st.stop()

    if st.session_state.show_popup:
        # Use Streamlit columns to center the modal and button
        st.markdown("""
        <style>
        .blur-bg {
            filter: blur(8px) !important;
            pointer-events: none !important;
            user-select: none !important;
        }
        </style>
        """, unsafe_allow_html=True)
        # Blur everything except the modal
        st.markdown('<div class="blur-bg">', unsafe_allow_html=True)
        # Render the rest of your page here if needed (optional)
        st.markdown('</div>', unsafe_allow_html=True)

        # Centered modal using columns
        modal_col1, modal_col2, modal_col3 = st.columns([2, 3, 2])
        with modal_col2:
            st.markdown("""
            <div style='
                background: white;
                padding: 40px 30px 30px 30px;
                border-radius: 20px;
                text-align: center;
                max-width: 420px;
                margin: 80px auto 0 auto;
                box-shadow: 0 25px 50px rgba(0,0,0,0.4);
                color: #1a202c;
                font-family: "Poppins", sans-serif;
                border-top: 5px solid #f5576c;
            '>
                <p style='font-size: 20px; font-weight: 700; margin-bottom: 24px; line-height: 1.6;'>{}</p>
            </div>
            """.format(ANOMALY_MESSAGE), unsafe_allow_html=True)
            if st.button("OK", key="anomaly_ok"):
                logout()
                st.experimental_rerun()
    st.stop()

    # Cart section
    st.markdown("### Your Cart")
    if st.session_state.cart:
        for item_name, item_price in st.session_state.cart:
            st.markdown(f"- **{item_name}** — {item_price}")
    else:
        st.info("Your cart is empty.")

def settings_page():
    st.markdown("<div class='header'>Bot Detection System</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtle'>Configure anomaly detection parameters for this session</div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        <div style='background: rgba(255,255,255,0.95); padding: 30px; border-radius: 16px; margin-bottom: 20px;'>
            <h3 style='color: #2d3748; margin-top: 0; font-size: 22px;'>How Bot Detection Works</h3>
            <p style='color: #4a5568; line-height: 1.8; font-size: 15px;'>
                Our system analyzes user behavior in real-time to identify suspicious bot-like patterns.
                The detection algorithm monitors three key parameters:
            </p>
            <ul style='color: #4a5568; line-height: 2; font-size: 14px;'>
                <li><strong>Click Speed:</strong> Measures clicks per minute to detect automated clicking</li>
                <li><strong>Interaction Timing:</strong> Tracks time between actions to identify unnatural speed</li>
                <li><strong>Random Detection:</strong> Simulates probabilistic anomaly triggers for testing</li>
            </ul>
            <p style='color: #4a5568; line-height: 1.8; font-size: 14px; margin-bottom: 0;'>
                When bot-like behavior is detected, the user session is immediately terminated to protect the platform.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Detection Parameters")
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        current_prob = st.session_state.session_RANDOM_ANOMALY_PROB if st.session_state.session_RANDOM_ANOMALY_PROB is not None else st.session_state.RANDOM_ANOMALY_PROB
        current_max_clicks = st.session_state.session_MAX_CLICKS_PER_MIN if st.session_state.session_MAX_CLICKS_PER_MIN is not None else st.session_state.MAX_CLICKS_PER_MIN
        current_min_safe = st.session_state.session_MIN_SAFE_SECONDS if st.session_state.session_MIN_SAFE_SECONDS is not None else st.session_state.MIN_SAFE_SECONDS

        new_prob = st.slider(
            "Random Anomaly Probability (%)",
            0, 100, int(current_prob * 100),
            help="Probability of triggering random bot detection on each interaction"
        ) / 100.0

        new_max_clicks = st.slider(
            "Maximum Clicks Per Minute",
            5, 100, current_max_clicks,
            help="Maximum allowed clicks per minute before flagging as bot"
        )

        new_min_safe = st.slider(
            "Minimum Safe Interval (seconds)",
            1, 30, current_min_safe,
            help="Minimum time required between clicks to avoid bot detection"
        )

        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Apply Settings for This Session", use_container_width=True):
                st.session_state.session_RANDOM_ANOMALY_PROB = new_prob
                st.session_state.session_MAX_CLICKS_PER_MIN = new_max_clicks
                st.session_state.session_MIN_SAFE_SECONDS = new_min_safe
                st.success("✓ Settings applied to current session only!")
                st.info("Note: These settings will reset to default when you logout.")

        with col_btn2:
            if st.button("Reset to Default", use_container_width=True):
                st.session_state.session_RANDOM_ANOMALY_PROB = None
                st.session_state.session_MAX_CLICKS_PER_MIN = None
                st.session_state.session_MIN_SAFE_SECONDS = None
                st.success("✓ Reset to default settings!")
                st.experimental_rerun()

    with col2:
        st.markdown("""
        <div style='background: rgba(255,255,255,0.95); padding: 25px; border-radius: 16px; margin-bottom: 20px;'>
            <h4 style='color: #2d3748; margin-top: 0; font-size: 18px;'>Current Status</h4>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.start_time:
            elapsed = int(time.time() - st.session_state.start_time)
            clicks_per_min = (st.session_state.click_count / max(elapsed, 1)) * 60.0

            st.metric("Session Duration", f"{elapsed}s")
            st.metric("Total Clicks", st.session_state.click_count)
            st.metric("Clicks/Min", f"{clicks_per_min:.1f}")
            st.metric("Scroll Progress", f"{st.session_state.scroll_depth}%")

            st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

            active_prob = st.session_state.session_RANDOM_ANOMALY_PROB if st.session_state.session_RANDOM_ANOMALY_PROB is not None else st.session_state.RANDOM_ANOMALY_PROB
            active_max = st.session_state.session_MAX_CLICKS_PER_MIN if st.session_state.session_MAX_CLICKS_PER_MIN is not None else st.session_state.MAX_CLICKS_PER_MIN
            active_min = st.session_state.session_MIN_SAFE_SECONDS if st.session_state.session_MIN_SAFE_SECONDS is not None else st.session_state.MIN_SAFE_SECONDS

            st.markdown(f"""
            <div style='background: rgba(102, 126, 234, 0.1); padding: 15px; border-radius: 12px; border-left: 4px solid #667eea;'>
                <p style='color: #2d3748; font-size: 13px; margin: 0; line-height: 1.8;'>
                    <strong>Active Thresholds:</strong><br/>
                    Random: {int(active_prob * 100)}%<br/>
                    Max Clicks: {active_max}/min<br/>
                    Min Interval: {active_min}s
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No active session")

        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div style='background: rgba(245, 87, 108, 0.1); padding: 20px; border-radius: 12px; border-left: 4px solid #f5576c;'>
            <h5 style='color: #2d3748; margin-top: 0; font-size: 15px;'>⚠ Warning</h5>
            <p style='color: #4a5568; font-size: 13px; line-height: 1.6; margin: 0;'>
                Lower thresholds increase bot detection sensitivity.
                Settings are session-specific and reset on logout.
            </p>
        </div>
        """, unsafe_allow_html=True)

# ------------------ ROUTER ------------------
if st.session_state.logged_in:
    page = st.sidebar.radio("Navigation", ["Shop", "Anomaly Settings"])
    if page == "Shop":
        shop_page()
    elif page == "Anomaly Settings":
        settings_page()
else:
    login_page()