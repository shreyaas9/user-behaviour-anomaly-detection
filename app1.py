
# import os
# import time
# import random
# import numpy as np
# import streamlit as st
# from PIL import Image

# # ------------------ SETTINGS ------------------
# DEMO_MODE = True  # True = demo rules, False = use anomaly_model.pkl

# # Default demo parameters
# if "RANDOM_ANOMALY_PROB" not in st.session_state:
#     st.session_state.RANDOM_ANOMALY_PROB = 0.20
# if "MAX_CLICKS_PER_MIN" not in st.session_state:
#     st.session_state.MAX_CLICKS_PER_MIN = 30
# if "MIN_SAFE_SECONDS" not in st.session_state:
#     st.session_state.MIN_SAFE_SECONDS = 8

# ANOMALY_MESSAGE = "You've been detected as bot, you're out of this session."
# VALID_USERNAME = "admin"
# VALID_PASSWORD = "1234"
# IMG_W, IMG_H = 300, 200

# # ------------------ MODEL (optional) ------------------
# model = None
# if not DEMO_MODE:
#     try:
#         import joblib
#         model = joblib.load("anomaly_model.pkl")
#     except Exception as e:
#         DEMO_MODE = True
#         print("Falling back to DEMO_MODE:", e)

# # ------------------ SESSION STATE ------------------
# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False
# if "start_time" not in st.session_state:
#     st.session_state.start_time = None
# if "click_count" not in st.session_state:
#     st.session_state.click_count = 0
# if "scroll_depth" not in st.session_state:
#     st.session_state.scroll_depth = 0
# if "show_popup" not in st.session_state:
#     st.session_state.show_popup = False
# if "failed_logins" not in st.session_state:
#     st.session_state.failed_logins = 0
# if "account_locked_until" not in st.session_state:
#     st.session_state.account_locked_until = None

# # ------------------ ANOMALY DETECTION ------------------
# def update_scroll_depth():
#     if st.session_state.scroll_depth < 100:
#         bump = random.randint(2, 8)
#         st.session_state.scroll_depth = min(100, st.session_state.scroll_depth + bump)

# def detect_anomaly():
#     if st.session_state.start_time is None:
#         return False
#     elapsed = max(1, int(time.time() - st.session_state.start_time))
#     clicks = st.session_state.click_count
#     update_scroll_depth()
#     scroll_norm = st.session_state.scroll_depth / 100.0

#     if DEMO_MODE:
#         if random.random() < st.session_state.RANDOM_ANOMALY_PROB:
#             return True
#         clicks_per_min = (clicks / elapsed) * 60.0
#         if clicks_per_min > st.session_state.MAX_CLICKS_PER_MIN:
#             return True
#         if elapsed < st.session_state.MIN_SAFE_SECONDS and clicks >= 2:
#             return True
#         return False
#     else:
#         if model is None:
#             return False
#         features = np.array([[elapsed, clicks, scroll_norm]])
#         try:
#             pred = model.predict(features)[0]
#             return pred == -1
#         except Exception:
#             return False

# def logout():
#     st.session_state.logged_in = False
#     st.session_state.start_time = None
#     st.session_state.click_count = 0
#     st.session_state.scroll_depth = 0
#     st.session_state.show_popup = False

# # ------------------ UI THEME ------------------
# st.set_page_config(page_title="SmartShop", layout="wide")
# # st.markdown("""
# # <style>
# # /* App background */
# # [data-testid="stAppViewContainer"] {
# #     background-color: #f4f6f9 !important;
# #     color: #111827 !important;
# #     font-family: 'Inter', 'Segoe UI', Roboto, Arial, sans-serif;
# # }

# # /* Sidebar */
# # [data-testid="stSidebar"] {
# #     background-color: #1f2937 !important;
# #     color: #f9fafb !important;
# # }
# # [data-testid="stSidebar"] .css-1offfwp, 
# # [data-testid="stSidebar"] .css-qrbaxs {
# #     color: #f9fafb !important;
# #     font-weight: 600;
# # }

