import streamlit as st
import json
from google.cloud import firestore
from google.oauth2 import service_account

# --- Connection Function (Connects to Firestore using individual secret keys) ---

@st.cache_resource
def get_firestore_client():
    """
    Initializes and returns a Firestore client object by reconstructing the service account 
    key from individual pieces stored securely in Streamlit's secrets.toml file.
    
    This function specifically looks for the flattened keys (project_id, private_key, etc.)
    """
    try:
        # Check if a mandatory key exists to verify secrets are loaded
        if "project_id" not in st.secrets:
            # If we were previously using 'textkey', the error message is now clearer.
            st.warning("The 'project_id' key is missing from secrets.toml. The database connection cannot be established.")
            return None

        # Reconstruct the service account JSON dictionary from individual secrets
        key_dict = {
            "type": st.secrets["type"],
            "project_id": st.secrets["project_id"],
            "private_key_id": st.secrets["private_key_id"],
            "private_key": st.secrets["private_key"],
            "client_email": st.secrets["client_email"],
            "client_id": st.secrets["client_id"],
            "auth_uri": st.secrets["auth_uri"],
            "token_uri": st.secrets["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["client_x509_cert_url"],
            "universe_domain": st.secrets["universe_domain"],
        }
        
        # Create credentials object
        creds = service_account.Credentials.from_service_account_info(key_dict)
        
        # Initialize and return the Firestore client
        db = firestore.Client(credentials=creds)
        st.success("Successfully connected to Firestore!")
        return db
        
    except KeyError as e:
        # This will catch specific missing keys like 'private_key' if they are placeholders
        st.error(
            f"Configuration Error: Missing key {e} in secrets.toml. "
            "Please ensure you've copied all required fields from your Service Account JSON "
            "into the secrets.toml file."
        )
        return None
    except Exception as e:
        # Handle other initialization errors (e.g., malformed private key)
        st.error(f"Failed to initialize Firestore client. Check the private key formatting. Error: {e}")
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
    st.subheader("Last 10 Messages")
    
    # Simple read example
    try:
        # Ordering by timestamp is generally preferred for chronological lists
        messages_ref = db.collection('messages').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(10)
        
        docs = messages_ref.stream()
        
        data_list = []
        for doc in docs:
            doc_data = doc.to_dict()
            
            # Format timestamp safely
            timestamp_obj = doc_data.get('timestamp')
            # Check if timestamp is a valid datetime object before formatting
            timestamp_str = timestamp_obj.strftime('%Y-%m-%d %H:%M:%S') if timestamp_obj and hasattr(timestamp_obj, 'strftime') else 'N/A'
            
            data_list.append({
                'Name': doc_data.get('name', 'N/A'),
                'Message': doc_data.get('message', 'N/A'),
                'Timestamp': timestamp_str,
                'ID': doc.id
            })
        
        if data_list:
            st.dataframe(data_list, use_container_width=True)
        else:
            st.info("No messages found in the database yet.")

    except Exception as e:
        # This warning remains if there's a problem fetching or parsing data (e.g., security rules)
        st.warning(f"Could not retrieve messages: {e}")
