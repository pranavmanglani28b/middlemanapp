
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import os

st.set_page_config(page_title="Firebase Login Demo")
st.title("🔐 Simple Login Page (Sends creds to Firestore)")

# Firebase initialization - expects firebase_key.json in same folder as app.py
cred_path = os.path.join(os.path.dirname(__file__), "firebase_key.json")
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        st.info("Firebase initialized (using local firebase_key.json).")
    except Exception as e:
        db = None
        st.warning(f"Firebase not initialized: {e}")

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
            st.error(f"Firebase error: {e}")
    else:
        st.error("Firebase not initialized — place your firebase_key.json (service account) in the app folder.")