# # /* Make all widget labels readable */
# # .stMarkdown, .stSlider label, .stSlider span, .stSlider div, 
# # .stTextInput label, .stTextInput input,
# # .stButton button, .stSelectbox label,
# # .stNumberInput label, .stNumberInput input,
# # .stCheckbox label, .stRadio label {
# #     color: #111827 !important;
# #     font-weight: 500 !important;
# # }

# # /* Headings */
# # .header {
# #     text-align:center;
# #     font-size: 32px;
# #     font-weight: 800;
# #     color: #1e40af;
# #     margin: 8px 0 12px;
# # }
# # .subtle {
# #     text-align:center;
# #     color:#374151;
# #     margin-bottom: 24px;
# #     font-size: 14px;
# # }

# # /* Product cards */
# # .card {
# #     border: 1px solid #e5e7eb;
# #     border-radius: 12px;
# #     padding: 16px;
# #     background: #fff;
# #     box-shadow: 0 2px 6px rgba(0,0,0,0.06);
# #     text-align: center;
# #     transition: transform .2s ease, box-shadow .2s ease;
# #     color: #111827;
# # }
# # .card:hover {
# #     transform: translateY(-4px);
# #     box-shadow: 0 8px 20px rgba(0,0,0,0.12);
# # }
# # .title {
# #     font-size: 18px;
# #     font-weight: 600;
# #     margin-top: 10px;
# # }
# # .price {
# #     font-size: 16px;
# #     font-weight: 700;
# #     color: #d32f2f;
# #     margin: 6px 0 12px;
# # }

# # /* Footer */
# # .footer {
# #     text-align:center;
# #     margin-top:40px;
# #     font-size: 13px;
# #     color:#6b7280;
# # }
# # </style>
# # """, unsafe_allow_html=True)
# st.markdown("""
# <style>
# /* App background */
# [data-testid="stAppViewContainer"] {
#     background: linear-gradient(135deg, #f9fafb, #eef2f7);
#     color: #111827 !important;
#     font-family: 'Inter', 'Segoe UI', Roboto, Arial, sans-serif;
# }

# /* Sidebar */
# [data-testid="stSidebar"] {
#     background: rgba(31,41,55,0.95) !important;
#     color: #f9fafb !important;
#     backdrop-filter: blur(8px);
#     border-right: 1px solid #374151;
# }
# [data-testid="stSidebar"] .css-1offfwp, 
# [data-testid="stSidebar"] .css-qrbaxs {
#     color: #f9fafb !important;
#     font-weight: 600;
# }

# /* Headings */
# .header {
#     text-align:center;
#     font-size: 34px;
#     font-weight: 800;
#     color: #1d4ed8;
#     margin: 8px 0 16px;
# }
# .subtle {
#     text-align:center;
#     color:#4b5563;
#     margin-bottom: 24px;
#     font-size: 15px;
# }

# /* Product cards */
# .card {
#     border: 1px solid #e5e7eb;
#     border-radius: 14px;
#     padding: 18px;
#     background: #ffffff;
#     box-shadow: 0 3px 10px rgba(0,0,0,0.06);
#     text-align: center;
#     transition: transform .25s ease, box-shadow .25s ease;
# }
# .card:hover {
#     transform: translateY(-6px) scale(1.02);
#     box-shadow: 0 12px 24px rgba(0,0,0,0.15);
# }
# .title {
#     font-size: 19px;
#     font-weight: 600;
#     margin-top: 10px;
#     color: #111827;
# }
# .price {
#     font-size: 16px;
#     font-weight: 700;
#     color: #dc2626;
#     margin: 8px 0 14px;
# }

# /* Buttons */
# .stButton button {
#     background: linear-gradient(90deg, #2563eb, #3b82f6);
#     color: white !important;
#     font-weight: 600 !important;
#     border: none;
#     border-radius: 8px;
#     padding: 10px 18px;
#     transition: all 0.2s ease;
# }
# .stButton button:hover {
#     background: linear-gradient(90deg, #1d4ed8, #2563eb);
#     transform: translateY(-2px);
#     box-shadow: 0 4px 12px rgba(37,99,235,0.4);
# }

