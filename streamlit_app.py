import streamlit as st
import requests
import json
from google.cloud import firestore
from google.oauth2 import service_account

# --- Connection Function (Connects to Firestore using secret key) ---

@st.cache_resource
def get_firestore_client():
    """
    Initializes and returns a Firestore client object using the service account 
    key stored securely in Streamlit's secrets.toml file.
    """
    try:
        # Load the service account JSON string from secrets.toml
        key_dict = json.loads(st.secrets["textkey"]) 
        
        # Create credentials object
        creds = service_account.Credentials.from_service_account_info(key_dict)
        
        # Initialize and return the Firestore client
        db = firestore.Client(credentials=creds)
        st.success("Successfully connected to Firestore!")
        return db
        
    except KeyError:
        # This error occurs if 'textkey' is missing in secrets.toml
        st.error(
            "Configuration Error: 'textkey' not found in secrets.toml. "
            "Please ensure you've copied your Firestore service account JSON into the file."
        )
        return None
    except Exception as e:
        # Handle other initialization errors (e.g., malformed JSON)
        st.error(f"Failed to initialize Firestore client: {e}")
        return None

# --- Main Streamlit App Logic ---

# Get the initialized database client
db = get_firestore_client()

st.title("Firestore Data Submission")
st.markdown("Enter data below to save directly into the `messages` collection.")

if db:
    with st.form("data_submission_form"):
        st.subheader("Send Data")
        
        name = st.text_input("Name")
        message = st.text_area("Message")
        
        submitted = st.form_submit_button("Save to Firestore")

        if submitted and name and message:
            try:
                # Add a new document to the 'messages' collection
                doc_ref = db.collection('messages').add({
                    'name': name,
                    'message': message,
                    'timestamp': firestore.SERVER_TIMESTAMP,
                })
                st.success(f"Data successfully saved! Document ID: {doc_ref[1].id}")
            except Exception as e:
                st.error(f"Error saving data to Firestore: {e}")
        elif submitted:
            st.warning("Please enter both a Name and a Message.")

    st.write("---")
    st.subheader("Last 10 Messages (Real-time update disabled in this example)")
    
    # Simple read example (not real-time on every run, as Streamlit reruns on input)
    try:
        messages_ref = db.collection('messages').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(10)
        
        docs = messages_ref.stream()
        
        data_list = []
        for doc in docs:
            doc_data = doc.to_dict()
            data_list.append({
                'Name': doc_data.get('name', 'N/A'),
                'Message': doc_data.get('message', 'N/A'),
                # Convert Firestore Timestamp object to readable string
                'Timestamp': doc_data.get('timestamp').strftime('%Y-%m-%d %H:%M:%S') if doc_data.get('timestamp') else 'N/A',
                'ID': doc.id
            })
        
        if data_list:
            # Use st.dataframe for a nice display
            st.dataframe(data_list, use_container_width=True)
        else:
            st.info("No messages found in the database yet.")

    except Exception as e:
        st.warning(f"Could not retrieve messages: {e}")

else:
    st.error("Cannot proceed until the Firestore client is configured correctly.")
