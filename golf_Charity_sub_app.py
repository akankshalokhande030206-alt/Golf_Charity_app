import streamlit as st
import random
from datetime import datetime

# Page Config
st.set_page_config(page_title="GCS | Golf Charity Subscription", layout="wide", initial_sidebar_state="expanded")

# ---------------------- PREMIUM CSS (WITH MOBILE RESPONSIVENESS) ----------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Inter:wght@400;600;700;800&display=swap');

    .stApp { background-color: #f8faf8; font-family: 'Inter', sans-serif; }

    /* GLOWING GOLDEN POP BUTTON */
    div.stButton > button:first-child[kind="primary"] {
        background: #d4af37 !important; 
        color: #000000 !important; 
        font-size: 24px !important;
        font-weight: 900 !important;
        padding: 20px 60px !important;
        border-radius: 60px !important;
        border: 2px solid #fde68a !important;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.6);
        transition: all 0.3s ease-in-out;
        animation: glowing-pop 2s infinite;
    }
    
    @keyframes glowing-pop {
        0% { transform: scale(1); box-shadow: 0 0 5px #d4af37; }
        50% { transform: scale(1.05); box-shadow: 0 0 25px #fbbf24; border-color: #ffffff; }
        100% { transform: scale(1); box-shadow: 0 0 5px #d4af37; }
    }

    /* MEMBER UI COMPONENTS */
    .member-card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        margin-bottom: 20px;
    }
    .profile-header {
        background: linear-gradient(90deg, #064e3b, #14532d);
        padding: 40px;
        border-radius: 25px;
        color: white;
        margin-bottom: 30px;
    }
    .prd-header {
        background-color: #14532d;
        color: white;
        padding: 10px 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        font-weight: 800;
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] { background-color: #064e3b !important; }
    section[data-testid="stSidebar"] .stButton > button {
        background-color: rgba(255,255,255,0.05);
        color: #ecfdf5 !important;
        border: 1px solid rgba(255,255,255,0.1);
        font-weight: 600;
        margin-bottom: 10px;
        width: 100%;
    }
    section[data-testid="stSidebar"] .stButton > button:hover { background-color: #d4af37; color: #064e3b !important; }

    /* WELCOME HERO SECTION */
    .welcome-hero {
        background: linear-gradient(rgba(10, 50, 20, 0.75), rgba(10, 50, 20, 0.75)), 
                    url('https://images.unsplash.com/photo-1535131749006-b7f58c99034b?auto=format&fit=crop&q=80');
        background-size: cover;
        background-position: center;
        padding: 100px 60px;
        border-radius: 30px;
        color: white;
        text-align: center;
        margin-bottom: 50px;
    }

    /* ---------------- MOBILE OPTIMIZATION ---------------- */
    @media (max-width: 768px) {
        .welcome-hero {
            padding: 60px 20px !important;
        }
        .welcome-hero h1 {
            font-size: 38px !important; /* Smaller text for mobile */
        }
        .profile-header {
            padding: 20px !important;
        }
        .profile-header h1 {
            font-size: 24px !important;
        }
        div.stButton > button:first-child[kind="primary"] {
            font-size: 18px !important;
            padding: 15px 30px !important;
            width: 100% !important; /* Full width button on mobile */
        }
        .stMetric {
            text-align: center;
        }
    }
</style>
""", unsafe_allow_html=True)

# ---------------------- SESSION STATE ----------------------
if "users" not in st.session_state:
    st.session_state.users = {
        "admin": {"password": "123", "scores": [], "plan": "Platinum", "joined": "2026-01-15"}
    }
if "charities" not in st.session_state:
    st.session_state.charities = ["Global Golf Relief", "UNICEF Golf", "Red Cross Impact"]
if "current_user" not in st.session_state: st.session_state.current_user = None
if "page" not in st.session_state: st.session_state.page = "Welcome"
if "total_revenue" not in st.session_state: st.session_state.total_revenue = 1240000 

# ---------------------- FUNCTIONS ----------------------
def add_score_logic(user, score):
    new_entry = {"score": score, "date": datetime.now().strftime("%Y-%m-%d %H:%M")}
    user_scores = st.session_state.users[user]["scores"]
    user_scores.append(new_entry)
    if len(user_scores) > 5: user_scores.pop(0)

# ---------------------- SIDEBAR (GCS ⛳) ----------------------
with st.sidebar:
    st.markdown("<h1 style='color:#d4af37; text-align:center;'>GCS ⛳</h1>", unsafe_allow_html=True)
    if not st.session_state.current_user:
        if st.button("🔑 Login Account"): st.session_state.page = "Login"
        if st.button("📝 Register Member"): st.session_state.page = "Signup"
        st.markdown("<hr style='opacity:0.2'>", unsafe_allow_html=True)
        if st.button("🏠 Welcome Page"): st.session_state.page = "Welcome"
    else:
        st.markdown(f"<div style='text-align:center; color:white;'>Member: <b>{st.session_state.current_user}</b></div>", unsafe_allow_html=True)
        if st.button("🏠 Member Home"): st.session_state.page = "MemberHome"
        if st.button("📊 Admin Dashboard"): st.session_state.page = "Dashboard"
        if st.button("💳 Subscription Engine"): st.session_state.page = "Subscription"
        if st.button("🚪 Logout"):
            st.session_state.current_user = None
            st.session_state.page = "Welcome"
            st.rerun()

# ---------------------- PAGE LOGIC ----------------------

if st.session_state.page == "Welcome" and not st.session_state.current_user:
    st.markdown('<div class="welcome-hero"><h1>GOLF CHARITY <br> SUBSCRIPTION</h1><p>Play with purpose. Win with impact.</p></div>', unsafe_allow_html=True)
    _, col_btn, _ = st.columns([1, 2, 1])
    if col_btn.button("START YOUR IMPACT JOURNEY", type="primary"):
        st.session_state.page = "Signup"
        st.rerun()

elif st.session_state.page == "MemberHome" and st.session_state.current_user:
    user = st.session_state.current_user
    data = st.session_state.users[user]
    st.markdown(f'<div class="profile-header"><h1>Welcome Back, {user} 👋</h1><p>Tier: <b>{data.get("plan", "Standard")}</b></p></div>', unsafe_allow_html=True)
    
    #  | SCORE MANAGEMENT
    with st.expander("⛳ MY SCORES (Score Management System)", expanded=True):
        st.markdown('<div class="prd-header"> | SCORE MANAGEMENT</div>', unsafe_allow_html=True)
        c_in, c_out = st.columns([1, 2])
        with c_in:
            score_input = st.number_input("Stableford Score (1-45)", 1, 45, key="ms_in")
            if st.button("Submit Score"):
                add_score_logic(user, score_input)
                st.success("Score added. Rolling 5 logic applied.")
        with c_out:
            if data["scores"]:
                for s in reversed(data["scores"]):
                    st.info(f"⭐ Score: {s['score']} | 📅 Date: {s['date']}")
            else: st.write("No scores found.")

    #  | DRAW & REWARD SYSTEM
    with st.expander("🏆 DRAW REWARDS (Draw & Reward System)"):
        st.markdown('<div class="prd-header"> | DRAW & REWARDS</div>', unsafe_allow_html=True)
        st.markdown("- 5-Number Match (Jackpot)\n- 4-Number Match\n- 3-Number Match")
        if st.button("Run Simulation Draw"):
            st.success(f"Winning Numbers: {random.sample(range(1, 46), 5)}")
            st.balloons()

    #  | PRIZE POOL LOGIC
    with st.expander("💰 PRIZE POOLS (Prize Pool Logic)"):
        st.markdown('<div class="prd-header"> | PRIZE POOL LOGIC</div>', unsafe_allow_html=True)
        pool = st.session_state.total_revenue * 0.50
        st.table([
            {"Tier": "Match 5", "Pool Share": "40%", "Amount": f"₹{pool*0.4:,.0f}"},
            {"Tier": "Match 4", "Pool Share": "35%", "Amount": f"₹{pool*0.35:,.0f}"},
            {"Tier": "Match 3", "Pool Share": "25%", "Amount": f"₹{pool*0.25:,.0f}"}
        ])

elif st.session_state.page == "Dashboard" and st.session_state.current_user:
    st.title("🛡️ Admin Dashboard")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["👥 User Mgmt", "🎰 Draw Mgmt", "🎗️ Charity Mgmt", "🏆 Winners", "📈 Reports"])
    
    with tab1:
        st.subheader("Manage User Profiles & Scores")
        target_user = st.selectbox("Select User", list(st.session_state.users.keys()))
        if st.button("Reset User Scores"):
            st.session_state.users[target_user]["scores"] = []
            st.success("Scores Cleared.")

    with tab2:
        st.subheader("Draw Configuration")
        mode = st.radio("Draw Logic", ["Random Generation", "Algorithmic"])
        if st.button("Run Pre-Analysis Simulation"):
            st.write(f"Simulation result: {random.sample(range(1, 46), 5)}")

    with tab3:
        st.subheader("Charity Directory")
        new_ch = st.text_input("Add Charity")
        if st.button("Add"):
            st.session_state.charities.append(new_ch)
        st.write("Current:", st.session_state.charities)

    with tab4:
        st.subheader("Winner Verification")
        st.info("No winners currently pending payout verification.")

    with tab5:
        st.subheader("Reports & Analytics")
        st.metric("Total Prize Pool", f"₹{st.session_state.total_revenue * 0.5:,.0f}")
        st.line_chart([random.randint(30, 45) for _ in range(10)])

elif st.session_state.page == "Subscription":
    st.title("💳 Subscription Engine")
    st.info("10% min contribution logic active.")

elif st.session_state.page == "Login":
    _, c, _ = st.columns([1, 1.5, 1])
    with c:
        st.markdown('<div class="member-card"><h2>Login</h2>', unsafe_allow_html=True)
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Access GCS"):
            if u in st.session_state.users and st.session_state.users[u]["password"] == p:
                st.session_state.current_user = u
                st.session_state.page = "MemberHome"
                st.rerun()

elif st.session_state.page == "Signup":
    _, c, _ = st.columns([1, 1.5, 1])
    with c:
        st.markdown('<div class="member-card"><h2>Register</h2>', unsafe_allow_html=True)
        new_u = st.text_input("Username")
        new_p = st.text_input("Password", type="password")
        if st.button("Create Account"):
            st.session_state.users[new_u] = {"password": new_p, "scores": [], "plan": "Standard"}
            st.session_state.page = "Login"
            st.rerun()