# /* Modal overlay */
# .overlay {
#     position: fixed;
#     top: 0; left: 0; right: 0; bottom: 0;
#     background: rgba(0,0,0,0.55);
#     backdrop-filter: blur(6px);
#     display: flex;
#     justify-content: center;
#     align-items: center;
#     z-index: 9999;
# }
# .modal {
#     background: #ffffff;
#     padding: 28px;
#     border-radius: 14px;
#     text-align: center;
#     max-width: 420px;
#     box-shadow: 0 0 24px rgba(0,0,0,0.25);
#     color: #111827;
#     font-family: Inter, sans-serif;
# }
# .modal button {
#     padding: 10px 20px;
#     border: none;
#     border-radius: 10px;
#     background: #ef4444;
#     color: white;
#     font-weight: bold;
#     cursor: pointer;
#     transition: all .2s ease;
# }
# .modal button:hover {
#     background: #dc2626;
#     transform: scale(1.05);
# }

# /* Footer */
# .footer {
#     text-align:center;
#     margin-top:50px;
#     font-size: 13px;
#     color:#6b7280;
# }
# </style>
# """, unsafe_allow_html=True)

# # ------------------ DATA ------------------
# PRODUCTS = [
#     ("Laptop", "₹55,000", "images/laptop.jpg"),
#     ("Smartphone", "₹25,000", "images/phone.jpg"),
#     ("Smart TV", "₹40,000", "images/tv.jpg"),
#     ("Headphones", "₹2,000", "images/headphones.jpg"),
#     ("Shoes", "₹3,500", "images/shoes.jpg"),
#     ("Smart Watch", "₹6,000", "images/watch.jpg"),
#     ("Camera", "₹35,000", "images/camera.jpg"),
#     ("Tablet", "₹20,000", "images/tablet.jpg"),
#     ("Refrigerator", "₹30,000", "images/fridge.jpg"),
#     ("Microwave Oven", "₹12,000", "images/microwave.jpg"),
# ]

# # ------------------ PAGES ------------------
# def login_page():
#     st.markdown("<div class='header'>SmartShop Sign In</div>", unsafe_allow_html=True)
#     st.markdown("<div class='subtle'>Use your credentials to continue</div>", unsafe_allow_html=True)

#     if st.session_state.account_locked_until and time.time() < st.session_state.account_locked_until:
#         remaining = int(st.session_state.account_locked_until - time.time())
#         st.error(f" Account locked. Try again in {remaining} seconds.")
#         return

#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")

#     if st.button("Login"):
#         if username == VALID_USERNAME and password == VALID_PASSWORD:
#             st.session_state.logged_in = True
#             st.session_state.start_time = time.time()
#             st.session_state.click_count = 0
#             st.session_state.scroll_depth = 0
#             st.session_state.failed_logins = 0
#             st.session_state.account_locked_until = None
#         else:
#             st.session_state.failed_logins += 1
#             remaining_attempts = 3 - st.session_state.failed_logins
#             if remaining_attempts > 0:
#                 st.warning(f"Wrong credentials. {remaining_attempts} attempt(s) left.")
#             else:
#                 st.session_state.account_locked_until = time.time() + 30
#                 st.error("Too many failed attempts. Locked for 30 seconds.")

# def shop_page():
#     st.markdown("<div class='header'>Welcome to SmartShop</div>", unsafe_allow_html=True)
#     st.markdown("<div class='subtle'>Browse top products</div>", unsafe_allow_html=True)

#     cols = st.columns(3)
#     for i, (name, price, img_path) in enumerate(PRODUCTS):
#         with cols[i % 3]:
#             st.markdown("<div class='card'>", unsafe_allow_html=True)
#             if os.path.exists(img_path):
#                 try:
#                     img = Image.open(img_path).convert("RGB")
#                     img = img.resize((IMG_W, IMG_H))
#                     st.image(img, use_column_width=False)
#                 except Exception as e:
#                     st.warning(f"Image error: {e}")
#             st.markdown(f"<div class='title'>{name}</div>", unsafe_allow_html=True)
#             st.markdown(f"<div class='price'>{price}</div>", unsafe_allow_html=True)
#             if st.button(f"Buy Now - {name}"):
#                 st.session_state.click_count += 1
#                 st.success(f"Order placed for {name}.")
#             st.markdown("</div>", unsafe_allow_html=True)

