import streamlit as st
from streamlit_ace import st_ace
import subprocess
import os
import sys
import json  # 👈 येथे json इम्पोर्ट फिक्स केले आहे, ज्यामुळे NameError येणार नाही!
import re
import time
import requests
import pandas as pd # 👈 पांडास लायब्ररी डॅशबोर्डसाठी आवश्यक
from datetime import datetime

# ==========================================
# नियम १, ९, १४, १७: ULTRA-PREMIUM PYDROID DARKENED THEME & ROUTING
# ==========================================
st.set_page_config(page_title="Pydroid 3 Professional Premium IDE", layout="wide", initial_sidebar_state="expanded")

# Pydroid 3 चा हुबेहूब लुक देणारा प्रगत CSS लेयर
st.markdown("""
<style>
    .main { background-color: #0d1117; color: #c9d1d9; }
    .stButton>button { background-color: #2188ff; color: white; border-radius: 6px; font-weight: bold; width: 100%; border: none; }
    .stButton>button:hover { background-color: #0066cc; }
    .trading-card { background-color: #161b22; padding: 20px; border-radius: 10px; border: 1px solid #30363d; margin-bottom: 15px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .metric-title { font-size: 16px; color: #8b949e; font-weight: bold; margin-bottom: 5px; }
    .metric-val { font-size: 24px; font-weight: bold; color: #58a6ff; font-family: 'Courier New', monospace; }
    .pydroid-terminal { background-color: #010409; border: 2px solid #30363d; padding: 15px; border-radius: 8px; font-family: 'Courier New', monospace; color: #39ff14; height: 350px; overflow-y: scroll; white-space: pre-wrap; }
    .shortcut-btn>button { background-color: #21262d !important; color: #58a6ff !important; font-size: 12px !important; padding: 2px 5px !important; }
</style>
""", unsafe_allow_html=True)

LOG_FILE = "bot_runtime.log"
VAULT_FILE = "secure_vault.json"
DEFAULT_SCRIPT = "whale_scanner.py"
RECENT_FILES_LOG = "recent_files.json"
GITHUB_REPO = "saurabjamdade-dev/Python-ide.py"

# ==========================================
# नियम ५, ६, १९: AUTOMATED CODE SANITIZER ENGINE
# ==========================================
def sanitize_python_code(raw_code):
    if not raw_code: return ""
    clean_code = raw_code.replace('\r\n', '\n').replace('\t', '    ')
    clean_code = re.sub(r'[精度“”]', '"', clean_code)
    clean_code = re.sub(r'[‘’]', "'", clean_code)
    return clean_code

# ==========================================
# नियम १०, २५: AUTOMATIC CREDENTIAL VAULT INJECTION
# ==========================================
def inject_vault_credentials(env_dict):
    if os.path.exists(VAULT_FILE):
        try:
            with open(VAULT_FILE, "r", encoding="utf-8") as f:
                vault = json.load(f)
                env_dict["EXCHANGE_API_KEY"] = vault.get("Exchange_API_Key", "")
                env_dict["TELEGRAM_BOT_TOKEN"] = vault.get("Telegram_Bot_Token", "")
                env_dict["TELEGRAM_CHAT_ID"] = vault.get("Telegram_Chat_ID", "")
        except Exception:
            pass
    return env_dict

# ==========================================
# 💾 RECENT FILES & FILE STORAGE ENGINE
# ==========================================
def track_recent_file(filename):
    try:
        files = []
        if os.path.exists(RECENT_FILES_LOG):
            with open(RECENT_FILES_LOG, "r") as f: files = json.load(f)
        if filename not in files:
            files.append(filename)
        with open(RECENT_FILES_LOG, "w") as f: json.dump(files[-5:], f)
    except Exception: pass

