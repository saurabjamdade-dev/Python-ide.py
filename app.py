import streamlit as st
from streamlit_ace import st_ace
import subprocess
import os
import sys
import json
import re
import requests
from datetime import datetime

# ==========================================
# 📱 PYDROID 3 TRUE FULL-SCREEN PREMIUM INTERFACE
# ==========================================
st.set_page_config(
    page_title="Pydroid 3 IDE", 
    layout="wide", 
    initial_sidebar_state="collapsed" # मोबाईल स्क्रीनसाठी सायडबार डीफॉल्ट बंद राहील
)

# हुबेहूब Pydroid 3 सारखा गडद काळा आणि पिवळा/निळा लूक देणारा प्रगत CSS
st.markdown("""
<style>
    /* मुख्य बॅकग्राउंड आणि फॉन्ट */
    .main { background-color: #151515; color: #ffffff; padding-top: 10px; }
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }
    
    /* Pydroid Top File Header Bar */
    .pydroid-header {
        background-color: #1e1e1e;
        padding: 10px;
        border-radius: 5px;
        border-bottom: 2px solid #ffcc00;
        margin-bottom: 10px;
        font-family: 'Courier New', monospace;
        font-size: 16px;
        color: #ffcc00;
        font-weight: bold;
    }
    
    /* Pydroid Bottom Shortcut Keys */
    .shortcut-container {
        background-color: #1e1e1e;
        padding: 5px;
        border-radius: 5px;
        margin-top: -10px;
        margin-bottom: 15px;
        border: 1px solid #333;
    }
    
    /* Pydroid RUN आणि सिंक बटन्स */
    .stButton>button { 
        background-color: #ffcc00 !important; 
        color: #000000 !important; 
        border-radius: 4px !important; 
        font-weight: bold !important; 
        border: none !important;
        height: 45px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .stButton>button:hover { background-color: #e6b800 !important; }
    
    /* Pydroid ओरिजिनल टर्मिनल लूक */
    .pydroid-terminal { 
        background-color: #000000; 
        border: 1px solid #ffcc00; 
        padding: 15px; 
        border-radius: 5px; 
        font-family: 'Courier New', monospace; 
        color: #ffffff; 
        height: 250px; 
        overflow-y: auto; 
        white-space: pre-wrap;
    }
</style>
""", unsafe_allow_html=True)

VAULT_FILE = "secure_vault.json"
DEFAULT_SCRIPT = "main.py"
RECENT_FILES_LOG = "recent_files.json"

# क्रेडेंशियल्स इंजेक्शन फंक्शन
def inject_vault_credentials(env_dict):
    if os.path.exists(VAULT_FILE):
        try:
            with open(VAULT_FILE, "r", encoding="utf-8") as f:
                vault = json.load(f)
                env_dict["EXCHANGE_API_KEY"] = vault.get("Exchange_API_Key", "")
                env_dict["TELEGRAM_BOT_TOKEN"] = vault.get("Telegram_Bot_Token", "")
                env_dict["TELEGRAM_CHAT_ID"] = vault.get("Telegram_Chat_ID", "")
        except Exception: pass
    return env_dict

# रिसेंट फाईल्स ट्रॅकिंग
def track_recent_file(filename):
    try:
        files = []
        if os.path.exists(RECENT_FILES_LOG):
            with open(RECENT_FILES_LOG, "r") as f: files = json.load(f)
        if filename not in files: files.append(filename)
        with open(RECENT_FILES_LOG, "w") as f: json.dump(files[-10:], f)
    except Exception: pass

# GitHub सेव्ह सिस्टीम
def save_to_github(file_name, code_content):
    if not os.path.exists(VAULT_FILE): return "❌ क्रेडेंशियल्स सापडले नाहीत!"
    with open(VAULT_FILE, "r") as f: vault = json.load(f)
    token = vault.get("GitHub_Personal_Token")
    repo = vault.get("GitHub_Repository")
    if not token or not repo: return "❌ GitHub टोकन सेट नाही!"
    url = f"https://api.github.com/repos/{repo}/contents/{file_name}"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    resp = requests.get(url, headers=headers)
    sha = resp.json().get("sha") if resp.status_code == 200 else None
    import base64
    encoded_content = base64.b64encode(code_content.encode("utf-8")).decode("utf-8")
    payload = {"message": f"🤖 Pydroid Auto-Sync", "content": encoded_content}
    if sha: payload["sha"] = sha
    put_resp = requests.put(url, headers=headers, json=payload)
    return "✅ GitHub वर सिंक यशस्वी!" if put_resp.status_code in [200, 201] else "❌ सिंक अपयशी."

# ==========================================
# 🛠️ SIDEBAR: फक्त अ‍ॅडव्हान्स सेटिंग्जसाठी (गुपित राहील)
# ==========================================
with st.sidebar:
    st.markdown("### ⚙️ Pydroid Settings")
    menu_selection = st.radio("पर्याय निवडा:", ["📝 Code Editor", "🔑 Setup API Vault", "📦 Install Packages"])

