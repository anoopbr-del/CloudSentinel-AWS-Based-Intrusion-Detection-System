import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pickle
import time
from datetime import datetime
import requests
import csv
import os
from dotenv import load_dotenv
import base64
load_dotenv()
import imaplib
import email
from email.parser import BytesParser, Parser
from email.policy import default
import os
import re
import requests
from bs4 import BeautifulSoup
import numpy as np
import socket
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import streamlit as st
from transformers import pipeline


st.set_page_config(page_title="Network Flow IDS", layout="wide", page_icon=":shield:")

# ---- Simple Authentication (Admin/User) ----
# Default credentials can be overridden via environment variables
USERS = {
    os.getenv("ADMIN_USERNAME", "admin"): {
        "password": os.getenv("ADMIN_PASSWORD", "admin123"),
        "role": "admin",
    },
    os.getenv("USER_USERNAME", "user"): {
        "password": os.getenv("USER_PASSWORD", "user123"),
        "role": "user",
    },
}

def ensure_auth_state():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.role = None

def login_page():
    set_login_background()
    st.markdown(
        """
        <style>
        .login-card {
            background: rgba(0,0,0,0.55);
            padding: 2rem;
            border-radius: 16px;
            -webkit-backdrop-filter: blur(6px);
            backdrop-filter: blur(6px);
            border: 1px solid rgba(255,255,255,0.08);
        }
        .login-title { color: #e5e7eb; text-align: center; margin-bottom: 0.25rem; }
        .login-subtitle { color: #cbd5e1; text-align: center; margin-bottom: 1.5rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        st.markdown("<div class='login-card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='login-title'>🔐 Login</h2>", unsafe_allow_html=True)
        st.markdown("<div class='login-subtitle'>Enter your credentials to continue.</div>", unsafe_allow_html=True)
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            user_record = USERS.get(username)
            if user_record and password == user_record["password"]:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.role = user_record["role"]
                st.success(f"Logged in as {username} ({st.session_state.role})")
                st.rerun()
            else:
                st.error("Invalid username or password")
        st.markdown("</div>", unsafe_allow_html=True)

def set_login_background():
    img_paths = [
        "./assets/login_bg.jpg",
        "./assets/login_bg.png",
        "./login_bg.jpg",
        "./login_bg.png",
    ]
    for path in img_paths:
        if os.path.exists(path):
            try:
                with open(path, "rb") as f:
                    data = f.read()
                b64 = base64.b64encode(data).decode()
                ext = os.path.splitext(path)[1].lower().replace('.', '')
                mime = "jpeg" if ext in ("jpg", "jpeg") else "png"
                st.markdown(
                    f"""
                    <style>
                    .stApp {{
                        background: url('data:image/{mime};base64,{b64}') no-repeat center center fixed;
                        background-size: cover;
                    }}
                    </style>
                    """,
                    unsafe_allow_html=True,
                )
                return
            except Exception:
                pass
    # Fallback gradient if no image is present
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0b1020 100%);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def set_app_background():
    img_paths = [
        "./assets/app_bg.jpg",
        "./assets/app_bg.png",
        "./app_bg.jpg",
        "./app_bg.png",
    ]
    for path in img_paths:
        if os.path.exists(path):
            try:
                with open(path, "rb") as f:
                    data = f.read()
                b64 = base64.b64encode(data).decode()
                ext = os.path.splitext(path)[1].lower().replace('.', '')
                mime = "jpeg" if ext in ("jpg", "jpeg") else "png"
                st.markdown(
                    f"""
                    <style>
                    .stApp {{
                        background: url('data:image/{mime};base64,{b64}') no-repeat center center fixed;
                        background-size: cover;
                    }}
                    </style>
                    """,
                    unsafe_allow_html=True,
                )
                return
            except Exception:
                pass
    # Fallback gradient if no image is present
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0b1020 100%);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def set_sidebar_style():
    # Try a few likely filenames for the cyber attack image
    img_paths = [
        "./assets/sidebar_bg.jpg",
        "./assets/sidebar_bg.png",
        "./assets/cyber_attack.jpg",
        "./assets/cyber_attack.png",
        "./sidebar_bg.jpg",
        "./sidebar_bg.png",
        "./cyber_attack.jpg",
        "./cyber_attack.png",
    ]
    css_bg = ""
    for path in img_paths:
        if os.path.exists(path):
            try:
                with open(path, "rb") as f:
                    data = f.read()
                b64 = base64.b64encode(data).decode()
                ext = os.path.splitext(path)[1].lower().replace('.', '')
                mime = "jpeg" if ext in ("jpg", "jpeg") else "png"
                css_bg = f"background: url('data:image/{mime};base64,{b64}') no-repeat center center; background-size: cover;"
                break
            except Exception:
                pass
    if not css_bg:
        css_bg = "background: linear-gradient(180deg, #111827 0%, #0b1020 100%);"

    st.markdown(
        f"""
        <style>
        /* Sidebar background */
        [data-testid="stSidebar"] > div:first-child {{
            {css_bg}
        }}
        /* Sidebar text colors */
        [data-testid="stSidebar"] * {{
            color: #e5e7eb !important;
        }}
        /* Sidebar selectbox styling */
        [data-testid="stSidebar"] .stSelectbox label {{
            color: #cbd5e1 !important;
            font-weight: 600;
        }}
        [data-testid="stSidebar"] div[data-baseweb="select"] > div {{
            background: rgba(0,0,0,0.45);
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 10px;
        }}
        /* Sidebar buttons */
        [data-testid="stSidebar"] .stButton > button {{
            background: #0ea5e9;
            color: #ffffff;
            border: 1px solid transparent;
            border-radius: 10px;
        }}
        [data-testid="stSidebar"] .stButton > button:hover {{
            background: #0284c7;
            border-color: transparent;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def sidebar_auth_widget():
    ensure_auth_state()
    st.sidebar.write("---")
    if st.session_state.authenticated:
        st.sidebar.success(f"Signed in: {st.session_state.username} ({st.session_state.role})")
        if st.sidebar.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.role = None
            st.rerun()
    else:
        st.sidebar.info("You are not signed in")

def get_allowed_pages():
    ensure_auth_state()
    base_pages = [
        "Home",
        "Live Detection",
        "Live Detection (Graph)",
        "Analytics",
        "Log Analysis",
        "Threat Intelligence",
        "Mail Security",
    ]
    if not st.session_state.authenticated:
        return ["Login"]
    if st.session_state.role == "admin":
        return ["Home", "Training", "Live Detection", "Live Detection (Graph)", "Analytics", "Log Analysis", "Threat Intelligence", "Mail Security", "Settings"]
    return base_pages

# ---- Settings (thresholds, lists) ----
def ensure_settings_state():
    if "detection_threshold" not in st.session_state:
        st.session_state.detection_threshold = 0.80

def read_list_file(path: str):
    try:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
    except Exception:
        pass
    return ""

def write_list_file(path: str, content: str):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content or "")
        return True
    except Exception:
        return False

def settings_page():
    ensure_settings_state()
    st.header("Settings")
    st.subheader("Detection Threshold")
    st.session_state.detection_threshold = st.slider(
        "High-confidence malicious threshold",
        min_value=0.50, max_value=0.99, value=float(st.session_state.detection_threshold), step=0.01,
        help="Alerts are emphasized when model confidence is at or above this value"
    )

    st.subheader("Allowlist / Blocklist")
    col_a, col_b = st.columns(2)
    with col_a:
        st.caption("Allowlist: entries to always treat as benign (one per line; IP/domain)")
        allow_text = st.text_area("Allowlist", value=read_list_file("allowlist.txt"), height=200)
        if st.button("Save Allowlist"):
            ok = write_list_file("allowlist.txt", allow_text)
            st.success("Allowlist saved") if ok else st.error("Failed to save allowlist")
    with col_b:
        st.caption("Blocklist: entries to always flag as malicious (one per line; IP/domain)")
        block_text = st.text_area("Blocklist", value=read_list_file("blocklist.txt"), height=200)
        if st.button("Save Blocklist"):
            ok = write_list_file("blocklist.txt", block_text)
            st.success("Blocklist saved") if ok else st.error("Failed to save blocklist")

@st.cache_data(show_spinner=False)
def load_data():
    df = pd.read_csv('./data/network_traffic.csv')
    return df

def preprocess_data(df):
    df_processed = df.copy()
    df_processed['Label'] = df_processed['Label'].apply(lambda x: 1 if x != 'BENIGN' else 0)
    return df_processed

def train_model(X_train, y_train):
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    return clf

def create_feature_importance_plot(model, feature_names):
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    fig = go.Figure(data=[go.Bar(
        x=[feature_names[i] for i in indices],
        y=[importances[i] for i in indices],
        text=[f"{importances[i]:.3f}" for i in indices],
        textposition='auto',
    )])
    
    fig.update_layout(
        title='Feature Importance',
        xaxis_title='Features',
        yaxis_title='Importance Score',
        xaxis_tickangle=-45
    )
    
    return fig

def analyze_logs(log_data):
    log_lines = log_data.split('\n')
    error_count = sum(1 for line in log_lines if 'ERROR' in line)
    warning_count = sum(1 for line in log_lines if 'WARNING' in line)

    st.write(f"Total log entries: {len(log_lines)}")
    st.write(f"Error entries: {error_count}")
    st.write(f"Warning entries: {warning_count}")
    
    st.subheader("Sample Log Entries")
    st.text("\n".join(log_lines[:10]))

# Function to generate an attack report (with a DataFrame containing a 'Label' column)
def generate_attack_report(df):
    if 'Label' not in df.columns:
        st.write("Dataframe must contain a 'Label' column for attack types.")
        return
    
    attack_counts = df['Label'].value_counts()
    attack_summary = attack_counts[attack_counts.index != 'BENIGN']

    st.write("### Attack Summary")
    st.write(attack_summary)

    fig = px.bar(attack_summary, x=attack_summary.index, y=attack_summary.values, 
                 labels={'x': 'Attack Type', 'y': 'Count'}, title="Attack Distribution")
    st.plotly_chart(fig)
    


API_KEY = os.getenv("API_KEY")
def lookup_input(input_value):
    """
    Lookup an IP Address or Subnet using the AbuseIPDB API.
    For domains, resolve them to an IP address first.
    """
    api_url = "https://api.abuseipdb.com/api/v2/check"
    headers = {
        "Accept": "application/json",
        "Key": API_KEY
    }
    
    params = {
        "maxAgeInDays": 90  # Look back for up to 90 days of abuse reports
    }
    
    try:
        if "/" in input_value:  # Check if it's a subnet
            params["ipAddress"] = input_value
        elif "." in input_value and not input_value.replace(".", "").isdigit():  # Domain name
            resolved_ip = socket.gethostbyname(input_value)
            params["ipAddress"] = resolved_ip
        else:  # Assume it's an IP address
            params["ipAddress"] = input_value

        response = requests.get(api_url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json().get("data", {})
            return {
                "Input": input_value,
                "Resolved IP": params.get("ipAddress"),
                "Is Malicious": data.get("isPublic", False),
                "Threat Score": data.get("abuseConfidenceScore", 0),
                "Last Reported": data.get("lastReportedAt", "Unknown"),
                "Category": data.get("usageType", "N/A"),
                "ISP": data.get("isp", "Unknown"),
                "Country": data.get("countryName", "Unknown")
            }
        else:
            return {"error": f"API request failed with status code {response.status_code}: {response.text}"}
    except socket.gaierror:
        return {"error": "Failed to resolve domain to an IP address."}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}

def display_threat_intelligence():
    """
    Display threat intelligence information in the Streamlit UI.
    """
    st.title("Threat Intelligence Lookup")
    st.markdown("Check an IP Address, Domain Name, or Subnet for potential malicious activity.")
    
    user_input = st.text_input("Enter an IP Address, Domain Name, or Subnet (e.g., 192.168.1.1, example.com, 192.168.0.0/24):")

    if user_input:
        with st.spinner("Looking up threat intelligence data..."):
            result = lookup_input(user_input)
        
        if "error" in result:
            st.error(result["error"])
        else:
            st.write("### Threat Intelligence Results")
            st.write(f"**Input**: {result['Input']}")
            st.write(f"**Resolved IP**: {result['Resolved IP']}")
            st.write(f"**Is Malicious**: {'Yes' if result['Is Malicious'] else 'No'}")
            st.write(f"**Threat Score**: {result['Threat Score']}")
            st.write(f"**Last Reported**: {result['Last Reported']}")
            st.write(f"**Category**: {result['Category']}")
            st.write(f"**ISP**: {result['ISP']}")
            st.write(f"**Country**: {result['Country']}")
            
            if result['Is Malicious']:
                st.warning("This input has a history of malicious activity.")
            else:
                st.success("This input appears to be safe.")
                
def save_flow_data(flow_data, predictions, filename):
    """
    Save flow data along with predictions to a CSV file.
    
    Args:
        flow_data (pd.DataFrame): Original flow data
        predictions (dict): Dictionary containing prediction results
        filename (str): Name of the CSV file to save
    """
    save_df = flow_data.copy()
    
    save_df['detection_time'] = predictions['detection_time']
    save_df['predicted_label'] = predictions['prediction']
    save_df['prediction_confidence'] = predictions['confidence']
   
    os.makedirs('captured_data', exist_ok=True)
    
   
    filepath = os.path.join('captured_data', filename)
    
   
    if os.path.exists(filepath):
        save_df.to_csv(filepath, mode='a', header=False, index=False)
    else:
        save_df.to_csv(filepath, index=False)
    
    return filepath

def live_detection():
    st.header("Live Flow Analysis")
    
    try:
        with open('ids_model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('ids_scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)

        st.sidebar.subheader("Data Capture Settings")
        save_data = st.sidebar.checkbox("Save flow data", value=True)
        custom_filename = st.sidebar.text_input(
            "Custom filename (optional)", 
            value=f"flow_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        
        if st.button("Start Flow Monitoring"):
            placeholder = st.empty()
            metrics_placeholder = st.empty()
            chart_placeholder = st.empty()
            pps_chart_placeholder = st.empty()
            
            flow_history = []
            pps_history = []
            saved_flows_count = 0
            
            for i in range(50):
                df = load_data()
                random_flow = df.iloc[np.random.randint(len(df))].copy()
                scaled_flow = scaler.transform(random_flow.drop('Label').values.reshape(1, -1))
                prediction = model.predict(scaled_flow)[0]
                prediction_prob = model.predict_proba(scaled_flow)[0]
                
                prediction_info = {
                    'detection_time': datetime.now(),
                    'prediction': prediction,
                    'confidence': prediction_prob.max()
                }
                
                if save_data:
                    filepath = save_flow_data(
                        random_flow.to_frame().T,
                        prediction_info,
                        custom_filename
                    )
                    saved_flows_count += 1
                
                flow_history.append({
                    'time': i,
                    'prediction': prediction,
                    'confidence': prediction_prob.max()
                })
                
                with placeholder.container():
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Flow ID", f"#{i+1}")
                    with col2:
                        # Emphasize based on admin-configured threshold
                        det_thresh = float(st.session_state.get('detection_threshold', 0.80))
                        if prediction == 0:
                            st.success("Benign Flow")
                        else:
                            if prediction_prob.max() >= det_thresh:
                                st.error("Suspicious Flow (High Confidence)")
                            else:
                                st.warning("Suspicious Flow (Low Confidence)")
                    with col3:
                        st.metric("Confidence", f"{prediction_prob.max():.2%}")
                    
                    # Add saved flows counter if saving is enabled
                    if save_data:
                        st.info(f"Saved flows: {saved_flows_count}")
                        st.text(f"Saving to: {filepath}")
                    
                    st.json({
                        'Flow Duration': f"{random_flow['Flow Duration']:.2f}",
                        'Fwd Packets': f"{random_flow['Total Fwd Packets']:.2f}",
                        'Bwd Packets': f"{random_flow['Total Backward Packets']:.2f}",
                        'Fwd Bytes': f"{random_flow['Total Length of Fwd Packets']:.2f}",
                        'Bwd Bytes': f"{random_flow['Total Length of Bwd Packets']:.2f}"
                    })
                
                # Update confidence history chart
                if len(flow_history) > 1:
                    history_df = pd.DataFrame(flow_history)
                    fig = px.line(history_df, x='time', y='confidence',
                                color=history_df['prediction'].astype(str),
                                title='Flow Analysis History',
                                color_discrete_map={'0': 'green', '1': 'red'})
                    chart_placeholder.plotly_chart(fig)
                
                # Compute packets per second (approx., assuming Flow Duration in ms)
                try:
                    total_packets = float(random_flow['Total Fwd Packets']) + float(random_flow['Total Backward Packets'])
                    flow_duration_ms = float(random_flow['Flow Duration'])
                    duration_seconds = flow_duration_ms / 1000.0 if flow_duration_ms > 0 else 1.0
                    pps_value = total_packets / duration_seconds
                except Exception:
                    pps_value = float(random_flow.get('Total Fwd Packets', 0)) + float(random_flow.get('Total Backward Packets', 0))
                
                pps_history.append({
                    'time': i,
                    'pps': pps_value
                })
                
                if len(pps_history) > 1:
                    pps_df = pd.DataFrame(pps_history)
                    pps_fig = px.line(pps_df, x='time', y='pps', title='Packets per Second (approx)')
                    pps_chart_placeholder.plotly_chart(pps_fig)
                
                time.sleep(0.5)
            
            if save_data:
                st.success(f"""
                Flow monitoring completed!
                - Total flows captured: {saved_flows_count}
                - Data saved to: {filepath}
                """)
                
    except FileNotFoundError:
        st.error("Please train the model first!")    

def live_detection_graph():
    st.header("Live Detection - Graph View")
    try:
        with open('ids_model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('ids_scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)

        controls = st.columns(3)
        with controls[0]:
            num_iters = st.number_input("Iterations", min_value=10, max_value=500, value=100, step=10)
        with controls[1]:
            delay_ms = st.number_input("Delay (ms)", min_value=0, max_value=2000, value=200, step=50)
        with controls[2]:
            sample_size = st.number_input("Sample Size", min_value=1, max_value=10000, value=1000, step=100)

        start = st.button("Start Graph Monitoring")

        conf_chart = st.empty()
        pps_chart = st.empty()
        meta = st.empty()

        if start:
            conf_history = []
            pps_history = []
            for i in range(int(num_iters)):
                df = load_data()
                if len(df) > sample_size:
                    df = df.sample(sample_size, random_state=None)
                random_flow = df.iloc[np.random.randint(len(df))].copy()
                scaled_flow = scaler.transform(random_flow.drop('Label').values.reshape(1, -1))
                prediction = model.predict(scaled_flow)[0]
                prediction_prob = model.predict_proba(scaled_flow)[0]
                conf = float(np.max(prediction_prob))

                # PPS
                try:
                    total_packets = float(random_flow['Total Fwd Packets']) + float(random_flow['Total Backward Packets'])
                    flow_duration_ms = float(random_flow['Flow Duration'])
                    duration_seconds = flow_duration_ms / 1000.0 if flow_duration_ms > 0 else 1.0
                    pps_value = total_packets / duration_seconds
                except Exception:
                    pps_value = float(random_flow.get('Total Fwd Packets', 0)) + float(random_flow.get('Total Backward Packets', 0))

                conf_history.append({"t": i, "confidence": conf, "pred": str(prediction)})
                pps_history.append({"t": i, "pps": pps_value})

                if len(conf_history) > 1:
                    conf_df = pd.DataFrame(conf_history)
                    conf_fig = px.line(conf_df, x='t', y='confidence', color='pred', title='Prediction Confidence Over Time',
                                       color_discrete_map={'0': 'green', '1': 'red'})
                    conf_chart.plotly_chart(conf_fig, use_container_width=True)

                if len(pps_history) > 1:
                    pps_df = pd.DataFrame(pps_history)
                    pps_fig = px.line(pps_df, x='t', y='pps', title='Packets Per Second (approx)')
                    pps_chart.plotly_chart(pps_fig, use_container_width=True)

                meta.info({
                    "iter": i + 1,
                    "prediction": "Malicious" if prediction == 1 else "Benign",
                    "confidence": round(conf, 4),
                    "pps": round(pps_value, 2)
                })

                if delay_ms:
                    time.sleep(delay_ms / 1000.0)
    except FileNotFoundError:
        st.error("Please train the model first!")

def save_feedback_to_csv(feedback):
    """
    Save the user feedback to a CSV file.
    """
    file_path = "feedback.csv"
    file_exists = os.path.isfile(file_path)
    with open(file_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Feedback"])
        
        writer.writerow([feedback])       




def connect_to_email(host, username, password):
    """Connect to an IMAP email server."""
    mail = imaplib.IMAP4_SSL(host)
    mail.login(username, password)
    return mail

def fetch_emails(mail, folder='inbox'):
    """Fetch emails from a specified folder."""
    mail.select(folder)
    _, data = mail.search(None, 'ALL')
    for num in data[0].split():
        _, data = mail.fetch(num, '(RFC822)')
        yield email.message_from_bytes(data[0][1], policy=default)

def extract_email_features(msg):
    """Extract features from an email message."""
    subject = msg['Subject']
    from_addr = msg['From']
    body = get_email_body(msg)
    attachments = get_email_attachments(msg)
    links = extract_links(body)
    return subject, from_addr, body, attachments, links

def get_email_body(msg):
    """Get the plain text body of an email message."""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                return part.get_payload(decode=True).decode('utf-8')
    else:
        return msg.get_payload(decode=True).decode('utf-8')

def get_email_attachments(msg):
    """Extract attachments from an email message."""
    attachments = []
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_disposition() == 'attachment':
                attachments.append(part)
    return attachments

def extract_links(text):
    """Extract links from the email body."""
    link_pattern = r'https?://\S+|www\.\S+'
    return re.findall(link_pattern, text)

def analyze_attachments(attachments):
    """Analyze the attachments for potential malware."""
    attachment_scores = []
    for attachment in attachments:
        filename = attachment.get_filename()
        if filename:
            score = analyze_file(filename, attachment.get_payload(decode=True))
            attachment_scores.append((filename, score))
    return attachment_scores

# def analyze_file(filename, content):
#     """Analyze a file for potential malware."""
#     # Implement file analysis logic here (e.g., using VirusTotal API)
#     # Return a malware score between 0 and 1 (0 = safe, 1 = malicious)
#     return 0.2

# def analyze_text(text):
#     """Analyze the email body text for potential malicious content."""
#     # Implement text analysis logic here (e.g., using a pre-trained NLP model)
#     # Return a malicious content score between 0 and 1 (0 = safe, 1 = malicious)
#     return 0.3
api_keyy = os.getenv("API_KEYY")
def analyze_file(filename, content):
    """Analyze a file for potential malware."""
    # Example implementation using VirusTotal API
    api_key = api_keyy
    url = "https://www.virustotal.com/vtapi/v2/file/scan"
    files = {'file': (filename, content)}
    params = {'apikey': api_key}
    response = requests.post(url, files=files, params=params)
    
    if response.status_code == 200:
        result = response.json()
        scan_id = result['scan_id']
        report_url = f"https://www.virustotal.com/vtapi/v2/file/report?apikey={api_key}&resource={scan_id}"
        report_response = requests.get(report_url)
        
        if report_response.status_code == 200:
            report = report_response.json()
            positives = report.get('positives', 0)
            total = report.get('total', 1)
            return positives / total
    

def analyze_text(text):
    try:
        classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
        result = classifier(text)
        
        if result:
            score = result[0]['score']
            label = result[0]['label']
            return score if label == 'NEGATIVE' else 0
        return 0  # Default to 0 if no result
    
    except Exception as e:
        print(f"Error in text analysis: {e}")
        return 0

def classify_email(subject, from_addr, body, attachments, links):
    """Classify an email as malicious or benign."""
    subject_score = analyze_text(subject)
    from_score = analyze_text(from_addr)
    body_score = analyze_text(body)
    attachment_scores = analyze_attachments(attachments)
    link_scores = [analyze_text(link) for link in links]

    total_score = (
    subject_score + 
    from_score + 
    body_score + 
    (max(link_scores) if link_scores else 0) + 
    (max(score for _, score in attachment_scores) if attachment_scores else 0)
    ) / 5

    if total_score > 0.5:
        return "Malicious"
    else:
        return "Benign"

def report_email(email_info, classification):
    """Report the email classification to the user."""
    subject, from_addr, body, attachments, links = email_info
    st.write(f"Subject: {subject}")
    st.write(f"From: {from_addr}")
    st.write("Body:")
    st.write(body)
    st.write(f"Attachments: {', '.join([a.get_filename() for a in attachments])}")
    st.write(f"Links: {', '.join(links)}")
    st.write(f"Classification: {classification}")

def final():
    st.title("Email Security Scanner")

    host = st.text_input("IMAP Server Host", "imap.gmail.com")
    username = st.text_input("Email Username")
    password = st.text_input("Email Password", type="password")

    if st.button("Scan Inbox"):
        mail = connect_to_email(host, username, password)
        for msg in fetch_emails(mail):
            email_info = extract_email_features(msg)
            classification = classify_email(*email_info)
            report_email(email_info, classification)

                        
def main():
    ensure_auth_state()
    # Set background: login gets its own, authenticated pages use app background
    if st.session_state.authenticated:
        set_app_background()
        set_sidebar_style()
    st.title("🛡️Intrusion Detection System and Anamoly Detection System")
    
    # Sidebar
    st.sidebar.header("Navigation")
    sidebar_auth_widget()
    allowed_pages = get_allowed_pages()
    # Keep navigation in session state so Quick Action buttons can update it
    if "nav_page" not in st.session_state or st.session_state.nav_page not in allowed_pages:
        st.session_state.nav_page = allowed_pages[0]
    page = st.sidebar.selectbox(
        "Choose a page",
        allowed_pages,
        index=allowed_pages.index(st.session_state.nav_page)
    )
    if page != st.session_state.nav_page:
        st.session_state.nav_page = page
    
    if page == "Home":
        st.markdown("""
        ## Welcome
        This application analyzes network flow and detect potential intrusions.
        it is a combination of anamoly detection system and intrusion detection system.
    
        ### Features:
        - Flow-based traffic analysis
        - Machine learning-based detection
        - Interactive visualizations
        - Real-time flow monitoring
        - Log parsing and analysis
        - Attack detection and reporting
        - Threat intelligence lookup
        
        ### Key Flow Metrics Analyzed:
        - Flow Duration
        - Packet Counts (Forward/Backward)
        - Packet Lengths
        - Inter-arrival Times (IAT)
        - Flow Patterns
        """)
        
        st.sidebar.title("Quick Actions")
        st.sidebar.write("Access the app's main features quickly:")
        
        if st.sidebar.button("View Analytics", key="analytics_btn"):
            if "Analytics" in allowed_pages:
                st.session_state.nav_page = "Analytics"
                st.rerun()
            
        
        if st.sidebar.button("Retrain Model", key="retrain_btn"):
            if "Training" in allowed_pages:
                st.session_state.nav_page = "Training"
                st.rerun()
        
        if st.sidebar.button("Live Detection", key="live_detection_btn"):
            if "Live Detection" in allowed_pages:
                st.session_state.nav_page = "Live Detection"
                st.rerun()
        
        if st.sidebar.button("Log Analysis", key="log_analysis_btn"):
            if "Log Analysis" in allowed_pages:
                st.session_state.nav_page = "Log Analysis"
                st.rerun()

    elif page == "Training":
        if not (st.session_state.authenticated and st.session_state.role == "admin"):
            st.error("You do not have permission to access Training. Please login as an admin.")
            return
        st.header("Model Training")
        
        if st.button("Load and Process Data"):
            with st.spinner("Loading data..."):
                df = load_data()
                st.success(f"Loaded {len(df)} flow records!")
                
                st.subheader("Sample Flow Data")
                st.dataframe(df.head())
                
                df_processed = preprocess_data(df)
                X = df_processed.drop('Label', axis=1)
                y = df_processed['Label']
                
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=0.2, random_state=42)
                
                scaler = StandardScaler()
                X_train_scaled = scaler.fit_transform(X_train)
                X_test_scaled = scaler.transform(X_test)
                
                with st.spinner("Training model..."):
                    model = train_model(X_train_scaled, y_train)
                    
                with open('ids_model.pkl', 'wb') as f:
                    pickle.dump(model, f)
                with open('ids_scaler.pkl', 'wb') as f:
                    pickle.dump(scaler, f)
                
                y_pred = model.predict(X_test_scaled)
                
                st.subheader("Model Performance")
                st.text("Classification Report:")
                st.text(classification_report(y_test, y_pred))
                
                cm = confusion_matrix(y_test, y_pred)
                fig, ax = plt.subplots()
                sns.heatmap(cm, annot=True, fmt='d', ax=ax, 
                          xticklabels=['Benign', 'Malicious'],
                          yticklabels=['Benign', 'Malicious'])
                plt.xlabel('Predicted')
                plt.ylabel('True')
                st.pyplot(fig)
                
                importance_fig = create_feature_importance_plot(model, X.columns)
                st.plotly_chart(importance_fig)

    elif page == "Live Detection":
        live_detection()
    elif page == "Live Detection (Graph)":
        live_detection_graph()
        
        # try:
        #     with open('ids_model.pkl', 'rb') as f:
        #         model = pickle.load(f)
        #     with open('ids_scaler.pkl', 'rb') as f:
        #         scaler = pickle.load(f)
                
        #     if st.button("Start Flow Monitoring"):
        #         placeholder = st.empty()
        #         metrics_placeholder = st.empty()
        #         chart_placeholder = st.empty()
                
        #         flow_history = []
                
        #         for i in range(50):
        #             df = load_data()
        #             random_flow = df.iloc[np.random.randint(len(df))].copy()
        #             scaled_flow = scaler.transform(random_flow.drop('Label').values.reshape(1, -1))
        #             prediction = model.predict(scaled_flow)[0]
        #             prediction_prob = model.predict_proba(scaled_flow)[0]
                    
        #             flow_history.append({
        #                 'time': i,
        #                 'prediction': prediction,
        #                 'confidence': prediction_prob.max()
        #             })
                    
        #             with placeholder.container():
        #                 col1, col2, col3 = st.columns(3)
                        
        #                 with col1:
        #                     st.metric("Flow ID", f"#{i+1}")
        #                 with col2:
        #                     if prediction == 0:
        #                         st.success("Benign Flow")
        #                     else:
        #                         st.error("Suspicious Flow")
        #                 with col3:
        #                     st.metric("Confidence", f"{prediction_prob.max():.2%}")
                        
        #                 st.json({
        #                     'Flow Duration': f"{random_flow['Flow Duration']:.2f}",
        #                     'Fwd Packets': f"{random_flow['Total Fwd Packets']:.2f}",
        #                     'Bwd Packets': f"{random_flow['Total Backward Packets']:.2f}",
        #                     'Fwd Bytes': f"{random_flow['Total Length of Fwd Packets']:.2f}",
        #                     'Bwd Bytes': f"{random_flow['Total Length of Bwd Packets']:.2f}"
        #                 })
                    
        #             if len(flow_history) > 1:
        #                 history_df = pd.DataFrame(flow_history)
        #                 fig = px.line(history_df, x='time', y='confidence',
        #                             color=history_df['prediction'].astype(str),
        #                             title='Flow Analysis History',
        #                             color_discrete_map={'0': 'green', '1': 'red'})
        #                 chart_placeholder.plotly_chart(fig)
                    
        #             time.sleep(0.5)
                    
        # except FileNotFoundError:
        #     st.error("Please train the model first!")

    elif page == "Analytics":
        st.header("Flow Analytics Dashboard")
        
        try:
            df = load_data()
            
            col1, col2 = st.columns(2)
            
            with col1:
                label_counts = df['Label'].value_counts()
                fig = px.pie(values=label_counts.values, 
                            names=label_counts.index,
                            title='Flow Classification Distribution')
                st.plotly_chart(fig)
            
            with col2:
                fig = px.scatter(df, x='Total Fwd Packets', y='Total Backward Packets',
                               color='Label', title='Forward vs Backward Packets',
                               opacity=0.6)
                st.plotly_chart(fig)
            
            fig = px.histogram(df, x='Flow Duration', color='Label',
                             title='Flow Duration Distribution',
                             marginal='box')
            st.plotly_chart(fig)
            
            iat_cols = [col for col in df.columns if 'IAT' in col]
            iat_data = df[iat_cols + ['Label']]
            
            fig = px.box(iat_data.melt(id_vars=['Label'], 
                                     value_vars=iat_cols),
                        x='variable', y='value', color='Label',
                        title="IAT Analysis")
            st.plotly_chart(fig)

            # Protocol Pie Chart if a Protocol column is present
            if 'Protocol' in df.columns:
                proto_counts = df['Protocol'].value_counts()
                proto_fig = px.pie(values=proto_counts.values, names=proto_counts.index, title='Protocol Share')
                st.plotly_chart(proto_fig)
            else:
                st.info("No 'Protocol' column found in data; add one to enable Protocol Pie Chart.")

            # Bubble Chart: IP vs packet size vs attack severity (synthetic placeholders for IP if absent)
            # Since dataset lacks IP columns, we simulate an index-based IP label for visualization only.
            try:
                bubble_df = df.copy().reset_index().rename(columns={"index": "Flow Index"})
                bubble_df["packet_size"] = (
                    bubble_df['Total Length of Fwd Packets'] + bubble_df['Total Length of Bwd Packets']
                )
                # Severity proxy: 0 for BENIGN else 1
                bubble_df["severity"] = (bubble_df['Label'] != 'BENIGN').astype(int)
                bubble_fig = px.scatter(
                    bubble_df.sample(min(len(bubble_df), 1000), random_state=42),
                    x='Flow Index', y='packet_size', size='packet_size', color='severity',
                    title='Bubble: Flow vs Packet Size vs Severity',
                    size_max=40, opacity=0.6, color_continuous_scale=['green', 'red']
                )
                st.plotly_chart(bubble_fig)
            except Exception:
                pass
            
        except FileNotFoundError:
            st.error("Data is not loaded yet. Please load the data first!")

    elif page == "Log Analysis":
        st.header("Log Analysis and Reporting")
        
        st.subheader("Log Upload")
        uploaded_file = st.file_uploader("Choose a log file", type=["txt", "log"])
        if uploaded_file is not None:
            log_data = uploaded_file.getvalue().decode("utf-8")
            st.success("Log file uploaded successfully!")
            
            st.subheader("Log Analysis")
            analyze_logs(log_data)
            
            st.subheader("Attack Report")
            df = load_data()
            generate_attack_report(df)
            
            st.subheader("Log Search")
            search_term = st.text_input("Enter a search term:")
            if search_term:
                st.write(f"Search results for '{search_term}':")
                # Display relevant log entries
            
            # Word Cloud of suspicious tokens (requires wordcloud)
            st.subheader("Word Cloud (Suspicious Terms)")
            try:
                from wordcloud import WordCloud
                tokens = re.findall(r"[A-Za-z0-9_.:-]+", log_data.lower())
                text_for_wc = " ".join(tokens)
                wc = WordCloud(width=800, height=400, background_color="white").generate(text_for_wc)
                fig_wc, ax_wc = plt.subplots(figsize=(10, 5))
                ax_wc.imshow(wc, interpolation='bilinear')
                ax_wc.axis('off')
                st.pyplot(fig_wc)
            except Exception as e:
                st.info("Install 'wordcloud' to see a word cloud (pip install wordcloud)")
                
        else:
            st.info("Please upload a log file to get started.")
    elif page == "Threat Intelligence":
        # Call the function from threat_intelligence.py to display the threat intelligence lookup interface
        display_threat_intelligence()
    elif page == "Mail Security":
        final() 
    elif page == "Login":
        login_page()
    elif page == "Settings":
        if not (st.session_state.authenticated and st.session_state.role == "admin"):
            st.error("You do not have permission to access Settings. Please login as an admin.")
            return
        settings_page()
    # st.sidebar.title("Application Settings")
    # st.sidebar.write("Customize the app's appearance and behavior:")
    # theme = st.sidebar.selectbox("Select a theme", ["Light", "Dark"])
    # if theme == "Dark":
    #     st.markdown("""
    #     <style>
    #     [data-theme="dark"] {
    #         --background-color: #1c1c1e;
    #         --text-color: #f2f2f2;
    #         --primary-color: #0077b6;
    #         --secondary-color: #00a8e8;
    #     }
    #     </style>
    #     """, unsafe_allow_html=True)
    # else:
    #     st.markdown("""
    #     <style>
    #     [data-theme="light"] {
    #         --background-color: #f2f2f2;
    #         --text-color: #1c1c1e;
    #         --primary-color: #0077b6;
    #         --secondary-color: #00a8e8;
    #     }
    #     </style>
    #     """, unsafe_allow_html=True)
        
    st.sidebar.write("---")
    st.sidebar.title("About")
    st.sidebar.write("Reg No:1BI23MC009")
    st.sidebar.write("Name:Amruth swamy c p")
    st.sidebar.write("MCA,Bangalore institute of technology")
    
    st.sidebar.write("---")
    st.sidebar.title("Feedback")
    with st.sidebar.form("feedback_form"):
        st.write("Let us know how we can improve!")
        feedback = st.text_area("Your feedback")
        submit = st.form_submit_button("Submit")
        if submit:
            if feedback.strip():
             save_feedback_to_csv(feedback)
             st.success("Thank you for your feedback! It has been saved.")
        else:
            st.warning(" Please provide your feedback.")
            
if __name__ == "__main__":
    if "page" not in st.session_state:
        st.session_state.page = "Home"
    main()

