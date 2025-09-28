import streamlit as st
import requests
import json
from google.cloud import firestore
from google.oauth2 import service_account

# --- Firebase Configuration ---
# Get API Key from secrets.toml
FIREBASE_API_KEY = st.secrets["AIzaSyD1kOtzXNccOe6cegQdWNSt6uVKb6l9Vpg"]
SIGN_IN_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"

# --- Firestore Setup (for demonstration/optional data retrieval) ---
# NOTE: For deployment, you need to securely configure Firestore credentials.
# Assuming you have a 'firestore-key.json' converted to a string in secrets.toml
try:
    key_dict = json.loads(st.secrets["textkey"]) # Example if using a key string
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds)
except KeyError:
    # Fallback for local development or if only using Firebase Auth
    db = None
    st.info("Firestore client not fully configured. Only authentication is simulated.")


# --- Authentication Functions ---
def authenticate_user(email, password):
    """Authenticates the user against Firebase Auth email/password."""
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    try:
        response = requests.post(SIGN_IN_URL, json=payload)
        response_data = response.json()
        
        if response.status_code == 200:
            # Login successful
            return True, response_data.get("idToken")
        else:
            # Login failed
            error_message = response_data.get("error", {}).get("message", "Unknown error")
            return False, error_message
    except requests.exceptions.RequestException as e:
        return False, f"Request failed: {e}"

# --- Streamlit App Layout ---

st.title("Simple Streamlit & Firebase Login")

# Initialize session state for login status
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
    st.session_state['user_data'] = None

if not st.session_state['authenticated']:
    # Show Login Form
    with st.form("login_form"):
        st.subheader("Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Log In")

        if submitted:
            success, token_or_error = authenticate_user(email, password)
            if success:
                st.session_state['authenticated'] = True
                st.session_state['user_data'] = {'email': email, 'token': token_or_error}
                st.success("Login Successful! Redirecting...")
                st.experimental_rerun() # Rerun to switch to the logged-in view
            else:
                st.error(f"Login Failed: {token_or_error}")

else:
    # Logged-in Content
    st.subheader(f"Welcome back, {st.session_state['user_data']['email']}!")
    
    # Optional: Display some Firestore data (requires Firestore setup to be correct)
    if db:
        st.write("---")
        st.subheader("Your User Data (from Firestore)")
        
        # Example: Fetch data from a 'users' collection using email as document ID
        # NOTE: This is a simplification; use Firebase Auth UIDs for real-world lookups
        doc_ref = db.collection('users').document(st.session_state['user_data']['email'])
        try:
            doc = doc_ref.get()
            if doc.exists:
                st.json(doc.to_dict())
            else:
                st.warning("No custom user profile found in Firestore.")
                
                # OPTIONAL: Create a user document if it doesn't exist
                if st.button("Initialize User Profile in Firestore"):
                    doc_ref.set({"email": st.session_state['user_data']['email'], "created_by_streamlit": True})
                    st.success("Profile initialized. Rerun to view.")
                    st.experimental_rerun()
                    
        except Exception as e:
            st.error(f"Error accessing Firestore: {e}")

    # Logout Button
    if st.button("Log Out"):
        st.session_state['authenticated'] = False
        st.session_state['user_data'] = None
        st.info("Logged out.")
        st.experimental_rerun()