# ==========================================
# MAIN INTERACTIVE WORKSPACE
# ==========================================
if menu_selection == "📝 Code Editor":
    
    # फाईल व्यवस्थापन बार (Pydroid स्टाइल)
    file_col1, file_col2 = st.columns([7, 3])
    with file_col1:
        current_file = st.text_input("📄 Active File Name:", value=DEFAULT_SCRIPT, label_visibility="collapsed")
    with file_col2:
        if os.path.exists(RECENT_FILES_LOG):
            with open(RECENT_FILES_LOG, "r") as f: r_files = json.load(f)
            selected_old = st.selectbox("📁 History", ["-- Recent --"] + r_files, label_visibility="collapsed")
            if selected_old != "-- Recent --":
                current_file = selected_old

    # फाईल रीड/राईट लॉजिक
    if os.path.exists(current_file):
        with open(current_file, "r", encoding="utf-8") as f: editor_code = f.read()
    else:
        editor_code = "# Pydroid 3 IDE Environment\nprint('Hello Trader!')\n"

    # Pydroid 3 सारखा टॉप फाईल हेडर डिस्प्ले
    st.markdown(f'<div class="pydroid-header">📁 Editing: {current_file}</div>', unsafe_allow_html=True)

    # ⌨️ मोबाईल कोडिंग शॉर्टकट कीज (Toolbar)
    st.markdown('<div class="shortcut-container">', unsafe_allow_html=True)
    key_cols = st.columns(8)
    shortcuts = ["Tab", "def", "if", "while", "import", "ccxt", "print", "Vault"]
    for i, key in enumerate(shortcuts):
        with key_cols[i]:
            if st.button(key, key=f"btn_{key}", use_container_width=True):
                # शॉर्टकट की दाबली की काय कोड जोडायचा ते इथे ठरवू शकता
                pass
    st.markdown('</div>', unsafe_allow_html=True)

    # 📝 मुख्य एडिटर विंडो (Full Screen Style)
    user_code = st_ace(
        value=editor_code, 
        language="python", 
        theme="twilight", # Pydroid सारखी डार्क थीम
        font_size=15, 
        height=420, 
        auto_update=False, 
        key="pydroid_editor"
    )
    
    track_recent_file(current_file)

    # 🚀 मुख्य ॲक्शन बटन्स (खाली मोठे आणि ठळक)
    st.markdown("---")
    act_col1, act_col2, act_col3 = st.columns([4, 3, 3])
    
    with act_col1:
        run_trigger = st.button("▶️ RUN CODE", use_container_width=True)
    with act_col2:
        save_git = st.button("💾 GIT SYNC", use_container_width=True)
    with act_col3:
        # क्विक सेव्ह फाईल
        save_local = st.button("💾 SAVE LOCAL", use_container_width=True)

    if save_local:
        with open(current_file, "w", encoding="utf-8") as f:
            f.write(user_code)
        st.toast(f"✅ {current_file} लोकल स्टोरेजमध्ये सुरक्षित सेव्ह झाली!", icon="💾")

    if save_git:
        with open(current_file, "w", encoding="utf-8") as f: f.write(user_code)
        st.info(save_to_github(current_file, user_code))

    # 🖥️ ओरिजिनल Pydroid टर्मिनल आउटपुट विंडो
    if run_trigger:
        # रन करण्यापूर्वी फाईल सेव्ह करणे आवश्यक
        with open(current_file, "w", encoding="utf-8") as f:
            f.write(user_code)
            
        st.markdown("##### 🖥️ Terminal Output:")
        try:
            env_run = os.environ.copy()
            env_run = inject_vault_credentials(env_run)
            
            # स्क्रिप्ट रन करा
            res = subprocess.run([sys.executable, current_file], capture_output=True, text=True, env=env_run)
            
            # आउटपुट कंसोल तयार करा
            output_log = res.stdout if res.stdout else res.stderr
            if not output_log:
                output_log = "[Process completed with no output text]"
                
            st.markdown(f'<div class="pydroid-terminal">{output_log}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f'<div class="pydroid-terminal">Execution Error: {e}</div>', unsafe_allow_html=True)

# ==========================================
# CONFIGURATION PAGES (सायडबारमधून ॲक्सेस होतील)
# ==========================================
elif menu_selection == "🔑 Setup API Vault":
    st.title("🔑 Secret Credentials Vault")
    st.info("तुमचे API की आणि टोकन्स इथे सुरक्षित सेव्ह करा. हे थेट तुमच्या स्क्रिप्टमध्ये बॅकएंडला लोड होतील.")
    
    v_git = st.text_input("GitHub Personal Access Token:", type="password")
    v_repo = st.text_input("GitHub Repo Path (user/repo_name):")
    v_exch = st.text_input("Exchange API Key:", type="password")
    v_tg_t = st.text_input("Telegram Bot Token:", type="password")
    v_tg_i = st.text_input("Telegram Chat ID:")
    
    if st.button("🔒 Save and Secure Vault"):
        vault_payload = {"GitHub_Personal_Token": v_git, "GitHub_Repository": v_repo, "Exchange_API_Key": v_exch, "Telegram_Bot_Token": v_tg_t, "Telegram_Chat_ID": v_tg_i}
        with open(VAULT_FILE, "w", encoding="utf-8") as f: json.dump(vault_payload, f)
        st.success("सर्व सिक्रेट की से
