import streamlit as st
import json
import pathlib
import time
import uuid
import hashlib
from datetime import datetime

# Step 1: Page Config
st.set_page_config(
    page_title="Course Manager",
    page_icon="",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Password hashing helper
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Step 2: Data Loading Logic
json_file = pathlib.Path("users.json")

if json_file.exists():
    with json_file.open("r", encoding="utf-8") as f:
        users = json.load(f)
else:
    users = [
        {
            "id": "1",
            "email": "admin@school.edu",
            "full_name": "System Admin",
            "password": hash_password("123ssag@43AE"),
            "role": "Admin",
            "registered_at": str(datetime.now())
        }
    ]
    with json_file.open("w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)

st.title("Course Manager")
st.divider()

tab_login, tab_register = st.tabs(["Login", "Register"])

# Login Tab
with tab_login:
    st.markdown("## Login")

    with st.container(border=True):
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_password")

        btn_login = st.button("Log In", use_container_width=True)

    if btn_login:
        with st.spinner("Verifying credentials..."):
            time.sleep(1)

        matched_user = None
        for user in users:
            if user["email"] == login_email and user["password"] == hash_password(login_password):
                matched_user = user
                break

        if matched_user:
            st.success(f"Welcome back, {matched_user['full_name']}! Role: {matched_user['role']}")
        else:
            st.error("Invalid email or password.")



# Register Tab
with tab_register:
    st.markdown("## New Instructor Account")

    with st.container(border=True):
        email = st.text_input("Email Address", key="reg_email")
        full_name = st.text_input("First and Last Name", key="reg_full_name")
        password = st.text_input("Password", type="password", key="reg_password")
        role = st.selectbox("Role", ["Instructor"])

        btn_register = st.button("Create Account", use_container_width=True)

    if btn_register:
        with st.spinner("Creating your account..."):
            time.sleep(1)

        new_user = {
            "id": str(uuid.uuid4()),
            "email": email,
            "full_name": full_name,
            "password": hash_password(password),
            "role": role,
            "registered_at": str(datetime.now())
        }
        users.append(new_user)

        with json_file.open("w", encoding="utf-8") as f:
            json.dump(users, f, indent=2)

        st.success("Account created successfully!")
with st.sidebar:
    st.markdown("This is a sidebar")
    if st.button("Log out", type="primary",use_container_width=True):
        time.sleep(5)
        st.success("you are being logged out!")
