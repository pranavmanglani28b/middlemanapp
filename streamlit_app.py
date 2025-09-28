import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

st.set_page_config(page_title="Firebase Login Demo")
st.title("🔐 Simple Firebase Login Page")

# i have harcoded the json not very secure though hehe-pranav at 28/09/25
firebase_key = {
    "type": "service_account",
    "project_id": "middleman-bcc1e",
    "private_key_id": "5ba87b5cede57c127f535dd16fd3e8558f915278",
    "private_key": """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDm83/kH4NIdJw4
trX9sHvwnCRlF3f7/YRDz/YOOtX4hf7jNz6a4WC3Jixgalb/v2LaH764Ft7RNE9E
m82sYliC12yY/K9HTIusyWNpcILS+CPUOupb3e1DTzPxUOQXJz931N2zAjo6PVkC
FYVtDDP7KxBeJiixzduDEkNvWUC/93/gXP2jEPwvUn9PIt7RobVICEe+2RKL7zzC
TmewiKTSJGSNr81XVmefPvNcVAo9YR4Y86Z6iIlpCFfPTM6Urs5L1cwMHrSf5/6o
ZGfJVT8pI1HPqiBNFhz3A6V6ya9+BdSdU4B+8uUsNTUkViO0sj7vFTsV8mybLZB+
Hm1caDuDAgMBAAECggEAC7a1+eAPTJF9ivLZcDCPWLjSr73s+/7zwmy90iLxz1Uc
hHG83yYnPaLWBV3fY8FVRjLt/XBLhNjeXGB6og+q5Zf/jhLi4P7k5rKgNCzctc6Y
Ip+KW3Z6HjvaKpcrunDnKzDEvduTEHkkFpL43XsM9+RLRDszPTFvvMokWXVxb0sJ
p90VtQvfegkfuDCjK4bFn42lNdu1VdlQb4bibMnCs+J1gO4AkKnLvB7WNa0EY3z/
my4qD+SByCucNOkaofFd5w6FoRtqR9uAy6U6p0N8vv/J9BuqVqfFw+rNdtAm+QOn
Agq49+kBBNdH0/60h86csBeKgUl778bM+PvS5RQCgQKBgQD65zsanVEgLUYuv9le
R6JjPFeFrinenXkY0+dEUibv5VZFQr6Pm4HfIhIxViz0vOXiWB4br/4bqP4r3UxN
ggtBzvaSMwdo+BnyJUuKh4CU7OnGasRSCnmSbVq7QxMeCz0fIpoJf1BmPRfLfnEZ
4tdNypl0tAMvZaSh2OCm/Bhm8wKBgQDrpIMdFQfn4B1uVzE25kQ86xeXlzyqamga
AivW/o9W1tffkiSSjb8/BcGuRL+5Wiy/SD7NylfHCUBclEAAEWgax7LP5y5yhwNL
HUfSIQLfpYp92OmfQYZUCNiO6BvIgHHVYy2uP0B1268TI2OcknXb/GrwhfqLDUak
HGZy0mEdMQKBgFL+FZDSJLmOAD8Keq4y58YHebPgTj0yvZG21jLFMdf8djLmxv3d
pHHYZUgohypVKX1bRGpIJrejiJ+dzdV9hJe6C9mEQ5k3J+3u5DPoamHYk+NsAZBZ
oqkKvw5eO36enRMlcOpfUIrg/nPzWRoE7M7wix4NRVhyOKjIglb54GB9AoGAShcZ
2oUITVHcLxtfMAHKptTMQC+fNX3raXIRUrILY6R9j6Alu6ax4SDwOtkG50KBG0ud
45qhasVv5Sv/y4Wtk+4CPPhVVFE7Kdz0/g6/Fo64MsWG/zndAIMfhB9azPoF0LA0
Zrsgi24daAkSguJSCG8fOK0Hj70G3wbG94dKXaECgYEAmjWuFD3jNbZJjpO+aCBw
anT4kTp7OtIpA7Ga59QfUeNrcnz4DjCkSAJmpd3gtOld6WH5ij0iI4r3v0jN1pIp
mnZtWu/hAyniNKorqpgSxQuyhKEZ/2MoVwVjibq8gZ8bkYjkqXcqVfHxps4zTJD3
MtA8WhM/1RO9zrrnyCkWf80=
-----END PRIVATE KEY-----"""},
  "client_email": "firebase-adminsdk-fbsvc@middleman-bcc1e.iam.gserviceaccount.com",
  "client_id": "114049452833380016606",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40middleman-bcc1e.iam.gserviceaccount.com",
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
