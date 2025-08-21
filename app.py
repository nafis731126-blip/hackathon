# ---------- Periods Pal (Pro UI) ----------
import os
from datetime import datetime, timedelta
import pandas as pd
import streamlit as st

# ---------------- Page Setup ----------------
st.set_page_config(page_title="YOUR FLOW SUPPORT", page_icon="🌸", layout="wide")

# ---------------- Constants / Paths ----------------
DATA_DIR = "data"
ASSETS_DIR = "assets"
USERS = os.path.join(DATA_DIR, "users.csv")
PERIODS = os.path.join(DATA_DIR, "periods.csv")
DIARY = os.path.join(DATA_DIR, "diary.csv")
CONSULTS = os.path.join(DATA_DIR, "consults.csv")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)

def init_csv(path, cols):
    if not os.path.exists(path):
        pd.DataFrame(columns=cols).to_csv(path, index=False)

init_csv(USERS,    ["username","password","name","age","height_cm","weight_kg","created"])
init_csv(PERIODS,  ["username","last_start","cycle_len","expected_next","created"])
init_csv(DIARY,    ["username","date","symptoms","notes","created"])
init_csv(CONSULTS, ["username","name","age","height_cm","weight_kg","problem","status","requested_at","doctor_reply"])

# ---------------- CSS (light polish) ----------------
st.markdown("""
<style>
/* Header title center */
.pp-title {text-align:center;font-size:28px;font-weight:700;margin:4px 0 0 0;}
.pp-sub   {text-align:center;color:#6b7280;margin:-2px 0 12px 0;}
/* Cards */
.pp-card {border:1px solid #e5e7eb;border-radius:16px;padding:18px;background:rgba(250,250,250,0.75);}
.pp-cta  {border:1px solid #dbeafe;background:#eff6ff;}
/* Bottom space (for chatbot) */
footer {visibility:hidden;}
/* Floating button (simulate) */
.pp-float {position:fixed; right:18px; bottom:18px; z-index:999;}
.pp-btn  {background:#ec4899;color:white;border:none;border-radius:999px;padding:12px 16px;font-weight:700;}
</style>
""", unsafe_allow_html=True)

# ---------------- Utilities ----------------
def load_df(path):      return pd.read_csv(path)
def save_df(df, path):  df.to_csv(path, index=False)

def user_row(username):
    u = load_df(USERS)
    if username in list(u["username"]):
        return u[u["username"]==username].iloc[0]
    return None

def ensure_session():
    for k, v in {
        "logged_in": False,
        "username": "",
        "page": "Home",
        "chat_open": False,
    }.items():
        if k not in st.session_state: st.session_state[k] = v

ensure_session()

# ---------------- Header ----------------
def header():
    cols = st.columns([1,5,2,2])
    with cols[0]:
        logo_path = os.path.join(ASSETS_DIR, "logo.png")
        if os.path.exists(logo_path):
            st.image(logo_path, width=60)
        else:
            st.write("🌸")
    with cols[1]:
        st.markdown("<div class='pp-title'>Periods Pal</div>", unsafe_allow_html=True)
        st.markdown("<div class='pp-sub'>Track · Learn · Consult — supported by Team UNAS</div>", unsafe_allow_html=True)
    with cols[2]:
        if st.session_state.logged_in:
            st.success(f"👤 {st.session_state.username}")
        else:
            st.info("Not logged in")
    with cols[3]:
        if st.session_state.logged_in:
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.session_state.username = ""
        else:
            st.write("")

# ---------------- Auth ----------------
def auth_block():
    st.markdown("### 🔐 Sign Up / Login")
    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        u = st.text_input("Username", key="lg_u")
        p = st.text_input("Password", type="password", key="lg_p")
        if st.button("Login"):
            df = load_df(USERS)
            ok = (len(df)>0) and ((df["username"]==u) & (df["password"]==p)).any()
            if ok:
                st.session_state.logged_in = True
                st.session_state.username = u
                st.success("Logged in ✅")
            else:
                st.error("Invalid credentials")

    with tab2:
        u = st.text_input("Choose username", key="su_u")
        p = st.text_input("Choose password", type="password", key="su_p")
        name = st.text_input("Your name")
        age  = st.number_input("Age", 10, 80, 20, step=1)
        h    = st.number_input("Height (cm)", 80, 220, 160, step=1)
        w    = st.number_input("Weight (kg)", 20, 200, 55, step=1)
        if st.button("Create Account"):
            if not u or not p:
                st.error("Username & password required")
            else:
                df = load_df(USERS)
                if u in list(df["username"]):
                    st.warning("Username already exists")
                else:
                    df = pd.concat([df, pd.DataFrame([{
                        "username": u, "password": p, "name": name,
                        "age": age, "height_cm": h, "weight_kg": w,
                        "created": datetime.now()
                    }])], ignore_index=True)
                    save_df(df, USERS)
                    st.success("Account created. Please login.")