#     if detect_anomaly():
#         st.session_state.show_popup = True

#     if st.session_state.show_popup:
#         st.markdown(f"""
#         <style>
#         .overlay {{
#             position: fixed;
#             top: 0; left: 0; right: 0; bottom: 0;
#             background: rgba(0,0,0,0.5);
#             backdrop-filter: blur(5px);
#             display: flex;
#             justify-content: center;
#             align-items: center;
#             z-index: 9999;
#         }}
#         .modal {{
#             background: white;
#             padding: 30px;
#             border-radius: 12px;
#             text-align: center;
#             max-width: 400px;
#             box-shadow: 0 0 20px rgba(0,0,0,0.3);
#             color: #111827;
#             font-family: Inter, sans-serif;
#         }}
#         .modal button {{
#             padding: 10px 20px;
#             border: none;
#             border-radius: 8px;
#             background: #ff4d4d;
#             color: white;
#             font-weight: bold;
#             cursor: pointer;
#         }}
#         </style>
#         <div class="overlay">
#             <div class="modal">
#                 <p style="font-size:18px;font-weight:bold;">{ANOMALY_MESSAGE}</p>
#                 <form action="" method="get">
#                     <button type="submit">OK</button>
#                 </form>
#             </div>
#         </div>
#         """, unsafe_allow_html=True)

#     st.markdown('<div class="footer">© 2025 SmartShop – Anomaly Detection Project</div>', unsafe_allow_html=True)

# def settings_page():
#     st.markdown("<div class='header'>Anomaly Detection Settings</div>", unsafe_allow_html=True)
#     st.markdown("<div class='subtle'>Adjust thresholds to simulate human vs bot behavior</div>", unsafe_allow_html=True)

#     st.session_state.RANDOM_ANOMALY_PROB = st.slider(
#         "Random anomaly chance (%)", 0, 100, int(st.session_state.RANDOM_ANOMALY_PROB * 100)
#     ) / 100.0

#     st.session_state.MAX_CLICKS_PER_MIN = st.slider(
#         "Max clicks per minute allowed", 5, 100, st.session_state.MAX_CLICKS_PER_MIN
#     )

#     st.session_state.MIN_SAFE_SECONDS = st.slider(
#         "Minimum safe seconds before multiple clicks", 1, 30, st.session_state.MIN_SAFE_SECONDS
#     )

#     st.info("""
#     **How it works:**
#     - If user exceeds clicks/min or acts too fast → popup alert appears.
#     - Adjust sliders to make thresholds stricter (bot-like) or looser (human-like).
#     """)

#     if st.button("Apply Settings"):
#         st.success("Parameters updated. Go back to Shop page to test behavior.")

# # ------------------ ROUTER ------------------
# if st.session_state.logged_in:
#     page = st.sidebar.radio("Navigation", ["Shop", "Anomaly Settings"])
#     if page == "Shop":
#         shop_page()
#     elif page == "Anomaly Settings":
#         settings_page()
# else:
#     login_page()














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
        if random.random() < st.session_state.RANDOM_ANOMALY_PROB:
            return True
        clicks_per_min = (clicks / elapsed) * 60.0
        if clicks_per_min > st.session_state.MAX_CLICKS_PER_MIN:
            return True
        if elapsed < st.session_state.MIN_SAFE_SECONDS and clicks >= 2:
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

# ------------------ UI THEME ------------------
st.set_page_config(page_title="SmartShop", layout="wide")
# st.markdown("""
# <style>
# /* App background */
# [data-testid="stAppViewContainer"] {
#     background-color: #f4f6f9 !important;
#     color: #111827 !important;
#     font-family: 'Inter', 'Segoe UI', Roboto, Arial, sans-serif;
# }

# /* Sidebar */
# [data-testid="stSidebar"] {
#     background-color: #1f2937 !important;
#     color: #f9fafb !important;
# }
# [data-testid="stSidebar"] .css-1offfwp, 
# [data-testid="stSidebar"] .css-qrbaxs {
#     color: #f9fafb !important;
#     font-weight: 600;
# }

