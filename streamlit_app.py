import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

st.set_page_config(page_title="Firebase Login Demo")
st.title("🔐 Simple Firebase Login Page")

# 🔑 Paste your Firebase service account JSON here
firebase_key = {
    "type": "service_account",
    "project_id": "your-project-id",
    "private_key_id": "xxxxxxxxxxxxxxxxxxxx",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEv...snip...\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-xxx@your-project-id.iam.gserviceaccount.com",
    "client_id": "1234567890",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-xxx%40your-project-id.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

# Initialize Firebase
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(firebase_key)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        st.success("✅ Firebase initialized successfully")
    except Exception as e:
        db = None
        st.error(f"❌ Firebase not initialized: {e}")
else:
    db = firestore.client()

# Login form
with st.form("login_form"):
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Login")

if submit:
    if db:
        try:
            db.collection("logins").add({"email": email, "password": password})
            st.success("✅ Credentials sent to Firebase (stored in Firestore).")
        except Exception as e:
            st.error(f"❌ Firebase error: {e}")
    else:
        st.error("❌ Firebase not initialized")