# ---------------- Navigation ----------------
def nav_bar():
    c1, c2, c3, c4 = st.columns(4)
    def nav_btn(col, label, target):
        with col:
            if st.button(label, use_container_width=True):
                st.session_state.page = target
    nav_btn(c1, "🏠 Home", "Home")
    nav_btn(c2, "📚 All Courses", "All Courses")
    nav_btn(c3, "👩‍⚕️ Consult", "Consult")
    nav_btn(c4, "📔 Diary", "Diary")

# ---------------- Pages ----------------
def page_home():
    st.markdown("#### স্বাগতম!  \nPeriods Pal আপনার ব্যক্তিগত সঙ্গী — **পিরিয়ড ট্র্যাকিং**, **শিক্ষামূলক কন্টেন্ট**, আর **ডাক্তারের পরামর্শ** — এক জায়গায়।")
    cols = st.columns(3)
    with cols[0]:
        st.markdown("<div class='pp-card'><h4>🗓️ Easy Tracking</h4><p>Last date দিন, expected date পেয়ে যান।</p></div>", unsafe_allow_html=True)
    with cols[1]:
        st.markdown("<div class='pp-card'><h4>📘 Learn Fast</h4><p>Do/Don'ts, Diet, Yoga — ছোট ছোট পাঠ।</p></div>", unsafe_allow_html=True)
    with cols[2]:
        st.markdown("<div class='pp-card'><h4>👩‍⚕️ Consult</h4><p>সমস্যা লিখুন, ডাক্তার রিভিউ দিবেন (ডেমো)।</p></div>", unsafe_allow_html=True)

    st.markdown("")
    with st.container():
        c1, c2, c3 = st.columns([1.2,1,1])
        with c1:
            st.markdown("<div class='pp-card pp-cta'><h4>🚀 Quick Start</h4><p>নিচের বাটনে ক্লিক করে দ্রুত শুরু করুন।</p></div>", unsafe_allow_html=True)
        with c2:
            if st.button("Start Tracking", use_container_width=True):
                st.session_state.page = "All Courses"
        with c3:
            if st.button("Consult Doctor", use_container_width=True):
                st.session_state.page = "Consult"

def page_courses():
    st.header("📚 Our Support")
    st.caption("শিক্ষামূলক মডিউল — দ্রুত পড়ুন, কাজে লাগান")
    choice = st.selectbox("Open a module", ["Periods Tracker","Do & Don'ts","Diet","Yoga"])

    # Periods Tracker
    if choice == "Periods Tracker":
        st.subheader("🗓️ Periods Tracker")
        last = st.date_input("Last period start date")
        cycle = st.number_input("Average cycle length (days)", 20, 45, 28)
        if st.button("Calculate Expected Date"):
            expected = last + timedelta(days=int(cycle))
            st.success(f"Next expected period: **{expected}**")
            if st.session_state.logged_in:
                df = load_df(PERIODS)
                row = {
                    "username": st.session_state.username,
                    "last_start": str(last),
                    "cycle_len": int(cycle),
                    "expected_next": str(expected),
                    "created": datetime.now()
                }
                save_df(pd.concat([df, pd.DataFrame([row])], ignore_index=True), PERIODS)
                st.info("Saved to your history ✅")
        st.markdown("---")
        st.markdown("**History (latest)**")
        if st.session_state.logged_in:
            df = load_df(PERIODS)
            mine = df[df["username"]==st.session_state.username].copy()
            if len(mine)>0:
                mine = mine.sort_values("created", ascending=False).head(5)
                st.table(mine[["last_start","cycle_len","expected_next","created"]])
            else:
                st.caption("No past entries yet.")
        else:
            st.caption("Login to save & view your history.")

    # Do & Don'ts
    elif choice == "Do & Don'ts":
        st.subheader("✅ Do & ❌ Don't")
        left, right = st.columns(2)
        with left:
            st.markdown("**Do**")
            st.markdown("- হাইজিন মেনে চলুন  \n- কুসুম গরম পানি পান করুন  \n- হালকা স্ট্রেচিং/বিশ্রাম  \n- আয়রন-ভিত্তিক খাবার")
        with right:
            st.markdown("**Don't**")
            st.markdown("- অতিরিক্ত ক্যাফেইন  \n- হেভি এক্সারসাইজ (হেভি ডে তে)  \n- অস্বাস্থ্যকর স্যানিটারি প্র্যাকটিস")

    # Diet
    elif choice == "Diet":
        st.subheader("🥗 Diet Tips")
        st.markdown("- পালংশাক, ডাল, ডিম — আয়রন  \n- ফল, শাক-সবজি  \n- উষ্ণ চা/হারবাল টি  \n- পানি বেশি পান")
        st.info("যদি মাথা ঘোরে/দুর্বল লাগে → আয়রন-সমৃদ্ধ খাবার ও ডাক্তারের পরামর্শ নিন।")

    # Yoga
    elif choice == "Yoga":
        st.subheader("🧘 Yoga for Relief")
        st.markdown("- Child’s pose  \n- Cat-Cow  \n- Legs-up-the-wall  \n- Deep breathing")
        st.video("https://www.youtube.com/watch?v=U2mA0e0YJ5c")

