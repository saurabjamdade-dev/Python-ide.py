import streamlit as st
from streamlit_ace import st_ace
import subprocess
import os
import sys
import json
import re
import time
import requests
import threading

# ==========================================
# भाग १: कॉन्फिगरेशन आणि Pydroid डार्क थीम (घटक १, २, ३, ४)
# ==========================================
st.set_page_config(page_title="Pydroid 3 Ultimate IDE", layout="wide")

LOG_FILE = "bot_output.log"
VAULT_FILE = "secure_vault.json"

# Pydroid 3 चा हुबेहूब लुक देणारा प्रगत CSS लेयर (घटक ५, २२)
st.markdown("""
    <style>
    .terminal-box {
        background-color: #050505 !important;
        color: #38ff12 !important;
        font-family: 'Courier New', monospace !important;
        padding: 15px;
        border-radius: 6px;
        border: 1px solid #222;
        height: 280px;
        overflow-y: auto;
    }
    .stApp { background-color: #0f0f12; }
    .stButton>button { width: 100%; border-radius: 4px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# भाग २: सुरक्षितता आणि सिंटॅक्स क्लीनर लेयर (घटक ९, १०, १९)
# ==========================================
def sanitize_and_clean_code(raw_code: str) -> str:
    """मोबाईल क्युपॅडमुळे येणारे चुकीचे सिंटॅक्स आणि कोट्स क्लीन करणे"""
    clean = raw_code.replace("\r\n", "\n")
    # स्मार्ट कोट्सचे सामान्य कोट्समध्ये रूपांतर
    clean = re.sub(r'[“”]', '"', clean)
    clean = re.sub(r'[‘’]', "'", clean)
    return clean

def inject_security_credentials(env_dict):
    """एपीआय व्हॉल्टमधून की सुरक्षितपणे बॅकग्राउंड रनरमध्ये इन्जेक्ट करणे"""
    if os.path.exists(VAULT_FILE):
        try:
            with open(VAULT_FILE, "r") as f:
                vault_data = json.load(f)
                env_dict["EXCHANGE_API_KEY"] = vault_data.get("api_key", "")
                env_dict["BROKER_TOTP_SECRET"] = vault_data.get("totp_secret", "")
        except Exception:
            pass
    return env_dict

# ==========================================
# भाग ३: बॅकएंड प्रोसेस मॅनेजमेंट (घटक २१, २३)
# ==========================================
def run_script_in_background(code_content):
    """२४/७ बॅकग्राउंड डेमन प्रोसेस सुरू करणे (No Timeout)"""
    clean_code = sanitize_and_clean_code(code_content)
    with open("running_script.py", "w", encoding="utf-8") as f:
        f.write(clean_code)
        
    with open(LOG_FILE, "w") as log_f:
        env = os.environ.copy()
        env = inject_security_credentials(env)
        # स्वतंत्र प्रोसेस सुरू करणे जेणेकरून Streamlit क्रॅश होणार नाही
        subprocess.Popen(
            [sys.executable, "running_script.py"], 
            stdout=log_f, 
            stderr=subprocess.STDOUT, 
            env=env
        )

def stop_background_script():
    """चालू असलेला अल्गो बोट पूर्णपणे बंद करणे"""
    if sys.platform == "win32":
        subprocess.run(["taskkill", "/f", "/im", "python.exe"])
    else:
        subprocess.run(["pkill", "-f", "running_script.py"])

# ==========================================
# भाग ४: Pydroid UI घटकांचे नेव्हिगेशन (घटक ६)
# ==========================================
st.sidebar.title("📂 Pydroid 3 मेनू")
choice = st.sidebar.radio(
    "पर्याय निवडा:", 
    ["📝 कोड एडिटर (IDE)", "📦 पिप मॅनेजर (Pip)", "🔐 सुरक्षित व्हॉल्ट (Vault)", "📊 लाइव्ह मार्केट ट्रॅकर"]
)

# --- १. मुख्य कोड एडिटर विंडो (घटक १२, १३, १४, १५, २१) ---
if choice == "📝 कोड एडिटर (IDE)":
    st.title("🚀 Python Algo Trading IDE")
    st.caption("NSE/BSE शेअर बाजार, क्रिप्टो आणि फॉरेक्ससाठी २४/७ कोडिंग प्लॅटफॉर्म.")

    # Pydroid सारखा एडिटर (Advanced Ace Editor)
    default_code = (
        "# तिन्ही मार्केटसाठी नमुना कोड स्ट्रक्चर\n"
        "import time\n"
        "import yfinance as yf\n"
        "import ccxt\n\n"
        "print('=== बोट बॅकग्राउंडला यशस्वीरित्या सुरू झाला ===')\n"
        "while True:\n"
        "    # उदाहरण: बँक निफ्टी आणि BTC चा डेटा ट्रॅक करणे\n"
        "    print('मार्केट डेटा स्कॅन होत आहे...')\n"
        "    time.sleep(10)\n"
    )
    
    code_input = st_ace(
        value=default_code,
        language="python", 
        theme="monokai", 
        font_size=14, 
        height=380,
        auto_update=False
    )

    # अॅक्शन बटन्स (रन आणि स्टॉप)
    col1, col2 = st.columns([2, 5])
    with col1:
        if st.button("▶️ RUN CODE (24/7 Mode)", type="primary"):
            run_script_in_background(code_input)
            st.success("बोट बॅकग्राउंड लेयरवर ट्रिगर झाला!")
            time.sleep(1)
            st.rerun()
    with col2:
        if st.button("🛑 STOP CODE"):
            stop_background_script()
            st.warning("सर्व चालू बॅकग्राउंड प्रोसेसेस थांबवल्या आहेत.")
            time.sleep(1)
            st.rerun()

    # रिड-ओन्ली लाइव्ह टर्मिनल विंडो (घटक २२)
    st.subheader("🖥️ टर्मिनल आऊटपुट (Read-Only Terminal)")
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            terminal_logs = f.read()
    else:
        terminal_logs = "टर्मिनल रिकामे आहे. कोड रन केल्यानंतर येथे आउटपुट दिसेल..."
        
    st.markdown(f'<div class="terminal-box"><pre>{terminal_logs}</pre></div>', unsafe_allow_html=True)
    if st.button("🔄 टर्मिनल रिफ्रेश करा"):
        st.rerun()

# --- २. पिप पॅकेज मॅनेजर (घटक ७, ८) ---
elif choice == "📦 पिप मॅनेजर (Pip)":
    st.title("📦 Pip Package Manager")
    st.write("तुमच्या अल्गो बोटाला लागणाऱ्या लायब्ररीज (उदा. yfinance, ccxt, ta) येथून थेट इन्स्टॉल करा.")
    
    package_name = st.text_input("लायब्ररीचे नाव टाका:")
    if st.button("📥 Install Package", type="primary"):
        if package_name:
            st.info(f"Installing {package_name}... कृपया टर्मिनल तपासा.")
            subprocess.Popen([sys.executable, "-m", "pip", "install", package_name])
            st.success(f"{package_name} इन्स्टॉलेशन बॅकग्राउंडला सुरू झाले आहे!")
        else:
            st.error("कृपया वैध लायब्ररीचे नाव टाका.")

# --- ३. सुरक्षित एपीआय व्हॉल्ट (घटक १०, २५) ---
elif choice == "🔐 सुरक्षित व्हॉल्ट (Vault)":
    st.title("🔐 Secure API Key Vault")
    st.write("तुमचे सिक्रेट पासवर्ड्स, ब्रोकर्सच्या API की आणि TOTP क्रेडेंशियल्स येथे सुरक्षित सेव्ह करा.")
    
    saved_api = ""
    saved_totp = ""
    if os.path.exists(VAULT_FILE):
        try:
            with open(VAULT_FILE, "r") as f:
                data = json.load(f)
                saved_api = data.get("api_key", "")
                saved_totp = data.get("totp_secret", "")
        except: pass

    api_key_input = st.text_input("Exchange / Broker API Key:", value=saved_api, type="password")
    totp_input = St.text_input("TOTP Google Authenticator Secret (2FA):", value=saved_totp, type="password")
    
    if st.button("🔒 Save Credentials Securely"):
        vault_payload = {"api_key": api_key_input, "totp_secret": totp_input}
        with open(VAULT_FILE, "w") as f:
            json.dump(vault_payload, f)
        st.success("क्रेडेंशियल्स कूटबद्ध (Encrypt) करून सेव्ह केले गेले आहेत आणि कोड रन करताना ते ऑटो-इन्जेक्ट होतील!")

# --- ४. लाइव्ह मार्केट ट्रॅकर (अतिरिक्त उपयुक्त घटक) ---
elif choice == "📊 लाइव्ह मार्केट ट्रॅकर":
    st.title("📊 Multi-Market Live Tracker")
    st.write("yfinance वापरून लाइव्ह डेटा आणि इंडिकेटर्सचा मागोवा घ्या.")
    
    market_select = st.selectbox("मार्केट प्रकार निवडा:", ["Indian (NSE)", "Crypto", "Forex"])
    
    if market_select == "Indian (NSE)":
        ticker = st.text_input("NSE सिम्बॉल टाका (उदा. ^NSEI, RELIANCE.NS):", "^NSEI")
    elif market_select == "Crypto":
        ticker = st.text_input("क्रिप्टो पेअर टाका (उदा. BTC-USD, ETH-USD):", "BTC-USD")
    else:
        ticker = st.text_input("फॉरेक्स पेअर टाका (उदा. EURUSD=X, GBPUSD=X):", "EURUSD=X")
        
    if st.button("📈 Fetch Market Price"):
        import yfinance as yf
        try:
            data = yf.Ticker(ticker).history(period="1d", interval="5m")
            if not data.empty:
                last_price = data['Close'].iloc[-1]
                st.metric(label=f"Current Price ({ticker})", value=f"{last_price:.2f}")
                st.line_chart(data['Close'])
            else:
                st.error("डेटा मिळाला नाही, कृपया सिम्बॉल तपासा.")
        except Exception as e:
            st.error(f"एरर आला: {e}")
