import streamlit as st
from streamlit_ace import st_ace
import subprocess
import os
import sys
import json
import re
import time

# ==========================================
# Pydroid 3 डार्क थीम आणि UI लेआउट कॉन्फिगरेशन
# ==========================================
st.set_page_config(page_title="Advanced Pydroid Ultimate", layout="wide")

LOG_FILE = "bot_output.log"
VAULT_FILE = "secure_vault.json"
SAVED_CODE_FILE = "user_script.py"

# Pydroid 3 सारखा हुबेहूब लुक देणारा प्रगत CSS लेयर (नियम ५, २२)
st.markdown("""
    <style>
    .terminal-box {
        background-color: #050505 !important;
        color: #38ff12 !important;
        font-family: 'Courier New', monospace !important;
        padding: 15px;
        border-radius: 6px;
        border: 1px solid #222;
        height: 250px;
        overflow-y: auto;
    }
    .stApp { background-color: #0f0f12; }
    .stButton>button { width: 100%; border-radius: 4px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# नियम ५ आणि १९: मोबाईल कीबोर्ड सिंटॅक्स क्लीनर
# ==========================================
def sanitize_code(raw_code: str) -> str:
    if not raw_code:
        return ""
    clean = raw_code.replace("\r\n", "\n")
    clean = re.sub(r'[“”]', '"', clean)
    clean = re.sub(r'[‘’]', "'", clean)
    return clean

# ==========================================
# नियम १०, २५: ऑटोमॅटिक क्रेडेंशियल इंजेक्शन
# ==========================================
def inject_credentials(env_dict):
    if os.path.exists(VAULT_FILE):
        try:
            with open(VAULT_FILE, "r") as f:
                vault = json.load(f)
                env_dict["EXCHANGE_API_KEY"] = vault.get("api_key", "")
                env_dict["TELEGRAM_BOT_TOKEN"] = vault.get("tg_token", "")
                env_dict["TELEGRAM_CHAT_ID"] = vault.get("tg_id", "")
        except:
            pass
    return env_dict

# ==========================================
# Pydroid 3 स्क्रीनशॉटप्रमाणे साइडबार नेव्हिगेशन ऑप्शन्स
# ==========================================
st.sidebar.title("☰ Pydroid 3 मेनू")

# Pydroid च्या स्क्रीनशॉट २ आणि ३ मधील सर्व ऑप्शन्स इथे समाविष्ट आहेत
menu_choice = st.sidebar.radio(
    "नेव्हिगेशन:",
    ["📝 Editor & Terminal", "📂 File Operations (New/Open)", "📦 Pip Installer", "🔐 Secure Vault", "💡 Code Samples"]
)

# --- १. मुख्य एडिटर आणि टर्मिनल (Screenshot 1 & 2) ---
if menu_choice == "📝 Editor & Terminal":
    st.title("🚀 Python Algo Trading Editor")
    st.caption("NSE, क्रिप्टो आणि फॉरेक्स २४/७ बॅकग्राउंड रनर सक्रिय.")

    # फाईल उघडण्याचे लॉजिक
    current_code = ""
    if os.path.exists(SAVED_CODE_FILE):
        with open(SAVED_CODE_FILE, "r", encoding="utf-8") as f:
            current_code = f.read()
    else:
        current_code = "# तुमच्या अल्गो बोटाचा कोड येथे लिहा...\nimport time\nprint('Pydroid 3 Engine Active!')\n"

    # Pydroid सारखा कस्टमाईज्ड एडिटर (नियम ७)
    code_input = st_ace(
        value=current_code,
        language="python",
        theme="monokai",
        font_size=14,
        height=320,
        auto_update=False
    )

    # नियम ११: custom toolbar shortcut बार (एडिटरच्या खाली झटपट बटन्स)
    st.write("⌨️ **Shortcuts:**")
    sc_col1, sc_col2, sc_col3, sc_col4, sc_col5 = st.columns(5)
    with sc_col1: st.button("Tab Space")
    with sc_col2: st.button("import ccxt")
    with sc_col3: st.button("import yfinance")
    with sc_col4: st.button("while True:")
    with sc_col5: st.button("try / except")

    # ॲक्शन बटन्स (नियम ८, २१, २३ - २४/७ डेमन रनर - No Timeout)
    col1, col2 = st.columns([2, 5])
    with col1:
        if st.button("▶️ RUN CODE", type="primary"):
            clean_code = sanitize_code(code_input)
            with open(SAVED_CODE_FILE, "w", encoding="utf-8") as f:
                f.write(clean_code)
                
            with open(LOG_FILE, "w") as log_f:
                env = os.environ.copy()
                env = inject_credentials(env)
                # स्वतंत्र सब-प्रोसेस runner (नियम १३, २३)
                subprocess.Popen([sys.executable, SAVED_CODE_FILE], stdout=log_f, stderr=subprocess.STDOUT, env=env)
            st.success("बोट बॅकग्राउंडला २४ तास मोडवर सुरू झाला!")
            time.sleep(1)
            st.rerun()

    with col2:
        if st.button("🛑 STOP BOT"):
            if sys.platform == "win32":
                subprocess.run(["taskkill", "/f", "/im", "python.exe"])
            else:
                subprocess.run(["pkill", "-f", SAVED_CODE_FILE])
            st.warning("चालू असलेला अल्गो बोट पूर्णपणे थांबवला आहे.")
            time.sleep(1)
            st.rerun()

    # नियम २२: रिड-ओन्ली टर्मिनल आउटपुट विंडो
    st.subheader("🖥️ टर्मिनल विंडो (Read-Only Console)")
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = f.read()
    else:
        logs = "टर्मिनल रिकामे आहे. कोड रन केल्यानंतर रिझल्ट येथे दिसेल."
    st.markdown(f'<div class="terminal-box"><pre>{logs}</pre></div>', unsafe_allow_html=True)

# --- २. फाईल ऑपरेशन्स (New / Open / Save As - Screenshot 2) ---
elif menu_choice == "📂 File Operations (New/Open)":
    st.title("📂 File Management")
    
    file_action = st.selectbox("ॲक्शन निवडा:", ["New File", "Open Saved File", "Save Backup"])
    
    if file_action == "New File":
        if st.button("🆕 नवीन कोरी फाईल तयार करा"):
            if os.path.exists(SAVED_CODE_FILE): os.remove(SAVED_CODE_FILE)
            if os.path.exists(LOG_FILE): os.remove(LOG_FILE)
            st.success("नवीन फाईल तयार झाली! एडिटर टॅबवर जा.")
            
    elif file_action == "Open Saved File":
        if os.path.exists(SAVED_CODE_FILE):
            st.info(f"सध्या स्टोरेजमध्ये '{SAVED_CODE_FILE}' उपलब्ध आहे.")
        else:
            st.warning("कोणतीही सेव्ह फाईल सापडली नाही.")

# --- ३. पिप पॅकेज मॅनेजर (Screenshot 3) ---
elif menu_choice == "📦 Pip Installer":
    st.title("📦 Pip Package Manager")
    st.write("लायब्ररीज थेट पीआयपी (PyPI) वरून इन्स्टॉल करा.")
    
    lib_to_install = st.text_input("लायब्ररीचे अचूक नाव टाका (उदा. requests, ta):")
    if st.button("📥 Install", type="primary"):
        if lib_to_install:
            st.info(f"'{lib_to_install}' इन्स्टॉलेशन सुरू झाले आहे...")
            res = subprocess.run([sys.executable, "-m", "pip", "install", lib_to_install], capture_output=True, text=True)
            st.code(res.stdout)
        else:
            st.error("कृपया नाव टाका.")

# --- ४. सुरक्षित क्रेडेंशियल्स व्हॉल्ट (नियम १०, २५) ---
elif menu_choice == "🔐 Secure Vault":
    st.title("🔐 API & Telegram Configuration Vault")
    
    api_k = st.text_input("Exchange/Broker API Key:", type="password")
    tg_t = st.text_input("Telegram Bot Token:", type="password")
    tg_i = st.text_input("Telegram Chat ID:")
    
    if st.button("🔒 Save Details", type="primary"):
        with open(VAULT_FILE, "w") as f:
            json.dump({"api_key": api_k, "tg_token": tg_t, "tg_id": tg_i}, f)
        st.success("डिटेल्स सेव्ह झाल्या! कोड रन करताना या ऑटो-इंजेक्ट होतील.")

# --- ५. कोड सॅम्पल्स (Pydroid Samples Option) ---
elif menu_choice == "💡 Code Samples":
    st.title("💡 Ready-to-Use Trading Samples")
    st.write("खालील रेडीमेड सॅम्पल कोड कॉपी करून तुम्ही थेट एडिटरमध्ये वापरू शकता:")
    
    st.subheader("१. क्रिप्टो मार्केट स्कॅनर (CCXT)")
    st.code("""import ccxt
print('Delta Exchange Coins:', len(ccxt.delta().load_markets()))""", language="python")
    
    st.subheader("२. शेअर बाजार आणि फॉरेक्स डेटा (yfinance)")
    st.code("""import yfinance as yf
print(yf.Ticker('RELIANCE.NS').history(period='1d'))""", language="python")