# /* Make all widget labels readable */
# .stMarkdown, .stSlider label, .stSlider span, .stSlider div, 
# .stTextInput label, .stTextInput input,
# .stButton button, .stSelectbox label,
# .stNumberInput label, .stNumberInput input,
# .stCheckbox label, .stRadio label {
#     color: #111827 !important;
#     font-weight: 500 !important;
# }

# /* Headings */
# .header {
#     text-align:center;
#     font-size: 32px;
#     font-weight: 800;
#     color: #1e40af;
#     margin: 8px 0 12px;
# }
# .subtle {
#     text-align:center;
#     color:#374151;
#     margin-bottom: 24px;
#     font-size: 14px;
# }

# /* Product cards */
# .card {
#     border: 1px solid #e5e7eb;
#     border-radius: 12px;
#     padding: 16px;
#     background: #fff;
#     box-shadow: 0 2px 6px rgba(0,0,0,0.06);
#     text-align: center;
#     transition: transform .2s ease, box-shadow .2s ease;
#     color: #111827;
# }
# .card:hover {
#     transform: translateY(-4px);
#     box-shadow: 0 8px 20px rgba(0,0,0,0.12);
# }
# .title {
#     font-size: 18px;
#     font-weight: 600;
#     margin-top: 10px;
# }
# .price {
#     font-size: 16px;
#     font-weight: 700;
#     color: #d32f2f;
#     margin: 6px 0 12px;
# }

