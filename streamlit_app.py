import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import time

# --- Setup Instructions ---
# 1. Go to Firebase Console (https://console.firebase.google.com/)
# 2. Create a new project.
# 3. Go to Project Settings -> Service Accounts.
# 4. Click "Generate new private key".
# 5. This will download a JSON file. Rename it to `firebase_key.json` and save it in the same directory as this script.
# 6. Go to Firestore Database and create a new database in "production mode".
# 7. Add security rules to allow read/write access for demonstration purposes:
#    rules_version = '2';
#    service cloud.firestore {
#      match /databases/{database}/documents {
#        match /{document=**} {
#          allow read, write: if true;
#        }
#      }
#    }

@st.cache_resource
def get_firestore_client():
    """Initializes and returns a Firebase Firestore client."""
    try:
        # Load the Firebase service account key from the file.
        # This file should be placed in the same directory as this script.
        # For security, you should use environment variables in production.
        cred = credentials.Certificate("firebase_key.json")
        firebase_admin.initialize_app(cred)
    except ValueError as e:
        if "The default Firebase app already exists" not in str(e):
            st.error(f"Error initializing Firebase: {e}. Please ensure 'firebase_key.json' is in the correct location and is a valid service account file.")
            st.stop()
    return firestore.client()

# --- Initialize Firestore Client ---
db = get_firestore_client()

# --- Main App Logic ---
st.title("🤝 Secure Exchange Middleman (Multi-User)")
st.markdown("Enter a shared Exchange ID to join a session with another person. The data is only revealed when both parties confirm.")

# --- Session Management ---
exchange_id = st.text_input(
    "Enter a shared Exchange ID", 
    help="Both users must enter the same ID to join the same exchange."
).strip()

if not exchange_id:
    st.info("Please enter a shared Exchange ID to begin.")
    st.stop()

# Get a reference to the specific document for this exchange.
exchange_ref = db.collection("exchanges").document(exchange_id)

# --- User Roles and Data ---
st.header("Your Information")
your_role = st.radio(
    "Are you User A or User B?",
    ('User A', 'User B'),
    key="user_role"
)

# Fetch the current state of the exchange from Firestore.
@st.cache_data(show_spinner="Fetching exchange status...")
def get_exchange_status():
    doc = exchange_ref.get()
    return doc.to_dict() if doc.exists else None

exchange_data = get_exchange_status()

# --- User Input Form ---
if your_role == 'User A':
    my_data_key = 'user_a_data'
    my_confirmed_key = 'user_a_confirmed'
    other_data_key = 'user_b_data'
elif your_role == 'User B':
    my_data_key = 'user_b_data'
    my_confirmed_key = 'user_b_confirmed'
    other_data_key = 'user_a_data'

my_confirmed_status = exchange_data.get(my_confirmed_key, False)
other_confirmed_status = exchange_data.get(other_data_key.replace('_data', '_confirmed'), False)

if not my_confirmed_status:
    my_input = st.text_area(
        f"Enter your information here ({your_role}):",
        value=exchange_data.get(my_data_key, ""),
        height=150,
        key="my_area"
    )

    if st.button("Confirm Details"):
        with st.spinner("Uploading data and confirming..."):
            exchange_ref.set({
                my_data_key: my_input,
                my_confirmed_key: True
            }, merge=True)
        st.success("Details confirmed. Waiting for the other party.")
        st.rerun()
else:
    st.success(f"{your_role} has confirmed their details.")

# --- Exchange Status ---
st.divider()
st.header("Exchange Status")

if my_confirmed_status and other_confirmed_status:
    st.balloons()
    st.success("✅ Exchange complete! Both parties have confirmed.")
    st.info("Here is the information from the other party:")
    st.code(exchange_data.get(other_data_key, "No data available."), language="text")

elif exchange_data.get('user_a_confirmed', False) or exchange_data.get('user_b_confirmed', False):
    st.info("Waiting for both parties to confirm their details...")
    # Add a refresh button for the user to check the status.
    if st.button("Check for Updates"):
        st.rerun()

else:
    st.info("Exchange is active. Enter your details to begin.")

# --- Reset Button ---
st.divider()
if st.button("Start a new exchange"):
    if st.warning("Are you sure? This will delete the current exchange."):
        # Delete the document and rerun to reset the state.
        exchange_ref.delete()
        st.rerun()