def page_consult():
    st.header("👩‍⚕️ Consult with Doctor")
    if not st.session_state.logged_in:
        st.info("Please login first to continue.")
        auth_block()
        return

    user = user_row(st.session_state.username)
    if user is not None:
        st.success(f"Profile: {user.get('name','')} · Age {user.get('age','')} · {user.get('height_cm','')}cm · {user.get('weight_kg','')}kg")

    problem = st.text_area("Tell us about your problem (বাংলা/English)")
    if st.button("Request Consultation"):
        df = load_df(CONSULTS)
        row = {
            "username": st.session_state.username,
            "name": user.get("name",""),
            "age": user.get("age",""),
            "height_cm": user.get("height_cm",""),
            "weight_kg": user.get("weight_kg",""),
            "problem": problem,
            "status": "requested",
            "requested_at": datetime.now(),
            "doctor_reply": ""
        }
        save_df(pd.concat([df, pd.DataFrame([row])], ignore_index=True), CONSULTS)
        st.success("Consultation requested ✅ (Demo: reply will be added later).")

    st.markdown("---")
    st.markdown("**Your recent requests**")
    df = load_df(CONSULTS)
    mine = df[df["username"]==st.session_state.username].copy()
    if len(mine)>0:
        mine = mine.sort_values("requested_at", ascending=False).head(5)
        st.table(mine[["problem","status","requested_at","doctor_reply"]])
    else:
        st.caption("No requests yet.")

def page_diary():
    st.header("📔 Personal Diary (Private)")
    if not st.session_state.logged_in:
        st.info("Please login to use diary.")
        auth_block()
        return

    c1, c2 = st.columns([1,2])
    with c1:
        d_date = st.date_input("Date")
        symptoms = st.multiselect("Symptoms", ["Cramps","Headache","Nausea","Mood swing","Heavy flow","None"])
    with c2:
        notes = st.text_area("Notes (private)")

    if st.button("Save Note"):
        df = load_df(DIARY)
        row = {
            "username": st.session_state.username,
            "date": str(d_date),
            "symptoms": "|".join(symptoms) if symptoms else "",
            "notes": notes,
            "created": datetime.now()
        }
        save_df(pd.concat([df, pd.DataFrame([row])], ignore_index=True), DIARY)
        st.success("Saved to diary ✅")

    st.markdown("---")
    st.markdown("**Recent entries**")
    df = load_df(DIARY)
    mine = df[df["username"]==st.session_state.username].copy()
    if len(mine)>0:
        mine = mine.sort_values("created", ascending=False).head(8)
        st.table(mine[["date","symptoms","notes","created"]])
    else:
        st.caption("No entries yet.")

# ---------------- Chatbot (simple toggle) ----------------
def chatbot():
    # floating style button (simulate)
    with st.container():
        st.markdown("<div class='pp-float'>", unsafe_allow_html=True)
        if not st.session_state.chat_open:
            if st.button("💬 Chat", key="chat_open", help="Open chatbot"):
                st.session_state.chat_open = True
        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.chat_open:
        st.markdown("### 💬 Chatbot")
        q = st.text_input("Ask your question (e.g., delay, pain, heavy flow)")
        if st.button("Send", key="chat_send"):
            txt = (q or "").lower()
            if any(k in txt for k in ["delay","late","দেরি"]):
                st.info("যদি ৭ দিন বা তার বেশি দেরি হয়, ডাক্তারের পরামর্শ নিন। স্ট্রেস/ওজন/গর্ভাবস্থা ইত্যাদি কারণ হতে পারে।")
            elif any(k in txt for k in ["pain","cramp","ব্যথা","কষ্ট"]):
                st.info("হট-বটল, হালকা ব্যথানাশক (ডাক্তারের পরামর্শে), বিশ্রাম। তীব্র হলে ডাক্তারের সাথে যোগাযোগ করুন।")
            elif any(k in txt for k in ["heavy","bleeding","রক্ত"]):
                st.info("অস্বাভাবিক ভারী রক্তপাত হলে দ্রুত ডাক্তারের সাথে যোগাযোগ করুন। আয়রন-সমৃদ্ধ খাবার গ্রহণ করুন।")
            else:
                st.info("আমি বুঝতে পারিনি। ‘delay’, ‘pain’, ‘heavy’ ইত্যাদি শব্দ ব্যবহার করুন বা Consult পেজে যান।")
        if st.button("Close Chat", key="chat_close"):
            st.session_state.chat_open = False

# ---------------- Main ----------------
def main():
    header()
    nav_bar()

    page = st.session_state.page
    if page == "Home":
        page_home()
    elif page == "All Courses":
        page_courses()
    elif page == "Consult":
        page_consult()
    elif page == "Diary":
        page_diary()

    st.markdown("---")
    st.caption("Privacy: Demo app — data stored locally in /data folder on this device only.")
    chatbot()

if __name__ == "__main__":
    main()