# /* Footer */
# .footer {
#     text-align:center;
#     margin-top:40px;
#     font-size: 13px;
#     color:#6b7280;
# }
# </style>
# """, unsafe_allow_html=True)
st.markdown("""
<style>
/* App background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f9fafb, #eef2f7);
    color: #111827 !important;
    font-family: 'Inter', 'Segoe UI', Roboto, Arial, sans-serif;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(31,41,55,0.95) !important;
    color: #f9fafb !important;
    backdrop-filter: blur(8px);
    border-right: 1px solid #374151;
}
[data-testid="stSidebar"] .css-1offfwp, 
[data-testid="stSidebar"] .css-qrbaxs {
    color: #f9fafb !important;
    font-weight: 600;
}

/* Headings */
.header {
    text-align:center;
    font-size: 34px;
    font-weight: 800;
    color: #1d4ed8;
    margin: 8px 0 16px;
}
.subtle {
    text-align:center;
    color:#4b5563;
    margin-bottom: 24px;
    font-size: 15px;
}

/* Product cards */
.card {
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 18px;
    background: #ffffff;
    box-shadow: 0 3px 10px rgba(0,0,0,0.06);
    text-align: center;
    transition: transform .25s ease, box-shadow .25s ease;
}
.card:hover {
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0 12px 24px rgba(0,0,0,0.15);
}
.title {
    font-size: 19px;
    font-weight: 600;
    margin-top: 10px;
    color: #111827;
}
.price {
    font-size: 16px;
    font-weight: 700;
    color: #dc2626;
    margin: 8px 0 14px;
}

/* Buttons */
.stButton button {
    background: linear-gradient(90deg, #2563eb, #3b82f6);
    color: white !important;
    font-weight: 600 !important;
    border: none;
    border-radius: 8px;
    padding: 10px 18px;
    transition: all 0.2s ease;
}
.stButton button:hover {
    background: linear-gradient(90deg, #1d4ed8, #2563eb);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(37,99,235,0.4);
}

/* Modal overlay */
.overlay {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.55);
    backdrop-filter: blur(6px);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
}
.modal {
    background: #ffffff;
    padding: 28px;
    border-radius: 14px;
    text-align: center;
    max-width: 420px;
    box-shadow: 0 0 24px rgba(0,0,0,0.25);
    color: #111827;
    font-family: Inter, sans-serif;
}
.modal button {
    padding: 10px 20px;
    border: none;
    border-radius: 10px;
    background: #ef4444;
    color: white;
    font-weight: bold;
    cursor: pointer;
    transition: all .2s ease;
}
.modal button:hover {
    background: #dc2626;
    transform: scale(1.05);
}

/* Footer */
.footer {
    text-align:center;
    margin-top:50px;
    font-size: 13px;
    color:#6b7280;
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
    st.markdown("<div class='header'>SmartShop Sign In</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtle'>Use your credentials to continue</div>", unsafe_allow_html=True)

    if st.session_state.account_locked_until and time.time() < st.session_state.account_locked_until:
        remaining = int(st.session_state.account_locked_until - time.time())
        st.error(f" Account locked. Try again in {remaining} seconds.")
        return

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            st.session_state.logged_in = True
            st.session_state.start_time = time.time()
            st.session_state.click_count = 0
            st.session_state.scroll_depth = 0
            st.session_state.failed_logins = 0
            st.session_state.account_locked_until = None
        else:
            st.session_state.failed_logins += 1
            remaining_attempts = 3 - st.session_state.failed_logins
            if remaining_attempts > 0:
                st.warning(f"Wrong credentials. {remaining_attempts} attempt(s) left.")
            else:
                st.session_state.account_locked_until = time.time() + 30
                st.error("Too many failed attempts. Locked for 30 seconds.")

def shop_page():
    st.markdown("<div class='header'>Welcome to SmartShop</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtle'>Browse top products</div>", unsafe_allow_html=True)

    cols = st.columns(3)
    for i, (name, price, img_path) in enumerate(PRODUCTS):
        with cols[i % 3]:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            if os.path.exists(img_path):
                try:
                    img = Image.open(img_path).convert("RGB")
                    img = img.resize((IMG_W, IMG_H))
                    st.image(img, use_column_width=False)
                except Exception as e:
                    st.warning(f"Image error: {e}")
            st.markdown(f"<div class='title'>{name}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='price'>{price}</div>", unsafe_allow_html=True)
            if st.button(f"Buy Now - {name}"):
                st.session_state.click_count += 1
                st.success(f"Order placed for {name}.")
            st.markdown("</div>", unsafe_allow_html=True)

    if detect_anomaly():
        st.session_state.show_popup = True

    if st.session_state.show_popup:
        st.markdown(f"""
        <style>
        .overlay {{
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.5);
            backdrop-filter: blur(5px);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
        }}
        .modal {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            text-align: center;
            max-width: 400px;
            box-shadow: 0 0 20px rgba(0,0,0,0.3);
            color: #111827;
            font-family: Inter, sans-serif;
        }}
        .modal button {{
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            background: #ff4d4d;
            color: white;
            font-weight: bold;
            cursor: pointer;
        }}
        </style>
        <div class="overlay">
            <div class="modal">
                <p style="font-size:18px;font-weight:bold;">{ANOMALY_MESSAGE}</p>
                <form action="" method="get">
                    <button type="submit">OK</button>
                </form>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="footer">© 2025 SmartShop – Anomaly Detection Project</div>', unsafe_allow_html=True)

def settings_page():
    st.markdown("<div class='header'>Anomaly Detection Settings</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtle'>Adjust thresholds to simulate human vs bot behavior</div>", unsafe_allow_html=True)

    st.session_state.RANDOM_ANOMALY_PROB = st.slider(
        "Random anomaly chance (%)", 0, 100, int(st.session_state.RANDOM_ANOMALY_PROB * 100)
    ) / 100.0

    st.session_state.MAX_CLICKS_PER_MIN = st.slider(
        "Max clicks per minute allowed", 5, 100, st.session_state.MAX_CLICKS_PER_MIN
    )

    st.session_state.MIN_SAFE_SECONDS = st.slider(
        "Minimum safe seconds before multiple clicks", 1, 30, st.session_state.MIN_SAFE_SECONDS
    )

    st.info("""
    **How it works:**
    - If user exceeds clicks/min or acts too fast → popup alert appears.
    - Adjust sliders to make thresholds stricter (bot-like) or looser (human-like).
    """)

    if st.button("Apply Settings"):
        st.success("Parameters updated. Go back to Shop page to test behavior.")

# ------------------ ROUTER ------------------
if st.session_state.logged_in:
    page = st.sidebar.radio("Navigation", ["Shop", "Anomaly Settings"])
    if page == "Shop":
        shop_page()
    elif page == "Anomaly Settings":
        settings_page()
else:
    login_page()

