import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json
import datetime

# --- Firestore Client Initialization ---
correct = """@st.cache_resource
def get_firestore_client():
    """Initializes and returns a Firestore client object."""
    try:
        # This is the line that throws the error if the key doesn't exist
        key_dict = json.loads(st.secrets["textkey"]) 
        
        # ... rest of connection logic ...
        
        return db
    except KeyError:
        st.error(
            "Configuration Error: 'textkey' not found in secrets.toml. "
            "Please ensure you've copied your Firestore service account JSON into the file."
        )
        return None"""
# This function securely loads your service account credentials 
# from st.secrets and initializes the Firestore client.
@st.cache_resource
def get_firestore_client():
    """Initializes and returns a Firestore client object."""
    try:
        # This is the line that throws the error if the key doesn't exist
        key_dict = json.loads(st.secrets["textkey"]) 
        
        # ... rest of connection logic ...
        
        return db
    except KeyError:
        st.error(
            "Configuration Error: 'textkey' not found in secrets.toml. "
            "Please ensure you've copied your Firestore service account JSON into the file."
        )
        return None
    except KeyError:
        st.error(
            "Configuration Error: 'textkey' not found in secrets.toml. "
            "Please ensure you've copied your Firestore service account JSON into the file."
        )
        return None
    except Exception as e:
        st.error(f"Failed to initialize Firestore client: {e}")
        return None

# Get the database client
db = get_firestore_client()

# --- Streamlit UI and Data Submission Logic ---

st.title("Firestore Data Submission")
st.markdown("Enter a name and a message below. The data will be sent directly to the `messages` collection in your Firestore database.")

if db:
    # Use a Streamlit form to group inputs and submission
    with st.form(key='data_form'):
        name = st.text_input("Your Name", max_chars=100)
        message = st.text_area("Your Message", max_chars=500)
        
        submit_button = st.form_submit_button("Submit Data to Firestore")

        if submit_button:
            if name and message:
                try:
                    # Data dictionary to send to Firestore
                    data = {
                        "name": name,
                        "message": message,
                        "timestamp": datetime.datetime.now(tz=datetime.timezone.utc)
                    }

                    # Add the new document to the 'messages' collection
                    # Firestore will automatically generate a document ID
                    doc_ref = db.collection("messages").add(data)
                    
                    st.success(f"Data submitted successfully! Document ID: {doc_ref[1].id}")
                    
                    # Optional: Display the data sent
                    st.subheader("Data Sent:")
                    st.json(data)
                    
                except Exception as e:
                    st.error(f"An error occurred during submission: {e}")
            else:
                st.warning("Please fill in both the Name and Message fields.")
else:
    st.warning("Cannot connect to the database. Please check your secrets configuration.")
