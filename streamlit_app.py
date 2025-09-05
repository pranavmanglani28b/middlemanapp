import streamlit as st

def reset_state():
    """Resets all session state variables to their initial values."""
    st.session_state.user_a_data = ""
    st.session_state.user_b_data = ""
    st.session_state.user_a_confirmed = False
    st.session_state.user_b_confirmed = False
    st.session_state.exchange_complete = False

# --- Initialize Session State ---
# This ensures variables persist across user interactions.
if 'user_a_data' not in st.session_state:
    reset_state()

# --- Page Layout and Introduction ---
st.title("🤝 Secure Exchange Middleman")
st.markdown("This app facilitates a secure exchange of information between two parties. The data is only revealed when both parties have submitted and confirmed their details.")

st.warning("Note: This app uses Streamlit's session_state for a simple demo. For a real-world application, a database would be required to manage sessions between different users and devices.")

# --- User Selection ---
st.header("Select Your Role")
# The user selects if they are User A or User B.
user_role = st.radio(
    "Are you User A or User B?",
    ('User A', 'User B'),
    help="Select your role to begin the exchange."
)

# --- User Input and Confirmation ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("User A")
    # Display the input form for User A if not confirmed yet.
    if not st.session_state.user_a_confirmed:
        user_a_input = st.text_area(
            "Enter your information here (User A):",
            value=st.session_state.user_a_data,
            height=150,
            key="user_a_area",
            disabled=(user_role != 'User A')
        )
        if user_a_input:
            st.session_state.user_a_data = user_a_input
            if st.button("Confirm Details (User A)", key="confirm_a", disabled=(user_role != 'User A')):
                st.session_state.user_a_confirmed = True
                st.experimental_rerun()
    else:
        st.success("User A has confirmed their details.")

with col2:
    st.subheader("User B")
    # Display the input form for User B if not confirmed yet.
    if not st.session_state.user_b_confirmed:
        user_b_input = st.text_area(
            "Enter your information here (User B):",
            value=st.session_state.user_b_data,
            height=150,
            key="user_b_area",
            disabled=(user_role != 'User B')
        )
        if user_b_input:
            st.session_state.user_b_data = user_b_input
            if st.button("Confirm Details (User B)", key="confirm_b", disabled=(user_role != 'User B')):
                st.session_state.user_b_confirmed = True
                st.experimental_rerun()
    else:
        st.success("User B has confirmed their details.")

# --- Exchange Logic ---
st.divider()
st.header("Exchange Status")

# Check if both users have confirmed.
if st.session_state.user_a_confirmed and st.session_state.user_b_confirmed:
    st.session_state.exchange_complete = True
    st.balloons()
    st.success("✅ Exchange complete! Both parties have confirmed.")
    
    # Reveal the data to the appropriate user.
    if user_role == 'User A':
        st.info("Here is the information from the other party (User B):")
        st.code(st.session_state.user_b_data, language="text")
    elif user_role == 'User B':
        st.info("Here is the information from the other party (User A):")
        st.code(st.session_state.user_a_data, language="text")

# If the exchange is not complete, show the waiting message.
elif st.session_state.user_a_data or st.session_state.user_b_data:
    st.info("Waiting for both parties to confirm their details...")
else:
    st.info("Please enter your details and confirm to begin the exchange.")

# --- Reset Button ---
st.divider()
if st.button("Start New Exchange", help="Click to reset the state and start over."):
    reset_state()
    st.experimental_rerun()
