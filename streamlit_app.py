import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Build credentials dict from st.secrets
secrets = st.secrets["firebase"]

cred_dict = {
    "type": secrets["type"],
    "project_id": secrets["project_id"],
    "private_key_id": secrets["private_key_id"],
    # Important: convert escaped \n into actual newlines
    "private_key": secrets["private_key"].replace('\\n', '\n'),
    "client_email": secrets["client_email"],
    "client_id": secrets["client_id"],
    "auth_uri": secrets["auth_uri"],
    "token_uri": secrets["token_uri"],
    "auth_provider_x509_cert_url": secrets["auth_provider_x509_cert_url"],
    "client_x509_cert_url": secrets["client_x509_cert_url"],
    "universe_domain": secrets["universe_domain"]
}

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

# ✅ Define Firestore client
db = firestore.client()

st.title("🔐 Firebase Login Demo")

with st.form("login_form"):
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Login")

if submit:
    try:
        db.collection("logins").add({"email": email, "password": password})
        st.success("✅ Credentials sent to Firebase (stored in Firestore).")
    except Exception as e:
        st.error(f"Firebase error: {e}")