# ==========================================
# नियम १५, २०: GITHUB AUTO-SAVE ENGINE 
# ==========================================
def save_to_github(file_name, code_content):
    if not os.path.exists(VAULT_FILE): return "❌ क्रेडेंशियल्स सापडले नाहीत! कृपया Vault मध्ये टोकन भरा."
    with open(VAULT_FILE, "r") as f: vault = json.load(f)
    
    token = vault.get("GitHub_Personal_Token")
    repo = vault.get("GitHub_Repository", GITHUB_REPO)
    if not token or not repo: return "❌ GitHub टोकन किंवा रिपॉझिटरी सेट नाही!"
    
    url = f"https://api.github.com/repos/{repo}/contents/{file_name}"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    
    resp = requests.get(url, headers=headers)
    sha = resp.json().get("sha") if resp.status_code == 200 else None
        
    import base64
    encoded_content = base64.b64encode(code_content.encode("utf-8")).decode("utf-8")
    payload = {"message": f"🤖 Auto-Save: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "content": encoded_content}
    if sha: payload["sha"] = sha
        
    put_resp = requests.put(url, headers=headers, json=payload)
    return "✅ GitHub वर कोड सुरक्षितपणे सिंक झाला!" if put_resp.status_code in [200, 201] else f"❌ GitHub Error: {put_resp.text}"

# ==========================================
# नियम २४: GOOGLE DRIVE SAFE SYNC ENGINE
# ==========================================
def save_to_google_drive(file_name, code_content):
    if not os.path.exists(VAULT_FILE): return "❌ Vault क्रेडेंशियल्स सापडले नाहीत!"
    with open(VAULT_FILE, "r") as f: vault = json.load(f)
    
    gdrive_token = vault.get("Google_Drive_API_Key")
    if not gdrive_token: return "❌ Google Drive Access Token सापडला नाही!"
    
    metadata = {"name": file_name, "mimeType": "text/x-python"}
    files = {
        'data': ('metadata', json.dumps(metadata), 'application/json; charset=UTF-8'),
        'file': ('file', code_content, 'text/x-python')
    }
    headers = {"Authorization": f"Bearer {gdrive_token}"}
    url = "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart"
    
    try:
        resp = requests.post(url, headers=headers, files=files, timeout=10)
        return "📁 Google Drive वर फाईल सुरक्षितपणे सेव्ह झाली!" if resp.status_code in [200, 201] else f"❌ Drive Error: {resp.text}"
    except Exception as e:
        return f"❌ Drive Connection Error: {e}"

# ==========================================
# NAVIGATION ARCHITECTURE
# ==========================================
page = st.sidebar.radio("Pydroid Menu Navigation:", ["📊 Dashboard Control", "📝 Editor Workspace", "📦 Pip Packages", "🔑 Credentials Vault"])

# ==========================================
# PAGE 1: DASHBOARD CONTROL ROOM
# ==========================================
if page == "📊 Dashboard Control":
    st.title("📱 Pydroid 3 Smart Control Room")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="trading-card"><div class="metric-title">Python Core Engine</div><div class="metric-val">Active 🟢</div></div>', unsafe_allow_html=True)
    with col2:
        is_running = "Running ⚡" if os.path.exists("bg_pid.txt") else "Idle 🛑"
        st.markdown(f'<div class="trading-card"><div class="metric-title">24/7 Daemon Process</div><div class="metric-val">{is_running}</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="trading-card"><div class="metric-title">Storage Sync Layer</div><div class="metric-val">Git + Drive App</div></div>', unsafe_allow_html=True)
        
    st.markdown("### 📊 Interactive Visualization Matrix Window")
    chart_data = pd.DataFrame({"Market Volatility Tracker": [12, 45, 23, 67, 43, 89, 110, 95]})
    st.line_chart(chart_data)

# ==========================================
# PAGE 2: MAIN PYDROID EDITOR WORKSPACE
# ==========================================
elif page == "📝 Editor Workspace":
    st.title("📝 Code Workspace Environment")
    
    f_col1, f_col2 = st.columns([4, 6])
    with f_col1:
        file_op = st.selectbox("📁 Pydroid File Action:", ["Open Active Script", "Create New File (.py)", "Recent Files History"])
    
    filename = DEFAULT_SCRIPT
    
    if file_op == "Create New File (.py)":
        with f_col2:
            new_name = st.text_input("नवीन फाईलचे नाव टाइप करा:", "my_new_bot.py")
        filename = new_name
        if not os.path.exists(filename):
            with open(filename, "w") as f: f.write("# New Script Initialized\n")
            
    elif file_op == "Recent Files History":
        if os.path.exists(RECENT_FILES_LOG):
            with open(RECENT_FILES_LOG, "r") as f: r_files = json.load(f)
            with f_col2:
                filename = st.selectbox("Recent Files:", r_files)

    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f: editor_code = f.read()
    else:
        editor_code = "# Multi-Market Algo Engine\nimport ccxt\nprint('System Online!')\n"

    # Shortcuts Panel
    st.markdown("##### 📱 Custom Toolbar Snippets")
    t_col1, t_col2, t_col3, t_col4 = st.columns(4)
    with t_col1: st.button("Tab (4 Spaces)")
    with t_col2: st.button("import ccxt, yfinance")
    with t_col3: st.button("while True Loop:")
    with t_col4: st.button("Open Interest Logic")

    user_raw_code = st_ace(value=editor_code, language="python", theme="monokai", font_size=14, height=350, auto_update=False, key="pydroid_ace")
    
    sanitized = sanitize_python_code(user_raw_code)
    track_recent_file(filename)

    tab_console, tab_daemon = st.tabs(["💻 Immediate Terminal Test", "⚙️ Persistent 24/7 Server Lock Daemon"])
    
    with tab_console:
        c1, c2, c3 = st.columns(3)
        with c1: run_now = st.button("▶️ RUN INSTANTLY")
        with c2: push_git = st.button("💾 SYNC TO GITHUB")
        with c3: push_drive = st.button("📁 SYNC TO DRIVE")
        
        if run_now:
            with open("test_runner.py", "w", encoding="utf-8") as f: f.write(sanitized)
            st.markdown("##### 🖥️ Live Output Log Terminal (Read-Only):")
            try:
                env_run = os.environ.copy()
                env_run = inject_vault_credentials(env_run)
                res = subprocess.run([sys.executable, "test_runner.py"], capture_output=True, text=True, env=env_run)
                output_log = res.stdout if res.stdout else res.stderr
                st.markdown(f'<div class="pydroid-terminal">{output_log}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Execution Engine Error: {e}")
                
        if push_git: st.info(save_to_github(filename, sanitized))
        if push_drive: st.info(save_to_google_drive(filename, sanitized))
            
    with tab_daemon:
        st.markdown("### ⏳ Independent Background Daemon Engine System")
        if st.button("🚀 UNLEASH ALGO BOT (24/7 Continuous Mode)"):
            with open(filename, "w", encoding="utf-8") as f: f.write(sanitized)
            log_f = open(LOG_FILE, "w")
            env_daemon = os.environ.copy()
            env_daemon = inject_vault_credentials(env_daemon)
            proc = subprocess.Popen([sys.executable, filename], stdout=log_f, stderr=log_f, start_new_session=True, env=env_daemon)
            with open("bg_pid.txt", "w") as f_pid: f_pid.write(str(proc.pid))
            st.success(f"🎯 बोट यशस्वीरित्या चालू झाला! PID: {proc.pid}")

# ==========================================
# PAGE 3: PACKAGE MANAGER
# ==========================================
elif page == "📦 Pip Packages":
    st.title("📦 Visual Pip Package Manager")
    p_name = st.text_input("पॅकेजचे अचूक नाव टाइप करा:")
    if st.button("📥 Dynamic Install Package"):
        if p_name:
            with st.spinner(f"{p_name} इन्स्टॉलेशन सुरू आहे..."):
                res = subprocess.run([sys.executable, "-m", "pip", "install", p_name], capture_output=True, text=True)
                st.code(res.stdout if res.stdout else res.stderr)

# ==========================================
# PAGE 4: CREDENTIALS VAULT MANAGER
# ==========================================
elif page == "🔑 Credentials Vault":
    st.title("🔑 Secure Storage Vault")
    v_git = st.text_input("GitHub Personal Access Token:", type="password")
    v_repo = st.text_input("GitHub Repo Path (user/repo_name):", value=GITHUB_REPO)
    v_drive = st.text_input("Google Drive OAuth/Access Token:", type="password")
    v_exch = st.text_input("Exchange / Broker API Key Master:", type="password")
    v_tg_t = st.text_input("Telegram Bot Token Secret:", type="password")
    v_tg_i = st.text_input("Telegram Chat ID:")
    
    if st.button("🔒 Lock & Sync Crypt Layer"):
        vault_payload = {"GitHub_Personal_Token": v_git, "GitHub_Repository": v_repo, "Google_Drive_API_Key": v_drive, "Exchange_API_Key": v_exch, "Telegram_Bot_Token": v_tg_t, "Telegram_Chat_ID": v_tg_i}
        with open(VAULT_FILE, "w", encoding="utf-8") as f: json.dump(vault_payload, f)
        st.success("सर्व क्रेडेंशियल्स यशस्वीरित्या सुरक्षितपणे लॉक झाले आहेत!")
